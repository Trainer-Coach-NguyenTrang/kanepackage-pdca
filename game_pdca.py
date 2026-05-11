import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="KanePackage Adaptive PDCA", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F6; border-top: 10px solid #001F3F; }
    .stButton>button { border: 2px solid #C5A021; color: #001F3F; font-weight: bold; }
    h1, h2, h3 { color: #001F3F; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO TRẠNG THÁI ---
if 'step' not in st.session_state:
    st.session_state.update({
        'step': "Input",
        'whys': [],
        'why_count': 0,
        'context_keywords': [],
        'user_responses': {}
    })

# --- MÀN HÌNH 1: HIỆN TRƯỜNG (GENBA) ---
if st.session_state.step == "Input":
    st.title("🛡️ KanePackage: Adaptive PDCA Simulation")
    st.subheader("I. HOẠCH ĐỊNH: Nắm bắt hiện trạng [cite: 225, 260]")
    
    domain = st.selectbox("Khía cạnh trọng yếu (P-Q-C-D-S-M-E-C): [cite: 4, 29]", 
                          ["Productivity", "Quality", "Cost", "Delivery", "Safety", "Morale", "Environment", "Compliance"])
    
    st.write("### Nhập mô tả vấn đề chi tiết (Mục tiêu: Làm rõ 5W1H) [cite: 91, 150]")
    problem = st.text_area("Học viên hãy mô tả cụ thể sự việc phát sinh tại hiện trường:", 
                           placeholder="Ví dụ: Công nhân ca chiều thao tác sai máy cắt số 4 gây lỗi mép thùng...")
    
    if st.button("PHÂN TÍCH & LẬP KẾ HOẠCH"):
        if problem:
            # Logic quét từ khóa để cá nhân hóa
            keywords = [w for w in problem.split() if len(w) > 3]
            st.session_state.update({'problem': problem, 'domain': domain, 'context_keywords': keywords, 'step': "Plan"})
            st.rerun()

# --- MÀN HÌNH 2: PLAN (5W1H2C & SMART) ---
elif st.session_state.step == "Plan":
    st.title("📝 Stage: PLAN - Hoạch định khả thi [cite: 164, 171]")
    st.info(f"Vấn đề: {st.session_state.problem}")
    
    st.write("### 1. Thiết lập mục tiêu SMART [cite: 93, 132]")
    goal = st.text_input("Mục tiêu cải thiện cụ thể của bạn là gì?")
    
    st.write("### 2. Kế hoạch hành động 5W1H2C [cite: 110, 157]")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Who: Ai phụ trách thực hiện? [cite: 152]")
        st.text_input("How: Phương pháp thực hiện cụ thể? [cite: 153]")
    with col2:
        st.text_input("Control: Phương pháp kiểm soát là gì? [cite: 154]")
        st.text_input("Check: Chỉ số KPI đo lường? [cite: 155, 237]")

    if st.button("XÁC NHẬN KẾ HOẠCH & TRIỂN KHAI (DO)"):
        st.session_state.goal = goal
        st.session_state.step = "Do"
        st.rerun()

# --- MÀN HÌNH 3: DO (ĐIỀU HÀNH THỰC TẾ) ---
elif st.session_state.step == "Do":
    st.title("🛠️ Stage: DO - Thực hiện & Đào tạo [cite: 174, 180]")
    st.write(f"Đang triển khai kế hoạch cho vấn đề: **{st.session_state.problem}**")
    
    st.error("🚨 BIẾN CỐ: Trong quá trình làm, phát sinh vấn đề ngoài dự kiến liên quan đến nhân sự!")
    
    # Phương án dựa trên "Những lưu ý trong giai đoạn DO" [cite: 202-210]
    choice = st.radio("Lựa chọn đối ứng của người quản lý:", [
        "A. Tạm dừng để trực tiếp hướng dẫn và ủy quyền đào tạo (Tư duy: Đào tạo cấp dưới là đường ngắn nhất) [cite: 207, 208]",
        "B. Ra lệnh yêu cầu làm đúng theo SOP, không cần bàn bạc thêm (Bẫy: Tâm lý 'Bị bắt phải làm') [cite: 160, 206]",
        "C. Tự mình xử lý ngay để kịp tiến độ giao hàng (Bẫy: Người quản lý không đi tiên phong dẫn dắt) [cite: 203]",
        "D. Bỏ qua biến cố nhỏ, tập trung vào KPI cuối ngày (Bẫy: Không tuân thủ 3G tại hiện trường) [cite: 188, 245]"
    ])
    
    if st.button("XÁC NHẬN"):
        st.session_state.do_feedback = choice
        st.session_state.step = "Check"
        st.rerun()

# --- MÀN HÌNH 4: CHECK (5 WHYS ĐỘNG) ---
elif st.session_state.step == "Check":
    st.title("📊 Stage: CHECK - Phân tích tại hiện trường [cite: 238, 241]")
    
    # Hiển thị khoảng cách Gap Analysis [cite: 147, 300]
    st.write(f"Mục tiêu: {st.session_state.goal}")
    st.warning("Thực tế: Kết quả chỉ đạt 70% mục tiêu do phát sinh lỗi hệ thống.")

    # Logic 5 Whys bám sát dữ liệu [cite: 103, 233, 248]
    if st.session_state.why_count < 5:
        # Câu hỏi Why đầu tiên bám vào vấn đề ban đầu
        if st.session_state.why_count == 0:
            current_q = f"Tại sao vấn đề '{st.session_state.problem}' vẫn xảy ra dù đã có kế hoạch?"
        else:
            # Lấy câu trả lời trước đó để hỏi Why tiếp theo
            prev_ans = st.session_state.whys[-1]
            current_q = f"Tại sao bạn cho rằng '{prev_ans}' là nguyên nhân trực tiếp?"

        st.subheader(f"Câu hỏi Why thứ {st.session_state.why_count + 1}:")
        st.info(current_q)
        ans = st.text_input("Nhập phân tích của bạn:", key=f"ans_{st.session_state.why_count}")
        
        if st.button("GỬI PHÂN TÍCH"):
            if ans:
                st.session_state.whys.append(ans)
                st.session_state.why_count += 1
                st.rerun()
    else:
        st.success("Bạn đã hoàn thành 5 tầng Why để tìm nguyên nhân gốc rễ! ")
        if st.button("TIẾN TỚI HÀNH ĐỘNG CẢI TIẾN"):
            st.session_state.step = "Action"
            st.rerun()

# --- MÀN HÌNH 5: ACTION (TIÊU CHUẨN HÓA) ---
elif st.session_state.step == "Action":
    st.title("🚀 Stage: ACTION - Tiêu chuẩn hóa & Cải tiến liên tục [cite: 264, 314]")
    
    st.write("### Các bước cần làm để đóng lại chu trình PDCA: [cite: 78, 265, 273]")
    st.write(f"Nguyên nhân gốc rễ bạn tìm được: **{st.session_state.whys[-1]}**")
    
    st.markdown("""
    1. **Tiêu chuẩn hóa (Standardize):** Cập nhật SOP, đào tạo lại dựa trên nguyên nhân gốc rễ[cite: 78, 312].
    2. **Yokoten:** Chia sẻ bài học thành công/thất bại cho các bộ phận khác[cite: 183, 274].
    3. **Nâng cao tiêu chuẩn:** Đặt mục tiêu cao hơn cho vòng lặp tiếp theo[cite: 313].
    """)
    
    new_standard = st.text_area("Học viên hãy soạn thảo 1 quy định mới để ngăn chặn lỗi này vĩnh viễn:")
    
    if st.button("HOÀN TẤT & ĐÁNH GIÁ"):
        st.balloons()
        st.header("🏆 ĐÁNH GIÁ NĂNG LỰC QUẢN TRỊ")
        # Logic đánh giá bám sát tư duy đào tạo
        if "triệt để" in st.session_state.do_feedback:
            st.success("Bạn có tư duy đào tạo cấp dưới rất tốt! [cite: 207]")
        else:
            st.warning("Bạn cần chú ý tránh bẫy 'tự làm thay' nhân viên. [cite: 203]")
            
        st.write("---")
        st.write("### Chuỗi tư duy 5 Whys của bạn:")
        for i, w in enumerate(st.session_state.whys):
            st.write(f"Bậc {i+1}: {w}")
        
        if st.button("Bắt đầu chu trình PDCA mới"):
            st.session_state.clear()
            st.rerun()
