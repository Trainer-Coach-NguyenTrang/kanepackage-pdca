"""
PDCA Master — KanePackage Vietnam
Management Simulation Game
Designed by Forval Vietnam | Marcella Nguyễn
"""

import streamlit as st
import anthropic
import json
import re
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PDCA Master · KanePackage Vietnam",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS — Minimalist Quiet Luxury
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --navy:   #0A1628;
  --navy2:  #112240;
  --navy3:  #1a3358;
  --gold:   #C9A84C;
  --gold2:  #e8c96a;
  --cream:  #F5F0E8;
  --white:  #FFFFFF;
  --red:    #E05252;
  --green:  #4CAF82;
  --muted:  #8896a8;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background-color: var(--navy);
  color: var(--cream);
}

.stApp { background-color: var(--navy); }

h1, h2, h3 { font-family: 'Playfair Display', serif; color: var(--gold); }

.stage-header {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  color: var(--gold);
  border-bottom: 1px solid var(--gold);
  padding-bottom: 0.4rem;
  margin-bottom: 1.2rem;
}

.card {
  background: var(--navy2);
  border: 1px solid var(--navy3);
  border-radius: 10px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}

.card-gold {
  background: var(--navy2);
  border: 1px solid var(--gold);
  border-radius: 10px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}

.badge {
  display: inline-block;
  background: var(--gold);
  color: var(--navy);
  font-weight: 700;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  padding: 0.18rem 0.7rem;
  border-radius: 20px;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.badge-navy {
  display: inline-block;
  background: var(--navy3);
  color: var(--gold);
  font-weight: 600;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  padding: 0.18rem 0.7rem;
  border-radius: 20px;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.insight {
  background: linear-gradient(135deg, #112240 0%, #1a3358 100%);
  border-left: 3px solid var(--gold);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
  margin: 0.8rem 0;
  font-style: italic;
  color: var(--cream);
  font-size: 0.92rem;
}

.pass-item { color: var(--green); font-size: 0.88rem; margin: 0.3rem 0; }
.fail-item { color: var(--red);   font-size: 0.88rem; margin: 0.3rem 0; }
.muted     { color: var(--muted); font-size: 0.85rem; }

.trap-correct {
  border: 2px solid var(--green) !important;
  background: linear-gradient(135deg, #112240 0%, #0e2b1e 100%) !important;
}
.trap-wrong {
  border: 2px solid var(--red) !important;
  background: linear-gradient(135deg, #112240 0%, #2b0e0e 100%) !important;
}

.score-box {
  text-align: center;
  background: var(--navy2);
  border: 1px solid var(--gold);
  border-radius: 10px;
  padding: 1rem;
}
.score-num {
  font-family: 'Playfair Display', serif;
  font-size: 2.8rem;
  color: var(--gold);
  line-height: 1;
}

hr.divider {
  border: none;
  border-top: 1px solid var(--navy3);
  margin: 1.5rem 0;
}

/* Streamlit overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background-color: var(--navy2) !important;
  border: 1px solid var(--navy3) !important;
  color: var(--cream) !important;
  border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}
.stButton > button {
  background: var(--gold) !important;
  color: var(--navy) !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.5rem 1.6rem !important;
  font-family: 'Inter', sans-serif !important;
  letter-spacing: 0.04em !important;
  transition: all 0.2s;
}
.stButton > button:hover {
  background: var(--gold2) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(201,168,76,0.25) !important;
}
.stRadio > div { background: transparent !important; }
.stRadio label { color: var(--cream) !important; font-size: 0.92rem !important; }
[data-testid="stSidebar"] { background: var(--navy2) !important; }
.stProgress > div > div { background: var(--gold) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
ASPECTS = {
    "P": ("Productivity", "Năng suất"),
    "Q": ("Quality",      "Chất lượng"),
    "C": ("Cost",         "Chi phí"),
    "D": ("Delivery",     "Giao hàng"),
    "S": ("Safety",       "An toàn"),
    "M": ("Morale",       "Tinh thần"),
    "E": ("Environment",  "Môi trường"),
    "CM":("Compliance",   "Tuân thủ"),
}

QUESTIONS_5W1H = {
    "P": [
        ("What",  "Vấn đề năng suất cụ thể là gì? (VD: sản lượng thấp, thời gian cycle time dài…)"),
        ("Why",   "Tại sao bạn xác định đây là vấn đề ưu tiên cần giải quyết ngay?"),
        ("Where", "Vấn đề xảy ra ở công đoạn / dây chuyền / bộ phận nào?"),
        ("Who",   "Những ai liên quan? Ai chịu trách nhiệm chính?"),
        ("When",  "Vấn đề bắt đầu từ khi nào? Có xảy ra theo chu kỳ không?"),
        ("How",   "Hiện tại quy trình đang được thực hiện như thế nào? Có tiêu chuẩn/SOP không?"),
        ("How much", "Tình trạng hiện tại đang ở mức nào? (số liệu cụ thể: %, UPH, tỷ lệ…)"),
    ],
    "Q": [
        ("What",  "Loại lỗi/defect cụ thể là gì? (tên lỗi, mô tả triệu chứng)"),
        ("Why",   "Tại sao lỗi này nghiêm trọng? Ảnh hưởng đến khách hàng/dây chuyền thế nào?"),
        ("Where", "Lỗi phát sinh ở công đoạn nào? Được phát hiện ở đâu?"),
        ("Who",   "Ai vận hành công đoạn đó? Trình độ kỹ năng ra sao?"),
        ("When",  "Lỗi xuất hiện lần đầu khi nào? Tần suất xuất hiện?"),
        ("How",   "Quy trình kiểm soát chất lượng hiện tại là gì? (QC, poka-yoke, SOP…)"),
        ("How much", "Tỷ lệ lỗi / PPM / số lượng cụ thể trong tháng gần nhất là bao nhiêu?"),
    ],
    "C": [
        ("What",  "Chi phí vượt ngân sách ở hạng mục nào? (vật tư, nhân công, năng lượng…)"),
        ("Why",   "Tại sao hạng mục này được xem là chi phí lãng phí cần kiểm soát?"),
        ("Where", "Lãng phí xảy ra ở công đoạn / phòng ban / hoạt động nào?"),
        ("Who",   "Ai quản lý ngân sách hạng mục này? Ai có quyền phê duyệt chi tiêu?"),
        ("When",  "Chi phí tăng bất thường từ thời điểm nào? Có yếu tố mùa vụ không?"),
        ("How",   "Hiện tại đang kiểm soát chi phí bằng phương pháp gì?"),
        ("How much", "Mức độ vượt ngân sách là bao nhiêu? (VNĐ, %, so với kế hoạch)"),
    ],
    "D": [
        ("What",  "Vấn đề giao hàng cụ thể là gì? (trễ deadline, thiếu hàng, sai số lượng…)"),
        ("Why",   "Tại sao việc giao hàng đúng hạn lại quan trọng với KanePackage lúc này?"),
        ("Where", "Giao hàng bị trễ ở khâu nào? (sản xuất, kho, logistics, supplier…)"),
        ("Who",   "Ai chịu trách nhiệm điều phối tiến độ? Ai bị ảnh hưởng trực tiếp?"),
        ("When",  "Trễ hạn xảy ra thường xuyên nhất vào thời điểm nào?"),
        ("How",   "Hiện tại dùng công cụ gì để theo dõi tiến độ? (Kanban, schedule board…)"),
        ("How much", "Tỷ lệ giao hàng đúng hạn (OTD) hiện tại là bao nhiêu %?"),
    ],
    "S": [
        ("What",  "Rủi ro / sự cố an toàn cụ thể là gì? (near-miss, tai nạn, nguy cơ tiềm ẩn…)"),
        ("Why",   "Tại sao rủi ro này được đánh giá mức độ nghiêm trọng cao?"),
        ("Where", "Khu vực / thiết bị / công đoạn nào có rủi ro cao nhất?"),
        ("Who",   "Ai thường xuyên tiếp xúc với rủi ro này? Đã được đào tạo an toàn chưa?"),
        ("When",  "Sự cố / nguy cơ xuất hiện nhiều nhất vào ca nào, thời điểm nào?"),
        ("How",   "Quy trình an toàn hiện tại là gì? Có thực hiện 5S/Kaizen an toàn không?"),
        ("How much", "Số liệu sự cố: bao nhiêu near-miss, bao nhiêu tai nạn trong 3 tháng gần nhất?"),
    ],
    "M": [
        ("What",  "Vấn đề về tinh thần/nhân sự là gì? (nghỉ việc cao, thiếu động lực, xung đột…)"),
        ("Why",   "Tại sao vấn đề này ảnh hưởng đến hiệu quả sản xuất?"),
        ("Where", "Vấn đề tập trung ở bộ phận / nhóm nào? Cấp bậc nào?"),
        ("Who",   "Ai là những nhân viên/nhóm bị ảnh hưởng nhiều nhất?"),
        ("When",  "Vấn đề bắt đầu từ khi nào? Có sự kiện nào khởi phát không?"),
        ("How",   "Hiện tại đang áp dụng biện pháp gì để cải thiện tinh thần nhân viên?"),
        ("How much", "Tỷ lệ nghỉ việc / vắng mặt / điểm engagement survey hiện tại là bao nhiêu?"),
    ],
    "E": [
        ("What",  "Vấn đề môi trường cụ thể là gì? (rác thải, khí thải, tiêu thụ điện/nước…)"),
        ("Why",   "Tại sao đây là vấn đề cần ưu tiên? (pháp lý, chi phí, hình ảnh công ty…)"),
        ("Where", "Nguồn phát sinh / khu vực ảnh hưởng chính là ở đâu?"),
        ("Who",   "Ai chịu trách nhiệm quản lý môi trường? Có bộ phận EHS không?"),
        ("When",  "Vượt chuẩn/phát sinh sự cố môi trường xảy ra vào thời điểm nào?"),
        ("How",   "Hiện tại đang kiểm soát bằng phương pháp gì? Có tuân thủ ISO 14001 không?"),
        ("How much", "Số liệu: lượng rác thải, mức tiêu thụ năng lượng, chỉ số vượt chuẩn cụ thể?"),
    ],
    "CM": [
        ("What",  "Quy định / tiêu chuẩn nào đang bị vi phạm hoặc có nguy cơ không tuân thủ?"),
        ("Why",   "Tại sao việc tuân thủ tiêu chuẩn này là bắt buộc với KanePackage?"),
        ("Where", "Vi phạm xảy ra ở bộ phận / quy trình / hồ sơ nào?"),
        ("Who",   "Ai chịu trách nhiệm đảm bảo tuân thủ? Ai có thẩm quyền kiểm tra?"),
        ("When",  "Vi phạm được phát hiện / báo cáo vào thời điểm nào?"),
        ("How",   "Cơ chế kiểm soát nội bộ hiện tại là gì? Có audit định kỳ không?"),
        ("How much", "Mức độ vi phạm: bao nhiêu lần, hậu quả tài chính/pháp lý ước tính là bao nhiêu?"),
    ],
}

PLAN_QUESTIONS = [
    ("task",       "Nhiệm vụ cụ thể (What)", "Hành động cụ thể này là gì?"),
    ("responsible","Người chịu trách nhiệm (Who)", "Ai là người chịu trách nhiệm thực hiện?"),
    ("start_date", "Ngày bắt đầu (When)", "Dự kiến bắt đầu ngày nào? (VD: 2025-06-01)"),
    ("end_date",   "Ngày kết thúc (When)", "Dự kiến hoàn thành ngày nào? (VD: 2025-06-15)"),
    ("location",   "Địa điểm thực hiện (Where)", "Thực hiện ở đâu? Bộ phận/công đoạn nào?"),
    ("method",     "Phương pháp (How / Method)", "Phương pháp hoặc công cụ nào sẽ được sử dụng?"),
    ("resource_man",   "Nguồn lực: Nhân lực (Man)", "Cần bao nhiêu người? Kỹ năng gì?"),
    ("resource_money", "Nguồn lực: Ngân sách (Money)", "Chi phí ước tính là bao nhiêu?"),
    ("resource_material","Nguồn lực: Vật tư (Material)", "Cần vật tư, nguyên liệu gì?"),
    ("resource_machine", "Nguồn lực: Thiết bị (Machine)", "Cần thiết bị, công cụ gì?"),
    ("control",    "Kiểm soát quá trình (Control)", "Bạn sẽ kiểm soát tiến trình thực hiện như thế nào để đảm bảo không đi lệch hướng?"),
    ("kpi",        "KPI đo lường (Check)", "Nhìn vào chỉ số nào để biết hành động này đã thành công? (số cụ thể, %)"),
]

DO_OPTIONS = [
    {
        "key": "A",
        "label": "🔥 Xử lý trực tiếp — tôi tự làm để đảm bảo tiến độ",
        "trap": True,
        "trap_name": "Bẫy Firefighting",
        "explanation": "Quản lý làm thay nhân viên sẽ giải quyết tạm thời nhưng không phát triển năng lực đội ngũ. Lần sau vẫn xảy ra vấn đề tương tự, và nhân viên sẽ quen với việc 'sếp lo hết'.",
        "qcd_delta": {"quality": -5, "cost": -3, "delivery": +4},
    },
    {
        "key": "B",
        "label": "📋 Giao việc và theo dõi kết quả qua báo cáo cuối ngày",
        "trap": True,
        "trap_name": "Bẫy Ủy quyền phó mặc",
        "explanation": "Giao việc mà không xuống hiện trường kiểm tra thực tế là thiếu 'Tam Hiện'. Báo cáo có thể không phản ánh đúng thực trạng. Vấn đề âm ỉ không được xử lý tận gốc.",
        "qcd_delta": {"quality": -8, "cost": -2, "delivery": -6},
    },
    {
        "key": "C",
        "label": "⏩ Yêu cầu nhân viên tăng tốc — bỏ qua bước training để kịp deadline",
        "trap": True,
        "trap_name": "Bẫy Chạy tiến độ bỏ OJT",
        "explanation": "Tăng tốc mà bỏ đào tạo sẽ tạo ra lỗi chất lượng và rủi ro an toàn về sau. Chi phí sửa lỗi sau này cao hơn nhiều lần chi phí đào tạo ban đầu.",
        "qcd_delta": {"quality": -10, "cost": -1, "delivery": +2},
    },
    {
        "key": "D",
        "label": "🎯 Xuống hiện trường — hướng dẫn trực tiếp và thiết lập HORENSO",
        "trap": False,
        "trap_name": "✅ Manager as Coach",
        "explanation": "Đây là tư duy đúng đắn! Quản lý giỏi biết rằng giải quyết vấn đề TẠI HIỆN TRƯỜNG (Genba), quan sát HIỆN VẬT (Genbutsu) và đối mặt HIỆN THỰC (Genjitsu) mới tạo ra giải pháp bền vững. HORENSO đảm bảo thông tin luôn thông suốt.",
        "qcd_delta": {"quality": +8, "cost": +4, "delivery": +3},
    },
]

WHY_GUIDANCE = {
    1: "Mô tả hiện tượng bề mặt — triệu chứng quan sát được là gì?",
    2: "Tiêu chuẩn/SOP nào đang bị vi phạm hoặc không tồn tại?",
    3: "Kỹ năng và ý thức của người thực hiện có vấn đề gì?",
    4: "Hệ thống quản lý / giám sát hiện tại đang thiếu điều gì?",
    5: "Văn hóa tổ chức và tư duy lãnh đạo ở gốc rễ là gì?",
}

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": 0,
        "api_key": "",
        "aspect": None,
        "ctx_answers": {},
        "ctx_step": 0,
        "keywords": [],
        "smart_goal": "",
        "smart_eval": None,
        "smart_ok": False,
        "smart_attempts": 0,
        "plan_answers": {},
        "plan_step": 0,
        "plan_done": False,
        "gantt_data": [],
        "gantt_generated": False,
        "incident": "",
        "incident_generated": False,
        "do_choice": None,
        "do_revealed": False,
        "why_level": 1,
        "why_answers": {},
        "why_questions": {},
        "std_answers": {},
        "qcd": {"quality": 65, "cost": 70, "delivery": 68},
        "qcd_delta_applied": False,
        "score": 0,
        "plan_score_applied": False,
        "check_score_applied": False,
        "report_md": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
ss = st.session_state

# ─────────────────────────────────────────────
# AI HELPER
# ─────────────────────────────────────────────
def ai(system_prompt: str, user_prompt: str, tokens: int = 800) -> str:
    try:
        client = anthropic.Anthropic(api_key=ss.api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=tokens,
            messages=[{"role": "user", "content": user_prompt}],
            system=system_prompt,
        )
        return msg.content[0].text
    except Exception as e:
        return f"[AI Error: {e}]"


def parse_json(text: str, fallback=None):
    try:
        clean = re.sub(r"```json|```", "", text).strip()
        return json.loads(clean)
    except Exception:
        try:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                return json.loads(m.group())
        except Exception:
            pass
    return fallback if fallback is not None else {}


# ─────────────────────────────────────────────
# QCD DASHBOARD
# ─────────────────────────────────────────────
def render_qcd():
    q = ss.qcd
    cols = st.columns(3)
    labels  = ["Quality", "Cost", "Delivery"]
    vals    = [q["quality"], q["cost"], q["delivery"]]
    colors  = ["#C9A84C", "#4CAF82", "#5B9BD5"]
    for i, col in enumerate(cols):
        with col:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=vals[i],
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": labels[i], "font": {"color": "#C9A84C", "size": 14, "family": "Inter"}},
                number={"suffix": "%", "font": {"color": "#F5F0E8", "size": 22}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#8896a8", "tickfont": {"color": "#8896a8", "size": 9}},
                    "bar":  {"color": colors[i], "thickness": 0.3},
                    "bgcolor": "#112240",
                    "bordercolor": "#1a3358",
                    "steps": [
                        {"range": [0,  50], "color": "#1e0e0e"},
                        {"range": [50, 75], "color": "#1e1a0e"},
                        {"range": [75, 100],"color": "#0e1e14"},
                    ],
                    "threshold": {
                        "line": {"color": "#C9A84C", "width": 2},
                        "thickness": 0.75,
                        "value": 80,
                    },
                },
            ))
            fig.update_layout(
                height=180, margin=dict(l=10, r=10, t=40, b=5),
                paper_bgcolor="#112240", font_color="#F5F0E8",
            )
            st.plotly_chart(fig, use_container_width=True, key=f"qcd_{labels[i]}_{vals[i]}")


# ─────────────────────────────────────────────
# PROGRESS BAR
# ─────────────────────────────────────────────
STAGE_NAMES = ["Chào mừng", "Chọn Khía cạnh", "Phân tích 5W1H",
               "Mục tiêu SMART", "Lập Kế hoạch", "Giai đoạn DO",
               "Phân tích CHECK", "Hành động ACTION", "Kết quả"]

def render_progress():
    if ss.stage == 0:
        return
    pct = ss.stage / (len(STAGE_NAMES) - 1)
    st.progress(pct)
    cols = st.columns(len(STAGE_NAMES) - 1)
    for i, name in enumerate(STAGE_NAMES[1:], 1):
        with cols[i-2] if i > 1 else cols[0]:
            color = "#C9A84C" if i <= ss.stage else "#8896a8"
            st.markdown(f"<div style='text-align:center;font-size:0.65rem;color:{color};'>{name}</div>",
                        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# STAGE 0 — WELCOME
# ─────────────────────────────────────────────────────
def stage_welcome():
    st.markdown("""
<div style='text-align:center; padding: 3rem 1rem 1rem;'>
  <div style='font-size:3.5rem; margin-bottom:0.5rem;'>⚙️</div>
  <h1 style='font-family:Playfair Display,serif; color:#C9A84C; font-size:2.8rem; letter-spacing:0.05em;'>
    PDCA MASTER
  </h1>
  <div style='color:#8896a8; font-size:1rem; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem;'>
    Management Simulation · KanePackage Vietnam
  </div>
  <div style='color:#F5F0E8; font-size:0.95rem; max-width:560px; margin:1.2rem auto; line-height:1.8;'>
    Trải nghiệm chu trình PDCA thực chiến — từ phân tích hiện trạng, lập kế hoạch,<br>
    xử lý tình huống đến tiêu chuẩn hóa bền vững tại nhà máy.
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="card-gold">', unsafe_allow_html=True)
        st.markdown('<div class="badge">Bắt đầu</div>', unsafe_allow_html=True)
        st.markdown("**Nhập Anthropic API Key của bạn để kích hoạt AI:**")
        key_input = st.text_input("API Key", type="password", placeholder="sk-ant-...",
                                   key="api_key_input", label_visibility="collapsed")
        st.markdown('<p class="muted">API key chỉ dùng trong phiên này, không được lưu trữ.</p>',
                    unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀  Bắt đầu Game", use_container_width=True):
                if key_input.strip():
                    ss.api_key = key_input.strip()
                    ss.stage = 1
                    st.rerun()
                else:
                    st.error("Vui lòng nhập API key.")
        with col_b:
            if st.button("▶  Demo (không AI)", use_container_width=True):
                ss.api_key = "demo"
                ss.stage = 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
<div style='text-align:center; margin-top:2rem;'>
  <div style='display:inline-flex; gap:2rem; color:#8896a8; font-size:0.82rem;'>
    <span>🎯 Mục tiêu SMART</span>
    <span>📋 Kế hoạch Gantt</span>
    <span>⚡ Tình huống thực chiến</span>
    <span>🔍 5 Whys chuyên sâu</span>
    <span>📄 Action Plan xuất file</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# STAGE 1 — ASPECT SELECTION
# ─────────────────────────────────────────────────────
def stage_aspect():
    st.markdown('<div class="stage-header">① Chọn Khía Cạnh Quản Trị</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight">Mỗi buổi PDCA bắt đầu từ việc xác định rõ <strong>bạn đang giải quyết vấn đề gì</strong>. Hãy chọn khía cạnh phản ánh đúng nhất thách thức hiện tại tại KanePackage.</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (code, (en, vn)) in enumerate(ASPECTS.items()):
        with cols[i % 4]:
            selected = ss.aspect == code
            border = "#C9A84C" if selected else "#1a3358"
            bg     = "linear-gradient(135deg,#112240,#1a3358)" if selected else "#112240"
            st.markdown(f"""
<div style='background:{bg};border:2px solid {border};border-radius:10px;
     padding:1rem;text-align:center;margin-bottom:0.8rem;cursor:pointer;'>
  <div style='font-size:1.8rem;'>{["📊","🎯","💰","🚚","🦺","🧑‍🤝‍🧑","🌿","📋"][i]}</div>
  <div style='color:#C9A84C;font-weight:700;font-size:0.95rem;'>{code} — {vn}</div>
  <div style='color:#8896a8;font-size:0.75rem;'>{en}</div>
</div>""", unsafe_allow_html=True)
            if st.button(f"Chọn {code}", key=f"asp_{code}", use_container_width=True):
                ss.aspect = code
                st.rerun()

    if ss.aspect:
        st.markdown(f"""
<div class="card-gold" style='margin-top:1rem;'>
  <div class='badge'>Đã chọn</div>
  <strong style='color:#C9A84C;'>
    {ss.aspect} — {ASPECTS[ss.aspect][1]} ({ASPECTS[ss.aspect][0]})
  </strong><br>
  <span class='muted'>Nhấn "Tiếp theo" để phân tích hiện trạng bằng 5W1H</span>
</div>""", unsafe_allow_html=True)
        if st.button("Tiếp theo →  Phân tích 5W1H", use_container_width=False):
            ss.stage = 2
            ss.ctx_step = 0
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 2 — 5W1H CONTEXT
# ─────────────────────────────────────────────────────
def stage_5w1h():
    aspect = ss.aspect
    qs = QUESTIONS_5W1H[aspect]
    total = len(qs)
    step  = ss.ctx_step

    st.markdown('<div class="stage-header">② Phân Tích Hiện Trạng — 5W1H</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight">Phân tích MECE cho khía cạnh <strong>{ASPECTS[aspect][1]}</strong>. Trả lời chi tiết giúp AI cá nhân hóa các giai đoạn PLAN, DO, CHECK cho bối cảnh thực tế của bạn.</div>', unsafe_allow_html=True)

    st.progress((step) / total)
    st.markdown(f'<p class="muted">Câu hỏi {min(step+1, total)} / {total}</p>', unsafe_allow_html=True)

    if step < total:
        wh, question = qs[step]
        st.markdown(f'<div class="card-gold"><div class="badge">{wh}</div><br><strong style="font-size:1.05rem;">{question}</strong></div>', unsafe_allow_html=True)

        prev_val = ss.ctx_answers.get(f"q{step}", "")
        answer = st.text_area("Câu trả lời của bạn:", value=prev_val, height=100,
                               key=f"ctx_{step}", placeholder="Mô tả chi tiết, càng cụ thể càng tốt…")

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("→ Tiếp", key=f"ctx_next_{step}"):
                if answer.strip():
                    ss.ctx_answers[f"q{step}"] = answer.strip()
                    ss.ctx_step += 1
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập câu trả lời trước khi tiếp tục.")
    else:
        # All answered — extract keywords
        st.markdown('<div class="card"><div class="badge">✅ Hoàn thành 5W1H</div><br><strong>Tổng hợp thông tin hiện trạng:</strong></div>', unsafe_allow_html=True)
        for i, (wh, q) in enumerate(qs):
            ans = ss.ctx_answers.get(f"q{i}", "")
            st.markdown(f'<p style="margin:0.3rem 0;"><span class="badge-navy">{wh}</span> <span style="color:#F5F0E8;">{ans}</span></p>', unsafe_allow_html=True)

        if not ss.keywords:
            with st.spinner("Đang trích xuất từ khóa…"):
                ctx_text = "\n".join([f"{qs[i][0]}: {ss.ctx_answers.get(f'q{i}','')}" for i in range(total)])
                raw = ai(
                    "Bạn là chuyên gia phân tích sản xuất Nhật Bản. Trích xuất 5-8 từ khóa QUAN TRỌNG NHẤT từ mô tả vấn đề dưới đây. Chỉ trả về JSON array: [\"từ khóa 1\", \"từ khóa 2\", ...]. Không giải thích thêm.",
                    f"Khía cạnh: {ASPECTS[aspect][1]}\n{ctx_text}"
                )
                keywords = parse_json(raw, fallback=[])
                if not keywords:
                    keywords = [w for w in ctx_text.split() if len(w) > 4][:6]
                ss.keywords = keywords

        st.markdown(f'<div class="card"><strong>Từ khóa đã trích xuất:</strong><br>{"  ".join([f"<span class=badge-navy>{k}</span>" for k in ss.keywords])}</div>', unsafe_allow_html=True)

        if st.button("Tiếp theo →  Thiết lập Mục tiêu SMART"):
            ss.stage = 3
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 3 — SMART GOAL
# ─────────────────────────────────────────────────────
def eval_smart(goal: str) -> dict:
    ctx_summary = "; ".join([f"{QUESTIONS_5W1H[ss.aspect][i][0]}: {v}" for i, v in ss.ctx_answers.items()])
    raw = ai(
        """Bạn là chuyên gia đào tạo quản lý sản xuất theo chuẩn SMART. Đánh giá mục tiêu sau và trả về JSON duy nhất (không text ngoài JSON):
{
  "S": {"pass": true/false, "comment": "nhận xét cụ thể bằng tiếng Việt, tối đa 1 câu"},
  "M": {"pass": true/false, "comment": "..."},
  "A": {"pass": true/false, "comment": "..."},
  "R": {"pass": true/false, "comment": "..."},
  "T": {"pass": true/false, "comment": "..."},
  "overall": true/false,
  "tip": "1 lời khuyên cụ thể để cải thiện nếu chưa đạt"
}
Tiêu chí:
S=Specific (cụ thể, rõ chỉ số, địa điểm, đối tượng)
M=Measurable (có con số đo lường được)
A=Achievable (thực tế, phù hợp nguồn lực)
R=Relevant (liên quan trực tiếp đến vấn đề đã nêu)
T=Time-bound (có deadline rõ ràng)""",
        f"Vấn đề: {ctx_summary}\nMục tiêu cần đánh giá: {goal}"
    )
    return parse_json(raw, fallback={
        "S": {"pass": False, "comment": "Cần thêm thông tin cụ thể"},
        "M": {"pass": False, "comment": "Cần có số liệu đo lường"},
        "A": {"pass": False, "comment": "Cần xem xét tính khả thi"},
        "R": {"pass": False, "comment": "Cần liên hệ rõ với vấn đề"},
        "T": {"pass": False, "comment": "Cần có thời hạn cụ thể"},
        "overall": False, "tip": "Hãy thêm con số cụ thể và thời hạn rõ ràng."
    })


def stage_smart():
    st.markdown('<div class="stage-header">③ Thiết lập Mục Tiêu SMART</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight">Một bản kế hoạch chỉ có ý nghĩa khi người quản lý suy nghĩ cặn kẽ đến mức <strong>"có cảm giác sẽ làm được"</strong>. Bắt đầu từ mục tiêu SMART — nền tảng của mọi hành động.</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<strong>Công thức SMART:</strong><br>
<span class="badge-navy">S</span> Specific — Cụ thể &nbsp;
<span class="badge-navy">M</span> Measurable — Đo lường được &nbsp;
<span class="badge-navy">A</span> Achievable — Khả thi &nbsp;
<span class="badge-navy">R</span> Relevant — Liên quan &nbsp;
<span class="badge-navy">T</span> Time-bound — Có thời hạn
</div>""", unsafe_allow_html=True)

    prev_goal = ss.smart_goal
    goal = st.text_area(
        "Nhập mục tiêu của bạn:",
        value=prev_goal, height=110,
        placeholder='VD: "Giảm tỷ lệ lỗi sản phẩm tại chuyền A từ 4.2% xuống dưới 2% trong vòng 8 tuần (kết thúc 30/06/2025) bằng cách áp dụng SOP mới và OJT cho 3 công nhân vận hành."',
        key="smart_input"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        evaluate = st.button("🔍 Đánh giá SMART", key="eval_smart_btn")

    if evaluate and goal.strip():
        ss.smart_goal = goal.strip()
        ss.smart_attempts += 1
        with st.spinner("Đang đánh giá mục tiêu…"):
            ss.smart_eval = eval_smart(goal.strip())
        st.rerun()

    if ss.smart_eval:
        ev = ss.smart_eval
        all_pass = all(ev.get(c, {}).get("pass", False) for c in ["S","M","A","R","T"])
        ss.smart_ok = all_pass

        st.markdown(f'<div class="{"card-gold" if all_pass else "card"}"><strong>Kết quả đánh giá SMART (lần {ss.smart_attempts}):</strong></div>', unsafe_allow_html=True)
        for criterion in ["S", "M", "A", "R", "T"]:
            data = ev.get(criterion, {})
            passed = data.get("pass", False)
            icon   = "✅" if passed else "❌"
            css    = "pass-item" if passed else "fail-item"
            names  = {"S":"Specific","M":"Measurable","A":"Achievable","R":"Relevant","T":"Time-bound"}
            st.markdown(f'<p class="{css}">{icon} <strong>{criterion} — {names[criterion]}:</strong> {data.get("comment","")}</p>', unsafe_allow_html=True)

        if all_pass:
            st.markdown('<div class="card-gold"><strong style="color:#4CAF82;">🎉 Mục tiêu đạt chuẩn SMART!</strong> Bạn có thể tiếp tục lập kế hoạch hành động.</div>', unsafe_allow_html=True)
            if not ss.plan_score_applied:
                ss.score += 20
                ss.plan_score_applied = True
            if st.button("Tiếp theo →  Lập Kế hoạch 5W1H2C"):
                ss.stage = 4
                st.rerun()
        else:
            tip = ev.get("tip", "")
            st.markdown(f'<div class="insight">💡 <strong>Gợi ý cải thiện:</strong> {tip}</div>', unsafe_allow_html=True)
            st.warning("Một số tiêu chí chưa đạt. Hãy chỉnh sửa mục tiêu và đánh giá lại.")


# ─────────────────────────────────────────────────────
# STAGE 4 — ACTION PLAN + GANTT
# ─────────────────────────────────────────────────────
def build_gantt(plan: dict) -> list:
    plan_text = json.dumps(plan, ensure_ascii=False)
    raw = ai(
        """Bạn là chuyên gia lập kế hoạch sản xuất. Từ thông tin kế hoạch hành động dưới đây, hãy tạo danh sách các task cho Gantt Chart. Chỉ trả về JSON array (không text ngoài):
[{"task":"tên task ngắn gọn","start":"YYYY-MM-DD","end":"YYYY-MM-DD","responsible":"tên người","category":"Planning/Execution/Control"}]
Tạo 5-7 task logic, có thứ tự thời gian hợp lý. Nếu ngày không rõ, suy luận từ thông tin có sẵn.""",
        f"Kế hoạch: {plan_text}"
    )
    tasks = parse_json(raw, fallback=[])
    if not tasks:
        today = datetime.today()
        tasks = [
            {"task": "Khảo sát hiện trạng",   "start": today.strftime("%Y-%m-%d"), "end": (today+timedelta(days=3)).strftime("%Y-%m-%d"),  "responsible": plan.get("responsible","PM"), "category":"Planning"},
            {"task": "Lập SOP mới",            "start": (today+timedelta(days=4)).strftime("%Y-%m-%d"), "end": (today+timedelta(days=7)).strftime("%Y-%m-%d"), "responsible": plan.get("responsible","PM"), "category":"Planning"},
            {"task": "OJT đào tạo nhân viên",  "start": (today+timedelta(days=8)).strftime("%Y-%m-%d"), "end": (today+timedelta(days=14)).strftime("%Y-%m-%d"),"responsible": plan.get("responsible","PM"), "category":"Execution"},
            {"task": "Triển khai thực tế",     "start": (today+timedelta(days=10)).strftime("%Y-%m-%d"),"end": (today+timedelta(days=20)).strftime("%Y-%m-%d"),"responsible": plan.get("responsible","PM"), "category":"Execution"},
            {"task": "Đo lường KPI",           "start": (today+timedelta(days=21)).strftime("%Y-%m-%d"),"end": (today+timedelta(days=25)).strftime("%Y-%m-%d"),"responsible": plan.get("responsible","PM"), "category":"Control"},
            {"task": "Đánh giá & Điều chỉnh",  "start": (today+timedelta(days=25)).strftime("%Y-%m-%d"),"end": (today+timedelta(days=30)).strftime("%Y-%m-%d"),"responsible": plan.get("responsible","PM"), "category":"Control"},
        ]
    return tasks


def render_gantt(tasks: list):
    if not tasks:
        return
    df = pd.DataFrame(tasks)
    for col in ["start","end"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df = df.dropna(subset=["start","end"])
    if df.empty:
        st.warning("Không thể vẽ Gantt Chart.")
        return

    cat_colors = {"Planning":"#C9A84C","Execution":"#4CAF82","Control":"#5B9BD5"}
    fig = px.timeline(
        df, x_start="start", x_end="end", y="task", color="category",
        color_discrete_map=cat_colors,
        labels={"task":"","category":"Giai đoạn"},
        hover_data={"responsible": True},
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        paper_bgcolor="#112240", plot_bgcolor="#0A1628",
        font_color="#F5F0E8", font_family="Inter",
        title=dict(text="📊 Gantt Chart — Kế Hoạch Thực Thi", font=dict(color="#C9A84C", size=15)),
        xaxis=dict(gridcolor="#1a3358", tickcolor="#8896a8"),
        yaxis=dict(gridcolor="#1a3358"),
        legend=dict(bgcolor="#112240", bordercolor="#1a3358"),
        height=320,
        margin=dict(l=10, r=10, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def stage_plan():
    st.markdown('<div class="stage-header">④ Lập Kế Hoạch Hành Động — 5W1H2C + 5M</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight">Mục tiêu SMART chỉ là đích đến. <strong>5W1H2C</strong> là bản đồ hành trình: bạn cần biết <em>Ai làm gì, ở đâu, khi nào, bằng cách nào</em> — và quan trọng hơn là <em>kiểm soát & đo lường bằng chỉ số gì</em>.</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card"><span class="badge">SMART Goal</span><br><em style="color:#C9A84C;">{ss.smart_goal}</em></div>', unsafe_allow_html=True)

    step  = ss.plan_step
    total = len(PLAN_QUESTIONS)

    if step < total and not ss.plan_done:
        st.progress(step / total)
        st.markdown(f'<p class="muted">Câu hỏi {step+1} / {total}</p>', unsafe_allow_html=True)

        key_name, label, question = PLAN_QUESTIONS[step]
        st.markdown(f'<div class="card-gold"><div class="badge">{label}</div><br><strong>{question}</strong></div>', unsafe_allow_html=True)

        prev = ss.plan_answers.get(key_name, "")
        ans  = st.text_area("Câu trả lời:", value=prev, height=90,
                             key=f"pa_{step}", placeholder="Trả lời cụ thể…")

        c1, c2 = st.columns([1, 6])
        with c1:
            if st.button("→ Tiếp", key=f"plan_next_{step}"):
                if ans.strip():
                    ss.plan_answers[key_name] = ans.strip()
                    ss.plan_step += 1
                    st.rerun()
                else:
                    st.warning("Vui lòng điền câu trả lời.")
    else:
        ss.plan_done = True
        st.markdown('<div class="card"><div class="badge">✅ Kế hoạch đã hoàn chỉnh</div></div>', unsafe_allow_html=True)
        for _, label, _ in PLAN_QUESTIONS:
            key_n = PLAN_QUESTIONS[[x[1] for x in PLAN_QUESTIONS].index(label)][0]
            val   = ss.plan_answers.get(key_n, "—")
            st.markdown(f'<p style="margin:0.3rem 0;"><span class="badge-navy">{label}</span> <span style="color:#F5F0E8;font-size:0.88rem;">{val}</span></p>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if not ss.gantt_generated:
            with st.spinner("Đang tạo Gantt Chart…"):
                ss.gantt_data = build_gantt(ss.plan_answers)
                ss.gantt_generated = True

        render_gantt(ss.gantt_data)

        st.markdown('<div class="insight">📌 <strong>Thông điệp quản lý:</strong> Kế hoạch tốt nhất là kế hoạch mà người thực hiện hiểu rõ đến mức họ tự tin nói: "Tôi biết mình phải làm gì ngay ngày mai." Gantt Chart là công cụ giao tiếp, không phải bùa hộ mệnh.</div>', unsafe_allow_html=True)

        # Update QCD
        if not ss.qcd_delta_applied:
            ss.qcd["quality"]  = min(100, ss.qcd["quality"]  + 5)
            ss.qcd["cost"]     = min(100, ss.qcd["cost"]     + 3)
            ss.qcd["delivery"] = min(100, ss.qcd["delivery"] + 4)
            ss.qcd_delta_applied = True

        if st.button("Tiếp theo →  Giai đoạn DO"):
            ss.stage = 5
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 5 — DO
# ─────────────────────────────────────────────────────
def generate_incident() -> str:
    ctx = "\n".join([f"{QUESTIONS_5W1H[ss.aspect][i][0]}: {v}" for i, v in ss.ctx_answers.items()])
    kw  = ", ".join(ss.keywords)
    raw = ai(
        """Bạn là chuyên gia mô phỏng quản trị sản xuất. Tạo ra một BIẾN CỐ bất ngờ (50-80 từ tiếng Việt) xảy ra trong quá trình thực hiện kế hoạch. Biến cố phải:
1. Liên quan trực tiếp đến từ khóa và vấn đề đã mô tả
2. Có thể là sự cố kỹ thuật, vấn đề nhân sự, hoặc áp lực từ bên ngoài
3. Tạo ra áp lực thực sự, buộc người quản lý phải ra quyết định ngay
4. Viết dưới dạng thông báo khẩn từ tổ trưởng/nhân viên
Chỉ trả về đoạn văn mô tả biến cố, không tiêu đề, không giải thích.""",
        f"Khía cạnh: {ASPECTS[ss.aspect][1]}\nTừ khóa: {kw}\nBối cảnh: {ctx}\nMục tiêu SMART: {ss.smart_goal}"
    )
    return raw.strip()


def stage_do():
    st.markdown('<div class="stage-header">⑤ Giai Đoạn DO — Thực Hiện & Điều Hành</div>', unsafe_allow_html=True)

    if not ss.incident_generated:
        with st.spinner("Đang tạo tình huống thực chiến…"):
            ss.incident = generate_incident()
            ss.incident_generated = True

    st.markdown(f"""
<div class="card-gold">
  <div class="badge">⚡ Biến cố bất ngờ</div><br>
  <p style="font-size:1.02rem; line-height:1.8; color:#F5F0E8;">{ss.incident}</p>
</div>""", unsafe_allow_html=True)

    st.markdown("**Bạn — với tư cách quản lý — sẽ phản ứng thế nào?**")
    st.markdown('<p class="muted">Hãy chọn phương án phản ánh đúng nhất cách bạn xử lý tình huống này:</p>', unsafe_allow_html=True)

    if not ss.do_revealed:
        choice = st.radio(
            "Lựa chọn của bạn:",
            options=[opt["key"] for opt in DO_OPTIONS],
            format_func=lambda k: next(o["label"] for o in DO_OPTIONS if o["key"] == k),
            key="do_radio",
        )
        if st.button("✅  Xác nhận lựa chọn"):
            ss.do_choice   = choice
            ss.do_revealed = True

            # Apply QCD delta
            delta = next(o["qcd_delta"] for o in DO_OPTIONS if o["key"] == choice)
            for k, v in delta.items():
                ss.qcd[k] = max(0, min(100, ss.qcd[k] + v))

            # Score
            if choice == "D":
                ss.score += 30
            else:
                ss.score += 10
            st.rerun()
    else:
        selected = next(o for o in DO_OPTIONS if o["key"] == ss.do_choice)
        is_correct = not selected["trap"]
        css_class  = "trap-correct" if is_correct else "trap-wrong"
        icon       = "✅" if is_correct else "❌"

        st.markdown(f"""
<div class="card {css_class}">
  <div class="badge">{'✅ Phương án tối ưu' if is_correct else '⚠️ ' + selected['trap_name']}</div>
  <div style="margin: 0.5rem 0;">
    <strong>{icon} {selected['label']}</strong>
  </div>
  <p style="color:#F5F0E8; line-height:1.7; font-size:0.92rem;">{selected['explanation']}</p>
</div>""", unsafe_allow_html=True)

        if not is_correct:
            correct_opt = next(o for o in DO_OPTIONS if not o["trap"])
            st.markdown(f"""
<div class="card trap-correct">
  <div class="badge">💡 Phương án tối ưu là</div>
  <strong>{correct_opt['label']}</strong>
  <p style="color:#F5F0E8; font-size:0.88rem; line-height:1.7;">{correct_opt['explanation']}</p>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="insight">
  <strong>Triết lý Tam Hiện (三現主義):</strong><br>
  🏭 <strong>Genba</strong> (現場) — Đến hiện trường &nbsp;|&nbsp;
  👁 <strong>Genbutsu</strong> (現物) — Quan sát hiện vật &nbsp;|&nbsp;
  📊 <strong>Genjitsu</strong> (現実) — Đối mặt hiện thực
</div>""", unsafe_allow_html=True)

        if st.button("Tiếp theo →  Phân tích CHECK (5 Whys)"):
            ss.stage = 6
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 6 — CHECK / 5 WHYS
# ─────────────────────────────────────────────────────
def make_why_question(level: int, prev_answer: str) -> str:
    guidance = WHY_GUIDANCE.get(level, "")
    context  = f"Vấn đề gốc: {ss.incident}\nTừ khóa: {', '.join(ss.keywords)}\nMục tiêu: {ss.smart_goal}"
    prev_why_text = ""
    for lvl in range(1, level):
        q = ss.why_questions.get(lvl, "")
        a = ss.why_answers.get(lvl, "")
        if q and a:
            prev_why_text += f"Why {lvl}: {q}\nTrả lời: {a}\n"

    raw = ai(
        f"""Bạn là chuyên gia 5 Whys khắt khe theo chuẩn TPS/Lean của Toyota. Nhiệm vụ: đặt câu hỏi "Tại sao?" thứ {level} dựa trên câu trả lời trước đó. 
Mục tiêu phân tích tầng {level}: {guidance}
Quy tắc:
- Câu hỏi phải trực tiếp đi sâu hơn câu trả lời trước
- Phong cách: chuyên gia nghiêm khắc nhưng xây dựng
- Dài tối đa 1-2 câu
- Nếu câu trả lời trước hời hợt (ví dụ "do lười", "do không biết"), hãy truy vấn ngay vào hệ thống: "Vậy tại sao hệ thống [tuyển dụng/đào tạo/giám sát] lại để điều đó xảy ra?"
Chỉ trả về câu hỏi, không giải thích.""",
        f"{context}\n{prev_why_text}Câu trả lời Why {level-1}: {prev_answer}"
    )
    return raw.strip()


def stage_check():
    st.markdown('<div class="stage-header">⑥ Giai Đoạn CHECK — Phân Tích 5 Whys</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight">"Hỏi Tại sao? không phải để đổ lỗi, mà để <strong>tìm gốc rễ</strong> — nơi duy nhất mà sự thay đổi thực sự có thể xảy ra." — Taiichi Ohno, Toyota</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card"><span class="badge">Vấn đề</span> {ss.incident}</div>', unsafe_allow_html=True)

    level     = ss.why_level
    MAX_LEVEL = 5

    # Show history
    for lvl in range(1, level):
        q = ss.why_questions.get(lvl, "")
        a = ss.why_answers.get(lvl, "")
        if q:
            st.markdown(f"""
<div class="card" style="margin-bottom:0.4rem;">
  <span class="badge-navy">Why {lvl}</span>
  <span style="color:#8896a8; font-size:0.85rem;"> — {WHY_GUIDANCE.get(lvl,'')}</span><br>
  <strong style="color:#C9A84C;">{q}</strong><br>
  <span style="color:#F5F0E8; font-size:0.88rem;">→ {a}</span>
</div>""", unsafe_allow_html=True)

    if level <= MAX_LEVEL:
        st.progress(level / (MAX_LEVEL + 1))

        # Generate question if needed
        if level not in ss.why_questions:
            with st.spinner(f"Đang phân tích Why {level}…"):
                if level == 1:
                    prev_ans = f"Biến cố: {ss.incident}"
                else:
                    prev_ans = ss.why_answers.get(level - 1, "")
                ss.why_questions[level] = make_why_question(level, prev_ans)

        q = ss.why_questions[level]
        st.markdown(f"""
<div class="card-gold">
  <span class="badge">Why {level} / {MAX_LEVEL}</span>
  <span style="color:#8896a8; font-size:0.82rem;"> — {WHY_GUIDANCE.get(level,'')}</span><br>
  <strong style="font-size:1.05rem; color:#F5F0E8;">{q}</strong>
</div>""", unsafe_allow_html=True)

        prev_ans = ss.why_answers.get(level, "")
        answer   = st.text_area(f"Câu trả lời Why {level}:", value=prev_ans, height=90,
                                 key=f"why_{level}", placeholder="Phân tích sâu, đừng dừng ở hiện tượng bề mặt…")

        c1, c2 = st.columns([1, 6])
        with c1:
            if st.button(f"→ Why {level+1}" if level < MAX_LEVEL else "→ Kết luận", key=f"why_next_{level}"):
                if answer.strip():
                    ss.why_answers[level] = answer.strip()
                    ss.why_level = level + 1
                    if not ss.check_score_applied:
                        ss.score += 8
                    st.rerun()
                else:
                    st.warning("Hãy phân tích kỹ trước khi tiếp tục.")
    else:
        # All 5 done
        if not ss.check_score_applied:
            ss.score += 8  # last level
            ss.check_score_applied = True

        # Generate root cause summary
        why_text = "\n".join([f"Why {l}: Q: {ss.why_questions.get(l,'')} | A: {ss.why_answers.get(l,'')}" for l in range(1,6)])
        if "root_cause_summary" not in ss:
            with st.spinner("Đang tổng hợp nguyên nhân gốc rễ…"):
                rc = ai(
                    "Bạn là chuyên gia TPS. Tóm tắt nguyên nhân gốc rễ từ phân tích 5 Whys dưới đây thành 2-3 câu ngắn gọn, súc tích. Xác định rõ: (1) Nguyên nhân gốc rễ chính, (2) Cấp độ thất bại (vận hành/quy trình/hệ thống quản lý). Trả lời bằng tiếng Việt.",
                    why_text
                )
                ss["root_cause_summary"] = rc.strip()

        st.markdown(f"""
<div class="card-gold">
  <div class="badge">🎯 Nguyên nhân gốc rễ</div>
  <p style="color:#F5F0E8; line-height:1.8;">{ss.get('root_cause_summary','')}</p>
</div>""", unsafe_allow_html=True)

        # Update QCD
        ss.qcd["quality"] = min(100, ss.qcd["quality"] + 5)

        st.markdown('<div class="insight">✅ Bạn đã hoàn thành phân tích 5 Whys. Nguyên nhân gốc rễ là nền tảng để xây dựng hành động ACTION bền vững — không phải chỉ "vá víu" mà là thay đổi hệ thống.</div>', unsafe_allow_html=True)

        if st.button("Tiếp theo →  Giai đoạn ACTION"):
            ss.stage = 7
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 7 — ACTION (STANDARDIZATION)
# ─────────────────────────────────────────────────────
ACTION_QUESTIONS = [
    ("sop_update",  "📋 Cập nhật SOP / Tiêu chuẩn",
     "Bạn sẽ cập nhật SOP hoặc tiêu chuẩn nào? Điều chỉnh cụ thể là gì? Ai phê duyệt?"),
    ("ojt_plan",    "👨‍🏫 Kế hoạch OJT / Đào tạo lại",
     "Ai cần được đào tạo lại? Nội dung đào tạo là gì? Dự kiến thực hiện trong bao lâu?"),
    ("yokoten",     "🌐 Lan tỏa Yokoten",
     "Bài học rút ra từ sự cố này cần được chia sẻ đến bộ phận/nhà máy nào khác? Bằng hình thức gì?"),
    ("next_pdca",   "🔄 Chu trình PDCA tiếp theo",
     "Mục tiêu nâng cao tiêu chuẩn cho chu trình PDCA kế tiếp là gì? Bạn sẽ nâng bar lên mức nào?"),
    ("commitment",  "🤝 Cam kết cá nhân",
     "Với tư cách quản lý, bạn cam kết điều gì cụ thể để đảm bảo vấn đề này KHÔNG tái diễn?"),
]


def stage_action():
    st.markdown('<div class="stage-header">⑦ Giai Đoạn ACTION — Tiêu Chuẩn Hóa & Cải Tiến</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight">"ACTION không phải là điểm kết thúc. Đây là điểm bắt đầu của chu trình PDCA tiếp theo — ở một tầng cao hơn." — Triết lý Kaizen</div>', unsafe_allow_html=True)

    rc = ss.get("root_cause_summary", "Xem phân tích 5 Whys")
    st.markdown(f'<div class="card"><span class="badge">Nguyên nhân gốc rễ</span><br><em style="color:#C9A84C;">{rc}</em></div>', unsafe_allow_html=True)

    std_step  = ss.std_answers.get("_step", 0)
    total     = len(ACTION_QUESTIONS)

    if std_step < total:
        st.progress(std_step / total)
        st.markdown(f'<p class="muted">Câu hỏi {std_step+1} / {total}</p>', unsafe_allow_html=True)

        key_n, label, question = ACTION_QUESTIONS[std_step]
        st.markdown(f'<div class="card-gold"><div class="badge">{label}</div><br><strong>{question}</strong></div>', unsafe_allow_html=True)

        prev = ss.std_answers.get(key_n, "")
        ans  = st.text_area("Câu trả lời:", value=prev, height=110,
                             key=f"std_{std_step}", placeholder="Soạn thảo chi tiết — đây là tài liệu thực chiến của bạn…")

        c1, _ = st.columns([1, 6])
        with c1:
            if st.button("→ Tiếp", key=f"std_next_{std_step}"):
                if ans.strip():
                    ss.std_answers[key_n]  = ans.strip()
                    ss.std_answers["_step"] = std_step + 1
                    st.rerun()
                else:
                    st.warning("Vui lòng soạn thảo nội dung.")
    else:
        # All done
        st.markdown('<div class="card"><div class="badge">✅ Standardization hoàn chỉnh</div></div>', unsafe_allow_html=True)
        for key_n, label, _ in ACTION_QUESTIONS:
            val = ss.std_answers.get(key_n, "—")
            st.markdown(f'<p style="margin:0.5rem 0;"><span class="badge">{label}</span><br><span style="color:#F5F0E8;font-size:0.88rem;">{val}</span></p>', unsafe_allow_html=True)

        # Final QCD boost
        ss.qcd["quality"]  = min(100, ss.qcd["quality"]  + 6)
        ss.qcd["cost"]     = min(100, ss.qcd["cost"]     + 5)
        ss.qcd["delivery"] = min(100, ss.qcd["delivery"] + 7)
        ss.score += 40

        st.markdown('<div class="insight">🎯 PDCA không kết thúc — nó xoay. Bản Standardization bạn vừa soạn là nền tảng cho chu trình tiếp theo ở mức độ trưởng thành cao hơn.</div>', unsafe_allow_html=True)

        if st.button("Xem Kết Quả & Tải Action Plan →"):
            ss.stage = 8
            st.rerun()


# ─────────────────────────────────────────────────────
# STAGE 8 — RESULTS
# ─────────────────────────────────────────────────────
def make_report() -> str:
    aspect_label = f"{ss.aspect} — {ASPECTS[ss.aspect][1]}"
    ctx_text = "\n".join([f"  - {QUESTIONS_5W1H[ss.aspect][i][0]}: {v}" for i, v in ss.ctx_answers.items()])
    plan_text = "\n".join([f"  - {PLAN_QUESTIONS[j][1]}: {ss.plan_answers.get(PLAN_QUESTIONS[j][0],'')}" for j in range(len(PLAN_QUESTIONS))])
    why_text  = "\n".join([f"  Why {l}:\n    Q: {ss.why_questions.get(l,'')}\n    A: {ss.why_answers.get(l,'')}" for l in range(1,6)])
    std_text  = "\n".join([f"  - {label}: {ss.std_answers.get(key,'')}" for key, label, _ in ACTION_QUESTIONS])

    do_opt = next((o for o in DO_OPTIONS if o["key"] == ss.do_choice), DO_OPTIONS[0])

    md = f"""# 📋 ACTION PLAN — KanePackage Vietnam
**Ngày tạo:** {datetime.today().strftime("%d/%m/%Y")}
**Người quản lý:** _(Điền tên)_
**Khía cạnh quản trị:** {aspect_label}

---

## 1. PHÂN TÍCH HIỆN TRẠNG (5W1H)
{ctx_text}

**Từ khóa trích xuất:** {', '.join(ss.keywords)}

---

## 2. MỤC TIÊU SMART
> {ss.smart_goal}

---

## 3. KẾ HOẠCH HÀNH ĐỘNG (5W1H2C + 5M)
{plan_text}

---

## 4. BIẾN CỐ & QUYẾT ĐỊNH (DO Stage)
**Tình huống:** {ss.incident}

**Quyết định:** {do_opt['label']}
**Phân tích:** {do_opt['explanation']}

---

## 5. PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ (5 Whys)
{why_text}

**Nguyên nhân gốc rễ:**
{ss.get('root_cause_summary', '—')}

---

## 6. TIÊU CHUẨN HÓA & CẢI TIẾN (ACTION)
{std_text}

---

## 7. DASHBOARD KẾT QUẢ
| Chỉ số | Điểm cuối |
|--------|-----------|
| Quality | {ss.qcd['quality']}% |
| Cost    | {ss.qcd['cost']}% |
| Delivery| {ss.qcd['delivery']}% |
| **Tổng điểm** | **{ss.score} điểm** |

---
*Được tạo bởi PDCA Master · KanePackage Vietnam · Forval Vietnam*
"""
    return md


def stage_results():
    st.markdown('<div class="stage-header">🏆 Kết Quả — Action Plan Hoàn Chỉnh</div>', unsafe_allow_html=True)

    # Score display
    score = ss.score
    if score >= 100:
        level, color, msg = "Chuyên gia PDCA", "#C9A84C", "Xuất sắc! Tư duy quản lý đạt tầm chiến lược."
    elif score >= 70:
        level, color, msg = "Quản lý Tiên tiến", "#4CAF82", "Tốt! Bạn nắm vững PDCA, tiếp tục nâng cao."
    elif score >= 40:
        level, color, msg = "Quản lý Đang phát triển", "#5B9BD5", "Đúng hướng! Cần thực hành thêm để thành thục."
    else:
        level, color, msg = "Học viên Cơ bản", "#E05252", "Tiếp tục luyện tập — PDCA là kỹ năng cần rèn giũa."

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-box"><div class="score-num" style="color:{color};">{score}</div><div style="color:#8896a8;font-size:0.82rem;">Điểm tổng</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-box"><div style="font-size:1.4rem;font-weight:700;color:{color};">{level}</div><div style="color:#8896a8;font-size:0.82rem;">Cấp độ</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-box"><div style="font-size:0.9rem;color:#F5F0E8;line-height:1.6;padding-top:0.3rem;">{msg}</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### 📊 Dashboard QCD Cuối Game")
    render_qcd()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Generate report
    if not ss.report_md:
        with st.spinner("Đang tạo Action Plan…"):
            ss.report_md = make_report()

    st.markdown("### 📄 Action Plan Hoàn Chỉnh")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(ss.report_md)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "⬇️  Tải Action Plan (.md)",
            data=ss.report_md.encode("utf-8"),
            file_name=f"action_plan_kanepackage_{datetime.today().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_b:
        if st.button("🔄  Chơi lại từ đầu", use_container_width=True):
            api_key = ss.api_key
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            init_state()
            ss.api_key = api_key
            ss.stage   = 1
            st.rerun()

    st.markdown("""
<div class="insight" style="margin-top:2rem;">
  🔄 <strong>"Mỗi chu trình PDCA kết thúc là một chu trình mới bắt đầu — ở một tầng cao hơn."</strong><br>
  Bản Action Plan này là tài liệu sống — hãy cập nhật nó khi thực tế triển khai tại KanePackage.
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────
def main():
    # Header (except welcome)
    if ss.stage > 0:
        st.markdown("""
<div style='display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;'>
  <span style='font-size:1.5rem;'>⚙️</span>
  <span style='font-family:Playfair Display,serif; color:#C9A84C; font-size:1.1rem; font-weight:600;'>
    PDCA MASTER · KanePackage Vietnam
  </span>
  <span style='margin-left:auto; font-family:Playfair Display,serif; color:#C9A84C;'>
    ★ {score} điểm
  </span>
</div>
""".format(score=ss.score), unsafe_allow_html=True)
        render_progress()

        # QCD in sidebar
        if ss.stage >= 4:
            with st.sidebar:
                st.markdown('<div style="color:#C9A84C;font-weight:700;margin-bottom:0.5rem;font-size:0.9rem;">📊 QCD Dashboard</div>', unsafe_allow_html=True)
                render_qcd()
                st.markdown(f'<div class="score-box" style="margin-top:0.5rem;"><div class="score-num">{ss.score}</div><div class="muted">điểm</div></div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    stage_map = {
        0: stage_welcome,
        1: stage_aspect,
        2: stage_5w1h,
        3: stage_smart,
        4: stage_plan,
        5: stage_do,
        6: stage_check,
        7: stage_action,
        8: stage_results,
    }
    fn = stage_map.get(ss.stage, stage_welcome)
    fn()


if __name__ == "__main__":
    main()
