import streamlit as st
from config import load_firebase_config
from utils.api_client import api, load_tasks
from utils.auth_helpers import init_firebase

def render_auth_section(auth_component, controller):
    try:
        auth_client = init_firebase()
        firebase_ok = True
    except Exception as e:
        st.error(f"⚠️ Chưa cấu hình Firebase: {e}\n\nVui lòng xem hướng dẫn trong README.md")
        firebase_ok = False

    if firebase_ok:
        _, col, _ = st.columns([1, 5, 1])
        with col:
            st.markdown('<p class="login-title" style="text-align: center;">Đăng nhập</p>', unsafe_allow_html=True)
            st.markdown('<p class="login-sub" style="text-align: center;">Dùng tài khoản Email/Password để tiếp tục</p>', unsafe_allow_html=True)
    
            tab_login, tab_register = st.tabs(["🔑 Đăng nhập", "📝 Đăng ký"])
    
            with tab_login:
                email = st.text_input("Email", key="login_email", placeholder="you@example.com")
                password = st.text_input("Mật khẩu", type="password", key="login_pass", placeholder="••••••••")
                if st.button("Đăng nhập", type="primary", width="stretch"):
                    if email and password:
                        try:
                            result = auth_client.sign_in_with_email_and_password(email, password)
                            st.session_state.id_token = result["idToken"]
                            controller.set('auth_token', result["idToken"])
                            resp = api("get", "/auth/me")
                            if resp and resp.status_code == 200:
                                st.session_state.user = resp.json()
                                load_tasks()
                                st.rerun()
                            else:
                                st.error("Lỗi xác thực với backend")
                        except Exception as e:
                            st.error("Email hoặc mật khẩu không đúng")
                    else:
                        st.warning("Vui lòng nhập đầy đủ thông tin")

                st.markdown('<div class="divider">HOẶC</div>', unsafe_allow_html=True)
                st.markdown('<div class="google-btn-wrapper">', unsafe_allow_html=True)
                google_res = auth_component(config=load_firebase_config(), key="google_login_btn")
                st.markdown('</div>', unsafe_allow_html=True)

                if google_res:
                    if "token" in google_res:
                        st.session_state.id_token = google_res["token"]
                        controller.set('auth_token', google_res["token"])
                        resp = api("get", "/auth/me")
                        if resp and resp.status_code == 200:
                            st.session_state.user = resp.json()
                            load_tasks()
                            st.rerun()
                        else:
                            st.error("Lỗi xác thực với backend")
                    elif "error" in google_res:
                        st.error(f"Lỗi đăng nhập Google: {google_res['error']}")

            with tab_register:
                r_email = st.text_input("Email", key="reg_email", placeholder="you@example.com")
                r_pass  = st.text_input("Mật khẩu", type="password", key="reg_pass", placeholder="Tối thiểu 6 ký tự")
                r_pass2 = st.text_input("Xác nhận mật khẩu", type="password", key="reg_pass2", placeholder="••••••••")
                if st.button("Tạo tài khoản", type="primary", width="stretch"):
                    if r_email and r_pass and r_pass2:
                        if r_pass != r_pass2:
                            st.error("Mật khẩu không khớp")
                        elif len(r_pass) < 6:
                            st.error("Mật khẩu phải có ít nhất 6 ký tự")
                        else:
                            try:
                                auth_client.create_user_with_email_and_password(r_email, r_pass)
                                st.success("✅ Tạo tài khoản thành công! Hãy đăng nhập.")
                            except Exception as e:
                                st.error("Email đã tồn tại hoặc không hợp lệ")
                    else:
                        st.warning("Vui lòng nhập đầy đủ thông tin")
