import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CẤU HÌNH GIAO DIỆN LUXURY ---
st.set_page_config(page_title="PDCA Mastery Simulation", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; border-top: 10px solid #001F3F; }
    .stButton>button { border: 2px solid #C5A021; color: #001F3F; font-weight: bold; }
    .stMetric { border-left: 5px solid #001F3F; background: white; }
    h1, h2, h3 { color: #001F3F; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO TRẠNG THÁI ---
if 'step' not in st.session_state:
    st.session_state.step = "Input"
    st.session_state.profit = 1000
    st.session_state.whys = []
    st.session_state.why_count = 0

# --- MÀN HÌNH 1: INPUT BỐI CẢNH ---
if st.session_state.step == "Input":
    st.title("📦 KanePackage: High-Stakes PDCA Simulation")
    st.subheader("Bối cảnh Quản trị (P-Q-C-D-S-M-E-C)")
    domain = st.selectbox("Chọn khía cạnh trọng yếu[cite: 30, 48]:", 
                          ["Productivity", "Quality", "Cost", "Delivery", "Safety", "Morale", "Environment", "Compliance"])
    problem = st.text_area("Mô tả chi tiết vấn đề tại hiện trường (Genba)[cite: 245]:")
    
    if st.button("BẮT ĐẦU HOẠCH ĐỊNH (PLAN)"):
        st.session_state.domain = domain
        st.session_state.problem = problem
        st.session_state.step = "Plan"
        st.rerun()

# --- MÀN HÌNH 2: PLAN (5W1H2C & 5M) ---
elif st.session_state.step == "Plan":
    st.title("📝 Stage: PLAN - Hoạch định thực chiến [cite: 86, 126]")
    st.write(f"Vấn đề: **{st.session_state.problem}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Thiết lập SMART [cite: 93, 108]")
        target = st.number_input("Mục tiêu cải thiện cụ thể (KPI %):", 0, 100, 80)
    with col2:
        st.subheader("Nguồn lực 5M [cite: 156, 315]")
        man = st.slider("Nhân lực (Man):", 1, 10, 5)
        money = st.slider("Ngân sách (Money - triệu):", 10, 500, 100)

    st.subheader("Kế hoạch thực thi (5W1H2C) [cite: 110, 157]")
    st.text_input("Cách thức thực hiện (How) & Điểm kiểm soát (Control)?")
    
    if st.button("PHÊ DUYỆT KẾ HOẠCH & TRIỂN KHAI"):
        st.session_state.target = target
        st.session_state.step = "Do"
        st.rerun()

# --- MÀN HÌNH 3: DO (BẪY QUẢN LÝ) ---
elif st.session_state.step == "Do":
    st.title("🛠️ Stage: DO - Đối diện bẫy Quản lý [cite: 174, 194]")
    st.warning("⚠️ TÌNH HUỐNG KHẨN CẤP: Dây chuyền phát sinh lỗi lạ, công nhân lúng túng!")
    
    # Các phương án "na ná" nhau lồng ghép bẫy quản lý
    decision = st.radio("Là quản lý hiện trường, bạn chọn phương án nào? [cite: 202, 203]", [
        "A. Trực tiếp xuống tay sửa lỗi cho kịp tiến độ (Bẫy: Quản lý làm thay nhân viên) [cite: 208]",
        "B. Chỉ đạo tổ trưởng tự xử lý và báo cáo sau 2 giờ (Bẫy: Thiếu kiểm soát thực tế - Genbutsu) [cite: 246]",
        "C. Dừng dây chuyền 15p để OJT (Đào tạo tại chỗ) cách xử lý cho nhóm (Tư duy: Manager as Coach) [cite: 338]",
        "D. Yêu cầu tăng ca bù vào phần thời gian máy hỏng (Bẫy: Chỉ tập trung vào Efficiency mà bỏ qua Why) [cite: 161]"
    ])
    
    if st.button("XÁC NHẬN HÀNH ĐỘNG"):
        st.session_state.do_score = 1.0 if "C." in decision else 0.6
        st.session_state.step = "Check"
        st.rerun()

# --- MÀN HÌNH 4: CHECK (5 WHYS KỸ THUẬT CAO) ---
elif st.session_state.step == "Check":
    st.title("📊 Stage: CHECK - Truy vấn nguyên nhân gốc rễ [cite: 103, 233]")
    actual = int(st.session_state.target * st.session_state.do_score)
    st.metric("Kết quả thực tế so với mục tiêu", f"{actual}% / {st.session_state.target}%")

    # Logic 5 Whys động
    why_questions = [
        f"Tại sao kết quả {st.session_state.domain} chỉ đạt {actual}%?",
        "Tại sao hiện tượng đó lại xảy ra ở công đoạn này mà không phải chỗ khác?",
        "Tại sao tiêu chuẩn vận hành hiện tại không ngăn chặn được lỗi này?",
        "Tại sao người phụ trách chưa phát hiện ra rủi ro từ sớm?",
        "Tại sao hệ thống quản trị của chúng ta lại để lỗ hổng này tồn tại? (Chạm đến Root Cause)"
    ]

    if st.session_state.why_count < 5:
        st.subheader(f"Why #{st.session_state.why_count + 1}:")
        st.info(why_questions[st.session_state.why_count])
        ans = st.text_input("Câu trả lời của bạn:", key=f"why_{st.session_state.why_count}")
        if st.button("GỬI PHÂN TÍCH"):
            if ans:
                st.session_state.whys.append(ans)
                st.session_state.why_count += 1
                st.rerun()
    else:
        st.success("Chúc mừng! Bạn đã hoàn thành phân tích 5 Whys chuyên sâu[cite: 248].")
        if st.button("TIẾN TỚI HÀNH ĐỘNG ĐIỀU CHỈNH (ACTION)"):
            st.session_state.step = "Action"
            st.rerun()

# --- MÀN HÌNH 5: ACTION (TIÊU CHUẨN HÓA THỰC THỰC TẾ) ---
elif st.session_state.step == "Action":
    st.title("🚀 Stage: ACTION - Tiêu chuẩn hóa & Phòng ngừa [cite: 264, 275]")
    st.write("Bản chất của Action là đóng lại lỗ hổng vĩnh viễn[cite: 78, 255].")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Tiêu chuẩn hóa (Standardize) [cite: 78, 312]")
        st.checkbox("Cập nhật lại SOP/Bản chỉ dẫn công việc chi tiết [cite: 178]")
        st.checkbox("Niêm yết bảng quản lý trực quan tại hiện trường [cite: 44, 245]")
    with col2:
        st.subheader("2. Lan tỏa (Yokoten) [cite: 46, 274]")
        st.checkbox("Chia sẻ bài học thất bại cho các bộ phận khác [cite: 271]")
        st.checkbox("Thiết lập lịch đào tạo định kỳ cho nhân viên mới [cite: 207]")

    standard_desc = st.text_area("Mô tả quy chuẩn mới bạn sẽ ban hành để không lặp lại sai lầm:")
    
    if st.button("HOÀN TẤT CHU TRÌNH PDCA"):
        st.balloons()
        st.title("🏆 TỔNG KẾT NĂNG LỰC")
        st.write("Dựa trên chu trình bạn vừa thực hiện:")
        st.write("- **Tư duy lập kế hoạch:** Tốt")
        st.write("- **Khả năng điều hành:** " + ("Xuất sắc" if st.session_state.do_score == 1.0 else "Cần tránh bẫy tự làm thay"))
        st.write("- **Phân tích Root Cause:** Đã thực hiện đủ 5 tầng Why [cite: 233]")
        if st.button("Bắt đầu thử thách mới"):
            st.session_state.clear()
            st.rerun()
