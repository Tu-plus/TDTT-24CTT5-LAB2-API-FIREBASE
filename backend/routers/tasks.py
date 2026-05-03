from fastapi import APIRouter, Depends, HTTPException
from services.auth_dependency import get_current_user
from services.firebase_service import get_db
from schemas.task import TaskCreate, TaskUpdate
from datetime import datetime, timezone
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter()


@router.post("/")
def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
    """Create a new task for the current user."""
    db = get_db()
    uid = user["uid"]

    # Check for duplicate task title
    existing_tasks = db.collection("tasks").where(filter=FieldFilter("uid", "==", uid)).where(filter=FieldFilter("title", "==", task.title)).stream()
    for _ in existing_tasks:
        raise HTTPException(status_code=400, detail="Task với tiêu đề này đã tồn tại")

    task_data = {
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "deadline": task.deadline,
        "completed": False,
        "uid": uid,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    doc_ref = db.collection("tasks").document()
    doc_ref.set(task_data)

    return {"id": doc_ref.id, **task_data}


@router.get("/")
def get_tasks(user: dict = Depends(get_current_user)):
    """Get all tasks for the current user."""
    db = get_db()
    uid = user["uid"]

    docs = db.collection("tasks").where(filter=FieldFilter("uid", "==", uid)).stream()
    tasks = []
    for doc in docs:
        task = doc.to_dict()
        task["id"] = doc.id
        tasks.append(task)

    # Sort tasks: created_at descending -> priority -> deadline -> completed
    tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    tasks.sort(key=lambda x: (
        x.get("completed", False),
        {"high": 1, "medium": 2, "low": 3}.get(x.get("priority", "medium"), 2),
        x.get("deadline") or "9999-12-31"
    ))
    return tasks


@router.patch("/{task_id}")
def update_task(task_id: str, update: TaskUpdate, user: dict = Depends(get_current_user)):
    """Update a task."""
    db = get_db()
    uid = user["uid"]

    doc_ref = db.collection("tasks").document(task_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = doc.to_dict()
    if task_data.get("uid") != uid:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = update.model_dump(exclude_none=True)
    if "priority" in update_data:
        update_data["priority"] = update_data["priority"].value

    doc_ref.update(update_data)
    task_data.update(update_data)
    task_data["id"] = task_id
    return task_data


@router.delete("/{task_id}")
def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    """Delete a task."""
    db = get_db()
    uid = user["uid"]

    doc_ref = db.collection("tasks").document(task_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Task not found")

    if doc.to_dict().get("uid") != uid:
        raise HTTPException(status_code=403, detail="Not authorized")

    doc_ref.delete()
    return {"message": "Task deleted"}
