import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Expert PDCA Challenge", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; border-top: 8px solid #001F3F; }
    h1, h2, h3 { color: #001F3F; font-family: 'Arial Black'; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); border-left: 5px solid #C5A021; }
    .stButton>button { background-color: #001F3F; color: #C5A021; border: 1px solid #C5A021; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if 'step' not in st.session_state:
    st.session_state.step = "Selection"
    st.session_state.resources = {"Man": 10, "Money": 1000, "Method": 5, "Machine": 5, "Material": 100}
    st.session_state.kpis = {"Efficiency": 70, "Quality": 80, "Safety": 90, "Morale": 75}

def update_kpi(kpi, val):
    st.session_state.kpis[kpi] = max(0, min(100, st.session_state.kpis[kpi] + val))

# --- GIAO DIỆN DASHBOARD ---
def sidebar_status():
    st.sidebar.title("📊 Quản trị Nhà máy (QCD)")
    for k, v in st.session_state.kpis.items():
        st.sidebar.progress(v/100, text=f"{k}: {v}%")
    st.sidebar.markdown("---")
    st.sidebar.write("**Nguồn lực hiện có (5M):**")
    st.sidebar.write(st.session_state.resources)

# --- MÀN HÌNH 1: CHỌN CHỦ ĐỀ (P-Q-C-D-S-M-E-C) ---
if st.session_state.step == "Selection":
    st.title("🛡️ KanePackage: Expert PDCA Simulation")
    st.subheader("Bước 0: Chọn khía cạnh quản trị cần cải tiến")
    
    domains = {
        "Productivity (Năng suất)": "P", "Quality (Chất lượng)": "Q", 
        "Cost (Chi phí)": "C", "Delivery (Tiến độ)": "D",
        "Safety (An toàn)": "S", "Morale (Tâm lý)": "M",
        "Environment (Môi trường)": "E", "Compliance (Tuân thủ)": "C"
    }
    
    choice = st.selectbox("Học viên chọn chủ đề thực hành:", list(domains.keys()))
    problem_desc = st.text_area("Mô tả thực trạng hiện trường (Genba):", placeholder="Ví dụ: Tỷ lệ thùng carton lỗi tại máy cắt đang là 5%...")
    
    if problem_desc:
        st.info("Câu hỏi truy vấn hiện trạng (5W1H):")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Vấn đề này xảy ra ở công đoạn nào? (Where)")
            st.text_input("Tần suất xuất hiện là khi nào? (When)")
        with col2:
            st.text_input("Ai là người trực tiếp thao tác? (Who)")
            st.text_input("Tại sao vấn đề này lại quan trọng cần giải quyết ngay? (Why)")

        if st.button("XÁC NHẬN BỐI CẢNH & VÀO PLAN"):
            st.session_state.domain = domains[choice]
            st.session_state.problem = problem_desc
            st.session_state.step = "Plan"
            st.rerun()

# --- MÀN HÌNH 2: PLAN (5W1H2C + 5M + SMART) ---
elif st.session_state.step == "Plan":
    sidebar_status()
    st.title("📝 Stage: PLAN (Hoạch định)")
    
    with st.expander("🎯 Thiết lập mục tiêu SMART", expanded=True):
        st.write(f"Vấn đề: {st.session_state.problem}")
        goal = st.text_input("Nhập mục tiêu cải tiến của nhóm (Ví dụ: Giảm lỗi phế phẩm từ 5% xuống 1% trong 2 tuần):")
        st.checkbox("Mục tiêu cụ thể (Specific)?")
        st.checkbox("Đo lường được (Measurable)?")
        st.checkbox("Khả thi (Achievable)?")
    
    st.subheader("⚙️ Lập kế hoạch 5W1H2C & Phân bổ 5M")
    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Nguồn lực (5M)**")
            m1 = st.slider("Nhân lực (Man)", 0, 10, 5)
            m2 = st.slider("Ngân sách (Money)", 0, 1000, 200)
            m3 = st.slider("Nguyên vật liệu (Material)", 0, 100, 20)
        with col2:
            st.write("**Kiểm soát (2C)**")
            c1 = st.text_input("Phương pháp kiểm tra (Check - KPI)?")
            c2 = st.text_input("Cách thức kiểm soát (Control)?")
            
        st.write("**Lộ trình (Gantt Chart logic)**")
        st.date_input("Ngày bắt đầu")
        st.date_input("Ngày hoàn thành")
        
        if st.form_submit_button("PHÊ DUYỆT KẾ HOẠCH & VÀO DO"):
            st.session_state.resources["Man"] -= m1
            st.session_state.resources["Money"] -= m2
            st.session_state.step = "Do"
            st.rerun()

# --- MÀN HÌNH 3: DO (HORENSO, ĐÀO TẠO, ĐỘNG LỰC) ---
elif st.session_state.step == "Do":
    sidebar_status()
    st.title("🛠️ Stage: DO (Thực hiện & Điều hành)")
    
    day = st.radio("Mô phỏng ngày vận hành:", ["Ngày 1: Triển khai", "Ngày 2: Biến cố", "Ngày 3: Về đích"])
    
    if day == "Ngày 1: Triển khai":
        st.write("Bạn cần đào tạo công nhân theo bản hướng dẫn công việc (SOP).")
        action = st.selectbox("Hành động của bạn:", ["Trực tiếp hướng dẫn tại hiện trường (OJT)", "Gửi tài liệu tự đọc", "Ủy quyền cho tổ trưởng"])
        if st.button("Xác nhận hành động"):
            update_kpi("Quality", 5 if "OJT" in action else -5)
            st.success("Đã ghi nhận hành động đào tạo.")
            
    elif day == "Ngày 2: Biến cố":
        st.error("⚠️ BIẾN CỐ: Có sự hiểu lầm về thông tin giữa ca sáng và ca chiều!")
        horenso = st.radio("Bạn sử dụng kỹ năng Horenso nào?", ["Họp bàn bạc (Sodan) tìm đối sách", "Chỉ ra lệnh báo cáo (Hokoku)", "Gửi tin nhắn thông báo (Renraku)"])
        if st.button("Xử lý biến cố"):
            update_kpi("Morale", 10 if "Sodan" in horenso else -5)
            st.info("Kỹ năng bàn bạc giúp tăng tinh thần đội ngũ.")

    elif day == "Ngày 3: Về đích":
        st.write("Kết thúc đợt triển khai thí điểm.")
        if st.button("TIẾN TỚI BƯỚC CHECK"):
            st.session_state.step = "Check"
            st.rerun()

# --- MÀN HÌNH 4: CHECK & ACTION (5 WHY, PARETO, STANDARDIZE) ---
elif st.session_state.step == "Check":
    sidebar_status()
    st.title("📊 Stage: CHECK (Kiểm tra & Đánh giá)")
    
    # Giả lập dữ liệu kết quả
    target = 90
    actual = st.session_state.kpis["Quality"]
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = actual,
        delta = {'reference': target},
        title = {'text': "Kết quả thực tế vs Mục tiêu (KPI)"},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#001F3F"}}
    ))
    st.plotly_chart(fig)
    
    st.subheader("🔍 Phân tích nguyên nhân gốc rễ (5 Whys)")
    why1 = st.text_input("Tại sao kết quả chưa đạt kỳ vọng? (Lần 1)")
    why2 = st.text_input("Tại sao? (Lần 2)")
    
    if st.button("CHUYỂN SANG ACTION"):
        st.session_state.step = "Action"
        st.rerun()

elif st.session_state.step == "Action":
    st.title("🚀 Stage: ACTION (Tiêu chuẩn hóa & Cải tiến)")
    st.write("Dựa trên phân tích ở bước Check, bạn sẽ làm gì?")
    
    act_choice = st.radio("Lựa chọn hành động:", [
        "Tiêu chuẩn hóa thành quy trình mới (Standardization)",
        "Tiếp tục cải tiến (Kaizen) vì chưa đạt mục tiêu",
        "Thay đổi hoàn toàn kế hoạch (Plan lại)"
    ])
    
    st.text_area("Mô tả nội dung tiêu chuẩn hóa hoặc bước Kaizen tiếp theo:")
    
    if st.button("KẾT THÚC DỰ ÁN & XEM ĐIỂM"):
        st.balloons()
        final_score = sum(st.session_state.kpis.values())
        st.header(f"🏆 Tổng điểm năng lực PDCA: {final_score}")
        if final_score > 320:
            st.success("Bạn là Chuyên gia PDCA thực thụ!")
        else:
            st.warning("Bạn cần chú ý hơn về việc cân bằng nguồn lực và đào tạo con người.")
        
        if st.button("Thực hiện dự án mới"):
            st.session_state.clear()
            st.rerun()
