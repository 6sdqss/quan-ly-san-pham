import streamlit as st
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ Thống Quản Lý Sản Phẩm", page_icon="📦", layout="wide")

# --- QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

# --- HÀM TẢI DỮ LIỆU TỪ GOOGLE SHEETS ---
# Sử dụng st.cache_data để cache dữ liệu trong 5 phút (300 giây) giống CACHE_TTL trong code gốc của bạn
@st.cache_data(ttl=300)
def load_product_data():
    # Link Google Sheets của bạn chuyển sang định dạng CSV
    SHEET_ID = "1wtIhG3O1_oDrJcUvgwxcjxeRnrWpqbWIN15c4a37kl0"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()

# --- GIAO DIỆN ĐĂNG NHẬP ---
def login_ui():
    st.markdown("<h2 style='text-align: center; color: #2563eb;'>HỆ THỐNG QUẢN LÝ SẢN PHẨM</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Đăng nhập hệ thống")
            email = st.text_input("Email")
            password = st.text_input("Mật khẩu", type="password")
            submit_button = st.form_submit_button("Đăng nhập")
            
            if submit_button:
                # Ở đây tôi làm logic cứng để demo. 
                # Thực tế bạn có thể đọc từ Sheet Permission_Log của bạn.
                if email == "nguyenduc6655@gmail.com":
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = 'Admin'
                    st.success("Đăng nhập thành công!")
                    time.sleep(1)
                    st.rerun()
                elif email != "" and password == "123456": # Mật khẩu mặc định cho user
                    st.session_state['logged_in'] = True
                    st.session_state['user_role'] = 'User'
                    st.success("Đăng nhập thành công!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu không đúng!")

# --- GIAO DIỆN CHÍNH ---
def main_ui():
    # Header user bar
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**👤 Xin chào, {st.session_state['user_role']}** | 🕐 Cập nhật lúc: {time.strftime('%H:%M:%S')}")
    with col2:
        if st.button("🔄 Tải lại dữ liệu (F5)"):
            st.cache_data.clear()
            st.rerun()
        if st.button("Đăng xuất"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Load dữ liệu gốc
    with st.spinner("📦 Đang khởi tạo dữ liệu..."):
        df_products = load_product_data()

    # Tạo các Tabs giống với giao diện HTML của bạn
    tab_overview, tab_image, tab_idgroup, tab_article, tab_video, tab_admin = st.tabs([
        "📊 Tổng quan", "🖼️ Trạng thái hình", "📦 Thống kê Bộ Hình", "✍️ Bài viết", "🎬 Quản lý Video", "🔐 Admin"
    ])

    # 1. TAB TỔNG QUAN
    with tab_overview:
        st.markdown("### 📊 Báo cáo tiến độ chung")
        
        # Dashboard metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tất cả Sản phẩm", f"{len(df_products)}")
        m2.metric("Bộ hình đã làm", "0", delta="Cần connect Gspread")
        m3.metric("Bài viết xong", "0")
        m4.metric("Video đã làm", "0")

        st.markdown("#### Dữ liệu đầu vào (Source Sheet)")
        st.dataframe(df_products, use_container_width=True)

    # 2. TAB TRẠNG THÁI HÌNH
    with tab_image:
        st.markdown("### ⏳ Đang chờ xử lý / Lịch sử xử lý")
        # Ví dụ bộ lọc cơ bản với Streamlit
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            search = st.text_input("🔍 Tìm ID / ERP / Tên...", key="search_img")
        
        if not df_products.empty:
            # Lọc dataframe cơ bản
            df_display = df_products
            if search:
                df_display = df_display[df_display.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
            st.dataframe(df_display.head(50), use_container_width=True) # Hiển thị 50 dòng đầu

    # 3. TAB THỐNG KÊ BỘ HÌNH
    with tab_idgroup:
        st.markdown("### 📦 Thống kê Bộ Hình & Phân loại")
        st.info("Tính năng đang được chuyển đổi từ giao diện web sang Streamlit Components.")

    # 4. TAB BÀI VIẾT
    with tab_article:
        st.markdown("### 📝 Đang chờ | 🗂 Lịch sử Bài viết")
        st.info("Sử dụng st.data_editor() tại đây để tạo bảng cho phép tích chọn check box trực tiếp trên web.")

    # 5. TAB VIDEO
    with tab_video:
        st.markdown("### 🎬 Quản lý Video")

    # 6. TAB ADMIN
    with tab_admin:
        if st.session_state['user_role'] == 'Admin':
            st.markdown("### 👑 Cấp quyền Nhân viên")
            st.text_input("Nhập Email nhân viên...")
            st.button("Lưu quyền")
        else:
            st.warning("Bạn không có quyền truy cập tab này.")

# --- LUỒNG CHẠY CHÍNH ---
if not st.session_state['logged_in']:
    login_ui()
else:
    main_ui()