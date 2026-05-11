import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CẤU HÌNH GIAO DIỆN LUXURY ---
st.set_page_config(page_title="KanePackage PDCA Simulation", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #001F3F; color: #C5A021; border-radius: 8px; border: 1.5px solid #C5A021; font-weight: bold; height: 3em; }
    .stButton>button:hover { background-color: #C5A021; color: #001F3F; }
    h1, h2, h3 { color: #001F3F; font-family: 'Helvetica Neue', sans-serif; }
    .stAlert { border-left: 5px solid #C5A021; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if 'step' not in st.session_state:
    st.session_state.step = "Input"
    st.session_state.profit = 1000 
    st.session_state.domain = "General"

# --- HÀM PHÂN TÍCH TỪ KHÓA (AI NỘI BỘ) ---
def analyze_domain(text):
    text = text.lower()
    if any(word in text for word in ['máy', 'thiết bị', 'hỏng', 'lỗi', 'kỹ thuật']):
        return "Technical"
    if any(word in text for word in ['người', 'công nhân', 'ý thức', 'thao tác', 'đào tạo']):
        return "Human"
    if any(word in text for word in ['muộn', 'trễ', 'giao hàng', 'tiến độ', 'khách hàng']):
        return "Delivery"
    return "General"

# --- STEP 0: INPUT & CONTEXT ---
if st.session_state.step == "Input":
    st.title("📦 KanePackage: PDCA Strategic Challenge")
    st.subheader("Bối cảnh: Hiện trường & Hiện vật (Genba & Genbutsu)")
    
    with st.container():
        problem_desc = st.text_area("Học viên mô tả vấn đề/tải file mô tả:", 
                                   placeholder="Ví dụ: Tỷ lệ phế phẩm thùng carton tại máy cắt số 4 đang quá cao...")
        
        if problem_desc:
            st.session_state.domain = analyze_domain(problem_desc)
            st.info(f"Hệ thống xác nhận bối cảnh thuộc nhóm: **{st.session_state.domain}**")
            
            st.write("---")
            q1 = st.text_input("1. Mục tiêu cụ thể (KPI) bạn muốn đạt được là gì?")
            q2 = st.text_input("2. Hiện tại lỗi này đang gây thiệt hại bao nhiêu (ước tính)?")
            
            if st.button("XÁC NHẬN & LẬP KẾ HOẠCH (PLAN)"):
                st.session_state.kpi_target = q1
                st.session_state.step = "Plan_Strategy"
                st.rerun()

# --- STEP 1: PLAN (CHIẾN LƯỢC & HÀNH ĐỘNG) ---
elif st.session_state.step == "Plan_Strategy":
    st.title("📝 Giai đoạn: PLAN (Lập kế hoạch)")
    
    # Dữ liệu kịch bản linh hoạt
    scenarios = {
        "Technical": [
            {"name": "Bảo trì phòng ngừa & Thay linh kiện", "cost": 150, "gain": 400},
            {"name": "Lắp đặt hệ thống cảm biến Jidoka", "cost": 300, "gain": 700},
            {"name": "Mời chuyên gia Nhật Bản kiểm tra máy", "cost": 200, "gain": 500}
        ],
        "Human": [
            {"name": "Đào tạo lại bộ quy chuẩn thao tác (SOP)", "cost": 50, "gain": 300},
            {"name": "Thiết lập cơ chế thưởng Kaizen cho công nhân", "cost": 80, "gain": 400},
            {"name": "Thiết kế lại bảng hướng dẫn trực quan (Visual Management)", "cost": 30, "gain": 200}
        ],
        "Delivery": [
            {"name": "Tối ưu hóa sơ đồ đường đi trong kho", "cost": 100, "gain": 350},
            {"name": "Thay đổi nhà cung cấp vận chuyển nội địa", "cost": 120, "gain": 400},
            {"name": "Số hóa quy trình theo dõi đơn hàng", "cost": 250, "gain": 600}
        ],
        "General": [
            {"name": "Tổ chức tổng vệ sinh 5S toàn nhà máy", "cost": 20, "gain": 150},
            {"name": "Họp nhóm chất lượng định kỳ hàng tuần", "cost": 40, "gain": 200},
            {"name": "Rà soát lại toàn bộ quy trình từ đầu", "cost": 100, "gain": 300}
        ]
    }

    current_options = scenarios[st.session_state.domain]
    
    st.write("### 1. Chọn chiến lược ưu tiên:")
    cols = st.columns(3)
    for i, option in enumerate(current_options):
        with cols[i]:
            if st.button(f"{option['name']}\n(Chi phí: {option['cost']}tr)"):
                st.session_state.selected_opt = option
                st.session_state.profit -= option['cost']
                st.session_state.step = "Plan_Detail"
                st.rerun()

elif st.session_state.step == "Plan_Detail":
    st.title("📝 PLAN: Chi tiết hóa hành động")
    st.write(f"Chiến lược: **{st.session_state.selected_opt['name']}**")
    
    st.write("### 2. Thiết lập khung thực thi (5W1H):")
    with st.form("5w1h"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Who (Ai phụ trách?)")
            st.text_input("Where (Địa điểm triển khai?)")
        with col2:
            st.text_input("When (Thời hạn hoàn thành?)")
            st.text_input("How (Cách thức đo lường?)")
        
        st.write("---")
        st.write("Dựa trên mục tiêu: " + st.session_state.kpi_target)
        kpi_val = st.slider("Bạn cam kết giảm tỷ lệ lỗi/tăng hiệu suất bao nhiêu %?", 0, 100, 50)
        
        if st.form_submit_button("CHỐT KẾ HOẠCH & TRIỂN KHAI (DO)"):
            st.session_state.kpi_commitment = kpi_val
            st.session_state.step = "Do"
            st.rerun()

# --- STEP 2: DO (THỰC HIỆN & BIẾN CỐ) ---
elif st.session_state.step == "Do":
    st.title("🛠️ Giai đoạn: DO (Thực hiện)")
    st.warning("⚠️ BIẾN CỐ BẤT NGỜ TẠI HIỆN TRƯỜNG!")
    
    disruptions = [
        "Máy đột ngột dừng do quá tải nhiệt!",
        "Một nhóm công nhân phản đối vì quy trình mới quá phức tạp.",
        "Khách hàng yêu cầu thay đổi thiết kế thùng ngay lập tức."
    ]
    event = disruptions[0] if st.session_state.domain == "Technical" else disruptions[1]
    
    st.error(f"Sự cố: {event}")
    choice = st.radio("Nhóm của bạn quyết định ứng phó thế nào?", [
        "Dừng lại để giải quyết triệt để rồi mới làm tiếp",
        "Vừa làm vừa sửa (Chắp vá) để kịp tiến độ",
        "Bỏ qua sự cố, tập trung hoàn thành KPI đã cam kết"
    ])
    
    if st.button("XÁC NHẬN ỨNG PHÓ"):
        # Logic tính điểm dựa trên sự lựa chọn
        if "triệt để" in choice:
            st.session_state.do_score = 1.2 # Hệ số nhân lợi nhuận tốt
        elif "chắp vá" in choice:
            st.session_state.do_score = 0.7
        else:
            st.session_state.do_score = 0.4
        st.session_state.step = "Check"
        st.rerun()

# --- STEP 3: CHECK (KIỂM TRA) ---
elif st.session_state.step == "Check":
    st.title("📊 Giai đoạn: CHECK (Kiểm tra)")
    
    # Giả lập kết quả dựa trên logic Plan + Do
    target = st.session_state.kpi_commitment
    actual = int(target * st.session_state.do_score * (random.uniform(0.8, 1.1)))
    
    st.write(f"Mục tiêu cam kết: **{target}%** | Kết quả thực tế: **{actual}%**")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = actual,
        title = {'text': "Hiệu quả cải tiến (%)"},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#001F3F"}}
    ))
    st.plotly_chart(fig)
    
    st.subheader("Phân tích nguyên nhân gốc rễ (5-Whys)")
    why = st.text_area("Tại sao kết quả thực tế lại như vậy? (Phân tích để tìm Action)")
    
    if st.button("HOÀN THÀNH KIỂM TRA"):
        # Tính toán lợi nhuận cuối cùng
        revenue = st.session_state.selected_opt['gain'] * (actual/100)
        st.session_state.profit += revenue
        st.session_state.step = "Action"
        st.rerun()

# --- STEP 4: ACTION (TIÊU CHUẨN HÓA) ---
elif st.session_state.step == "Action":
    st.title("🚀 Giai đoạn: ACTION (Cải tiến & Tiêu chuẩn hóa)")
    
    st.write("Bạn sẽ làm gì để lỗi này không lặp lại (Yokoten)?")
    action_type = st.radio("Chọn hành động tiếp theo:", [
        "Ban hành SOP mới và đào tạo diện rộng (Standardization)",
        "Tiếp tục cải tiến nhỏ (Kaizen) ở công đoạn tiếp theo",
        "Giữ nguyên vì kết quả đã tạm ổn"
    ])
    
    if st.button("TỔNG KẾT DỰ ÁN"):
        st.title("🏆 KẾT QUẢ CUỐI CÙNG")
        st.header(f"Lợi nhuận ròng: {round(st.session_state.profit, 2)} Triệu VNĐ")
        
        if st.session_state.profit > 1100:
            st.success("CHÚC MỪNG! Nhóm đã có tư duy PDCA xuất sắc, mang lại lợi nhuận cao cho KanePackage.")
        else:
            st.warning("CẢNH BÁO: Kế hoạch của bạn chưa tối ưu được chi phí và nguồn lực.")
            
        if st.button("Chơi lại từ đầu"):
            st.session_state.clear()
            st.rerun()