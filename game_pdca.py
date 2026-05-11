import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- CẤU HÌNH GIAO DIỆN CHUYÊN NGHIỆP ---
st.set_page_config(page_title="KanePackage Excellence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F0F2F6; }
    .stApp { border-top: 10px solid #001F3F; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); border-left: 5px solid #C5A021; }
    .stButton>button { width: 100%; background-color: #001F3F; color: #C5A021; border: 2px solid #C5A021; font-weight: bold; border-radius: 5px; }
    .stButton>button:hover { background-color: #C5A021; color: white; }
    h1, h2, h3 { color: #001F3F; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO STATE ---
if 'step' not in st.session_state:
    st.session_state.step = "Input"
    st.session_state.qcd = {"Quality": 85, "Cost": 1000, "Delivery": 90}
    st.session_state.history = []
    st.session_state.logs = []

# --- GIAO DIỆN CHỈ SỐ DASHBOARD ---
def display_dashboard():
    st.sidebar.title("🏭 Plant Dashboard")
    st.sidebar.markdown("---")
    st.sidebar.metric("Chỉ số Chất lượng (Q)", f"{st.session_state.qcd['Quality']}%")
    st.sidebar.metric("Ngân sách còn lại (C)", f"{st.session_state.qcd['Cost']}tr")
    st.sidebar.metric("Tỷ lệ Giao hàng (D)", f"{st.session_state.qcd['Delivery']}%")
    st.sidebar.markdown("---")
    st.sidebar.write("**Nhật ký vận hành:**")
    for log in st.session_state.logs[-5:]:
        st.sidebar.caption(log)

# --- STEP 0: INPUT ---
if st.session_state.step == "Input":
    st.title("🛡️ KanePackage: Operational Excellence Challenge")
    st.info("Chào mừng Ban quản lý. Nhà máy đang gặp một vấn đề nghiêm trọng cần giải quyết theo tư duy PDCA.")
    
    problem = st.selectbox("Chọn vấn đề thực tế tại hiện trường:", [
        "Tỷ lệ phế phẩm thùng carton tăng vọt do máy cắt số 4 không ổn định",
        "Tỷ lệ giao hàng muộn (Late Delivery) tăng do quy trình đóng gói thắt nút cổ chai",
        "Tai nạn lao động tiềm ẩn tại khu vực lưu kho nguyên liệu"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Phân tích hiện trạng (Genbutsu)")
        obs = st.text_area("Bạn quan sát được gì tại hiện trường?")
    with col2:
        st.write("### Phân tích nguyên nhân (Why-Why)")
        why = st.text_area("Nguyên nhân gốc rễ theo bạn là gì?")

    if st.button("XÁC NHẬN BỐI CẢNH & BẮT ĐẦU CHU TRÌNH PDCA"):
        st.session_state.problem = problem
        st.session_state.logs.append("Bắt đầu phân tích vấn đề nhà máy.")
        st.session_state.step = "Plan_Detail"
        st.rerun()

# --- STEP 1: PLAN (DEEP DIVE) ---
elif st.session_state.step == "Plan_Detail":
    display_dashboard()
    st.title("📝 Giai đoạn: PLAN (Lập kế hoạch chiến lược)")
    
    tab1, tab2 = st.tabs(["Thiết lập mục tiêu", "Phân bổ nguồn lực"])
    
    with tab1:
        st.write("Dựa trên vấn đề: " + st.session_state.problem)
        st.markdown("> **Yêu cầu:** Thiết lập mục tiêu theo SMART")
        target_q = st.slider("Mục tiêu cải thiện Chất lượng (%)", 0, 100, 95)
        target_d = st.slider("Mục tiêu cải thiện Giao hàng (%)", 0, 100, 98)
    
    with tab2:
        st.write("Phân bổ ngân sách 1000tr vào các hoạt động sau:")
        invest_tech = st.number_input("Đầu tư Máy móc/Kỹ thuật (triệu VNĐ)", 0, 1000, 200)
        invest_human = st.number_input("Đào tạo/Con người (triệu VNĐ)", 0, 1000, 100)
        invest_proc = st.number_input("Cải tiến Quy trình/5S (triệu VNĐ)", 0, 1000, 50)
        
        total = invest_tech + invest_human + invest_proc
        if total > st.session_state.qcd['Cost']:
            st.error(f"Vượt quá ngân sách! Bạn đang sử dụng {total}tr")
        else:
            st.success(f"Ngân sách hợp lệ. Còn lại {st.session_state.qcd['Cost'] - total}tr")

    if st.button("CHỐT KẾ HOẠCH (PLAN)"):
        st.session_state.qcd['Cost'] -= total
        st.session_state.plan_data = {"tech": invest_tech, "human": invest_human, "proc": invest_proc, "target": target_q}
        st.session_state.step = "Do_Simulation"
        st.session_state.logs.append(f"Đã phê duyệt kế hoạch ngân sách {total}tr.")
        st.rerun()

# --- STEP 2: DO (MANAGEMENT SIMULATION) ---
elif st.session_state.step == "Do_Simulation":
    display_dashboard()
    st.title("🛠️ Giai đoạn: DO (Điều hành thực tế)")
    
    st.write("### Nhật ký vận hành 5 ngày cao điểm")
    
    # Giả lập diễn biến
    with st.expander("Xem diễn biến ngày 1 - Ngày 3"):
        st.write("✅ Triển khai lắp đặt thiết bị...")
        time.sleep(0.5)
        st.write("✅ Tổ chức đào tạo công nhân ca sáng...")
        time.sleep(0.5)
        st.write("⚠️ PHÁT SINH: Máy cắt số 4 gặp lỗi cảm biến do bụi bẩn!")

    st.error("🚨 TÌNH HUỐNG KHẨN CẤP: Khách hàng yêu cầu kiểm tra toàn bộ lô hàng vừa sản xuất. Bạn xử lý thế nào?")
    
    decision = st.radio("Quyết định của quản lý:", [
        "Dừng dây chuyền 2 tiếng để tổng kiểm tra (Ưu tiên Chất lượng)",
        "Vừa sản xuất vừa kiểm tra xác suất (Ưu tiên Tiến độ)",
        "Cử nhóm Kaizen xử lý riêng, dây chuyền vẫn chạy (Ưu tiên Hệ thống)"
    ])
    
    if st.button("XÁC NHẬN QUYẾT ĐỊNH ĐIỀU HÀNH"):
        if "Chất lượng" in decision:
            st.session_state.qcd['Quality'] += 10
            st.session_state.qcd['Delivery'] -= 15
        elif "Tiến độ" in decision:
            st.session_state.qcd['Quality'] -= 10
            st.session_state.qcd['Delivery'] += 5
        else:
            st.session_state.qcd['Quality'] += 5
            st.session_state.qcd['Delivery'] += 2
        
        st.session_state.logs.append("Xử lý sự cố máy cắt số 4.")
        st.session_state.step = "Check_Report"
        st.rerun()

# --- STEP 3: CHECK ---
elif st.session_state.step == "Check_Report":
    display_dashboard()
    st.title("📊 Giai đoạn: CHECK (Phân tích hiệu quả)")
    
    # Tính toán kết quả cuối cùng dựa trên các biến số
    final_q = st.session_state.qcd['Quality'] + (st.session_state.plan_data['human'] / 20)
    final_d = st.session_state.qcd['Delivery'] + (st.session_state.plan_data['proc'] / 10)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[
            go.Bar(name='Mục tiêu', x=['Chất lượng', 'Giao hàng'], y=[st.session_state.plan_data['target'], 98], marker_color='#C5A021'),
            go.Bar(name='Thực tế', x=['Chất lượng', 'Giao hàng'], y=[final_q, final_d], marker_color='#001F3F')
        ])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("### Báo cáo kết quả (KPI Report)")
        st.write(f"- Tỷ lệ đạt mục tiêu Chất lượng: {round(final_q/st.session_state.plan_data['target']*100, 1)}%")
        st.write(f"- Hiệu quả sử dụng vốn: {round((final_q + final_d) / (1000 - st.session_state.qcd['Cost']), 2)} điểm")
        
        st.write("---")
        st.write("### Phân tích sai lệch")
        st.text_area("Tại sao có sự chênh lệch giữa Plan và Actual?")

    if st.button("TIẾN TỚI TIÊU CHUẨN HÓA (ACTION)"):
        st.session_state.final_results = {"Q": final_q, "D": final_d}
        st.session_state.step = "Action_Standard"
        st.rerun()

# --- STEP 4: ACTION ---
elif st.session_state.step == "Action_Standard":
    st.title("🚀 Giai đoạn: ACTION (Tiêu chuẩn hóa & Lan tỏa)")
    
    st.write("Để thành quả này bền vững, bạn chọn hành động nào?")
    
    st.checkbox("Cập nhật SOP (Quy trình vận hành tiêu chuẩn) cho máy cắt số 4")
    st.checkbox("Ban hành bảng Check-list 5S hàng ngày cho công nhân")
    st.checkbox("Đưa nội dung đào tạo này vào chương trình hội nhập nhân viên mới")
    
    st.text_area("Ý tưởng Kaizen cho chu kỳ PDCA tiếp theo là gì?")
    
    if st.button("TỔNG KẾT CHIẾN THẮNG"):
        st.balloons()
        st.title("🏆 KẾT QUẢ CUỐI CÙNG")
        score = st.session_state.final_results['Q'] + st.session_state.final_results['D']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng điểm Vận hành", round(score, 1))
        col2.metric("Ngân sách còn dư", f"{st.session_state.qcd['Cost']}tr")
        col3.metric("Xếp hạng", "A (Chuyên gia)" if score > 185 else "B (Quản lý)")
        
        if st.button("Bắt đầu thử thách mới"):
            st.session_state.clear()
            st.rerun()
