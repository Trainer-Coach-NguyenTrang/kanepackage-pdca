import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# --- CẤU HÌNH GIAO DIỆN QUIET LUXURY ---
st.set_page_config(page_title="KanePackage PDCA Simulation", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E0E0E0; }
    .stButton>button { background-color: #C5A059; color: #0A192F; border-radius: 5px; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #112240; color: #C5A059; border: 1px solid #C5A059; }
    h1, h2, h3 { color: #C5A059; font-family: 'serif'; }
    .status-box { padding: 20px; border-radius: 10px; border: 1px solid #C5A059; background-color: #112240; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO BIẾN TRẠNG THÁI (SESSION STATE) ---
if 'step' not in st.session_state:
    st.session_state.update({
        'step': 'INPUT',
        'qcd_scores': {'Quality': 70, 'Cost': 70, 'Delivery': 70},
        'context': {},
        'plan': {},
        'whys': [],
        'current_why': 1
    })

# --- HELPER FUNCTIONS ---
def update_qcd(q, c, d):
    st.session_state.qcd_scores['Quality'] += q
    st.session_state.qcd_scores['Cost'] += c
    st.session_state.qcd_scores['Delivery'] += d

def render_dashboard():
    df = pd.DataFrame(list(st.session_state.qcd_scores.items()), columns=['Metric', 'Value'])
    fig = px.line_polar(df, r='Value', theta='Metric', line_close=True, range_r=[0,100],
                        color_discrete_sequence=['#C5A059'])
    fig.update_polars(bgcolor="#112240")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E0E0E0")
    st.sidebar.plotly_chart(fig, use_container_width=True)
    st.sidebar.markdown("### 📊 Chỉ số Quản trị Hiện tại")

# --- MAIN FLOW ---
st.title("🏛️ KANEPACKAGE GENBA MANAGEMENT SIMULATION")
st.subheader("Chu trình PDCA: Từ Tư duy đến Thực thi Chiến lược")
render_dashboard()

# --- STAGE 1: INPUT & 5W1H ---
if st.session_state.step == 'INPUT':
    st.header("1. Phân tích Hiện trạng (Genba-Genbutsu-Genzitsu)")
    aspect = st.selectbox("Chọn khía cạnh quản trị cần cải tiến (P-Q-C-D-S-M-E-C):", 
                         ["Productivity", "Quality", "Cost", "Delivery", "Safety", "Morale", "Environment", "Compliance"])
    
    col1, col2 = st.columns(2)
    with col1:
        who = st.text_input("Who: Ai là đối tượng liên quan trực tiếp?")
        where = st.text_input("Where: Vấn đề xảy ra tại công đoạn/vị trí nào?")
        when = st.text_input("When: Tần suất hoặc thời điểm phát sinh?")
    with col2:
        what = st.text_area("What: Mô tả cụ thể hiện tượng (Hiện vật)?")
        why_init = st.text_input("Why: Tại sao đây lại là vấn đề cấp bách?")
        how = st.text_input("How: Hiện trạng đang được xử lý như thế nào?")

    if st.button("Xác nhận bối cảnh 5W1H"):
        if all([who, where, when, what, why_init, how]):
            st.session_state.context = {"aspect": aspect, "what": what, "keywords": what.lower()}
            st.session_state.step = 'PLAN'
            st.rerun()
        else:
            st.error("Vui lòng đảm bảo MECE - Cung cấp đầy đủ thông tin để nắm bắt toàn diện vấn đề.")

# --- STAGE 2: PLAN (SMART & 5W1H2C) ---
elif st.session_state.step == 'PLAN':
    st.header("2. Hoạch định (PLAN)")
    
    st.markdown("### Thiết lập mục tiêu SMART")
    target = st.text_input("Nhập mục tiêu của bạn (Ví dụ: Giảm tỷ lệ lỗi xuống 1% trong 3 tháng):")
    
    if target:
        # Logic đánh giá SMART đơn giản
        checks = {
            "Specific": any(word in target.lower() for word in ["giảm", "tăng", "đạt"]),
            "Measurable": any(char.isdigit() for char in target),
            "Time-bound": any(word in target.lower() for word in ["tháng", "tuần", "ngày", "năm"])
        }
        
        for k, v in checks.items():
            if v: st.success(f"✅ {k}")
            else: st.error(f"❌ {k}: Cần bổ sung dữ liệu cụ thể.")
        
        if all(checks.values()):
            st.markdown("---")
            st.markdown("### Lập kế hoạch 5W1H2C & 5M")
            col1, col2 = st.columns(2)
            with col1:
                method = st.text_input("Method: Phương pháp thực hiện mới là gì?")
                man = st.number_input("Man: Số lượng nhân sự cần thiết?", min_value=1)
                control = st.text_area("Control: Bạn kiểm soát quá trình này như thế nào để đảm bảo đạt mục tiêu?")
            with col2:
                check_kpi = st.text_input("Check (KPI): Bạn nhìn vào chỉ số nào để biết mình thành công?")
                timeline = st.date_input("Thời hạn hoàn thành:", [datetime.now(), datetime.now() + timedelta(days=30)])

            if st.button("Phê duyệt Kế hoạch"):
                st.session_state.plan = {"kpi": check_kpi, "control": control}
                st.session_state.step = 'DO'
                st.rerun()

# --- STAGE 3: DO (BIẾN CỐ & BẪY TƯ DUY) ---
elif st.session_state.step == 'DO':
    st.header("3. Thực hiện & Điều hành (DO)")
    
    # Logic động dựa trên keyword
    event_msg = "Máy móc gặp sự cố bất ngờ!" if "máy" in st.session_state.context['keywords'] else "Nhân sự chủ chốt xin nghỉ đột xuất!"
    
    st.warning(f"⚠️ BIẾN CỐ: {event_msg}")
    st.info(f"Mục tiêu của bạn là: {st.session_state.plan['kpi']}. Bạn sẽ hành động thế nào?")
    
    choice = st.radio("Chọn phương án xử lý:", [
        "Trực tiếp vào làm thay để kịp tiến độ (Firefighting)",
        "Giao cho tổ trưởng tự giải quyết, mình đợi báo cáo (Ủy quyền phó mặc)",
        "Yêu cầu tăng ca bù đắp sản lượng, đào tạo tính sau (Tập trung năng suất)",
        "Dừng lại hiện trường, hướng dẫn Genba và thiết lập Horenso (Manager as Coach)"
    ])

    if st.button("Thực thi quyết định"):
        if "Manager as Coach" in choice:
            st.success("Tuyệt vời! Bạn đã chọn tư duy TPS: Dừng lại để cải tiến.")
            update_qcd(10, -5, 5) # Chất lượng tăng, chi phí tăng nhẹ do dừng máy
        else:
            st.error("Bẫy tư duy! Quyết định này sẽ gây hệ lụy dài hạn cho hệ thống.")
            update_qcd(-10, 10, -5)
        
        st.session_state.step = 'CHECK'
        st.rerun()

# --- STAGE 4: CHECK (5-WHYS) ---
elif st.session_state.step == 'CHECK':
    st.header("4. Kiểm tra & Phân tích Gốc rễ (5-Whys)")
    
    whys_labels = [
        "Hiện tượng: Tại sao sự cố vẫn xảy ra dù có kế hoạch?",
        "Tiêu chuẩn: Tại sao tiêu chuẩn hiện tại không ngăn chặn được?",
        "Ý thức/Kỹ năng: Tại sao nhân viên chưa thực hiện đúng tiêu chuẩn?",
        "Quản lý: Tại sao hệ thống đào tạo/giám sát chưa phát hiện ra lỗ hổng?",
        "Lỗi hệ thống: Gốc rễ nằm ở cơ chế quản trị nào?"
    ]
    
    curr_idx = st.session_state.current_why - 1
    st.markdown(f"**Lớp cắt thứ {st.session_state.current_why}:**")
    ans = st.text_input(whys_labels[curr_idx])
    
    if st.button("Tiếp tục truy vấn"):
        if len(ans) < 10:
            st.warning("Câu trả lời quá hời hợt! Hãy nhìn vào 'Hiện thực' (Genzitsu).")
        else:
            st.session_state.whys.append(ans)
            if st.session_state.current_why < 5:
                st.session_state.current_why += 1
                st.rerun()
            else:
                st.session_state.step = 'ACTION'
                st.rerun()

# --- STAGE 5: ACTION (STANDARDIZATION) ---
elif st.session_state.step == 'ACTION':
    st.header("5. Tiêu chuẩn hóa & Cải tiến (ACTION)")
    st.markdown("### Thiết lập SOP & Yokoten")
    
    sop = st.text_area("Cập nhật SOP: Bạn sẽ thay đổi quy trình làm việc như thế nào để lỗi không lặp lại?")
    yokoten = st.text_area("Lan tỏa (Yokoten): Những bộ phận nào khác tại KanePackage có thể học hỏi từ bài học này?")
    
    if st.button("Hoàn thành chu trình PDCA"):
        st.balloons()
        st.header("📋 BẢN KẾ HOẠCH HÀNH ĐỘNG THỰC CHIẾN")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.subheader("Phân tích Gốc rễ (5-Whys)")
            for i, w in enumerate(st.session_state.whys):
                st.write(f"Why {i+1}: {w}")
        with res_col2:
            st.subheader("Hành động Tiêu chuẩn")
            st.write(f"**SOP mới:** {sop}")
            st.write(f"**Kế hoạch lan tỏa:** {yokoten}")
        
        st.info("Bản kế hoạch này đã sẵn sàng để trình bày tại Genba của KanePackage!")
        if st.button("Chơi lại từ đầu"):
            st.session_state.clear()
            st.rerun()
