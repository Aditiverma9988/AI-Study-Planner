import streamlit as st
import google.generativeai as genai
import random 
import time
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "plan" not in st.session_state:
    st.session_state.plan = ""
if "streak_updated" not in st.session_state:
    st.session_state.streak_updated = False
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 25 * 60
if "selected_minutes" not in st.session_state:
    st.session_state.selected_minutes = 25
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if not st.session_state.logged_in:

    st.title("🔐 Login")
    st.caption("Login to access your personalized AI Study Planner")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("🔓 Login"):

        USERNAME = st.secrets["USERNAME"]
        PASSWORD = st.secrets["PASSWORD"]

        if username == USERNAME and password == PASSWORD:
            st.success("Login Successful ✅")
            time.sleep(1)
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()
st.sidebar.title("🎓 Student Dashboard")

name = st.sidebar.text_input(
    "👤 Your Name",
    "Aditi"
)

st.sidebar.write(f"Welcome {name} 👋")

st.sidebar.markdown("---")

st.sidebar.metric("🔥 Streak", st.session_state.streak)


st.sidebar.write("🚀 AI Study Planner")
st.sidebar.markdown("---")

st.sidebar.success("Ready to Study 📚")
st.sidebar.markdown("---")

st.sidebar.subheader("📅 Today's Info")

from datetime import datetime

today = datetime.now()

st.sidebar.write("📆", today.strftime("%d %B %Y"))

st.sidebar.write("🕒", today.strftime("%I:%M %p"))

st.sidebar.metric(
    "💻 Status",
    "Active"
)
st.sidebar.metric(
    "🤖 AI Model",
    "Gemini 2.5 Flash"
)
if st.session_state.plan:
    st.sidebar.metric("📄 Plan", "Generated ✅")
else:
    st.sidebar.metric("📄 Plan", "Not Generated")
st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.success("Logged Out Successfully")
    time.sleep(1)

    st.session_state.logged_in=False

    st.rerun()
if st.sidebar.button("🌙 Toggle Theme"):

    if st.session_state.theme=="dark":
        st.session_state.theme="light"

    else:
        st.session_state.theme="dark"

    st.rerun()
if st.session_state.theme == "dark":
    bg = "#0f172a"
    sidebar = "#1e293b"
    card = "#1e293b"
    text = "white"
    placeholder = "#cbd5e1"

else:
    bg = "#f8fafc"
    sidebar = "#e2e8f0"
    card = "#ffffff"
    text = "#0f172a"
    placeholder = "#64748b"
st.markdown(f"""
<style>

.stApp{{
      background:{bg};
color:{text};
}}

[data-testid="stSidebar"]{{
background:{sidebar};
}}
[data-testid="stSidebar"] * {{
color:{text} !important;
}}
h1, h2, h3, h4, h5, h6,
p,
label,
span,
div,
small {{
    color:{text} !important;
}}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {{
    background:{card};
    color:{text};
    border-radius:12px;
    border:1px solid #64748b;
}}
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {{
    color:{text} !important;
}}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {{
    color:{placeholder};
}}

.stButton>button{{
background:linear-gradient(90deg,#4f46e5,#7c3aed);
color:white;
border:none;
border-radius:12px;
height:50px;
font-weight:bold;
width:100%;
}}

.stButton>button:hover{{
transform:scale(1.03);
transition:.3s;
}}

.hero{{
padding:55px;
background:linear-gradient(135deg,#4f46e5,#7c3aed);
border-radius:25px;
text-align:center;
box-shadow:0 15px 35px rgba(0,0,0,.35);
margin-bottom:30px;
color:white;
transition:.3s;
}}
.hero:hover{{
transform:translateY(-5px);
}}

.card{{
padding:28px;
background:{card};
border-radius:22px;
margin-bottom:20px;
box-shadow:0 10px 25px rgba(0,0,0,.18);
border-left:6px solid #6366f1;
transition:.3s;
}}

.card:hover{{
transform:translateY(-6px);
box-shadow:0 15px 35px rgba(79,70,229,.4);
}}

.metric-card{{
padding:25px;
border-radius:18px;
text-align:center;
background:{card};
box-shadow:0 8px 20px rgba(0,0,0,.15);
transition:.3s;
}}
.metric-card:hover{{
transform:translateY(-8px);
}}
.stAlert{{
    color:{text} !important;
}}
hr{{
border:none;
height:1px;
background:#475569;
margin:30px 0;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h1 style="font-size:52px;">📚 AI Study Planner</h1>

<h3>Plan Smarter. Learn Faster. Crack Placements 🚀</h3>

<p>Generate personalized study roadmaps, quizzes, analytics and productivity insights using Google Gemini AI.</p>
<p style="font-size:18px;">
⭐ Personalized Plans &nbsp;&nbsp;&nbsp;
📈 Progress Tracker &nbsp;&nbsp;&nbsp;
🤖 Gemini AI Powered
</p>
</div>
""",unsafe_allow_html=True)
st.markdown(f"""
<div class="card">
<h2>👋 Welcome {name}</h2>
<p style="font-size:18px;">
✅ Personalized AI Roadmaps
🧠 AI Quiz Generator
⏱ Smart Pomodoro Timer
📈 Analytics Dashboard
📄 PDF Export
🔥 Daily Streak Tracking
🎯 Placement Preparation
</p>
</div>
""", unsafe_allow_html=True)
st.write("")

subject = st.text_input("Enter Subject")
st.caption(
"Examples : DSA, DBMS, Python, AI, ML, Java"
)
hours = st.number_input(
    "Hours per day",
    min_value=1,
    max_value=12,
    value=2
)

level = st.selectbox(
    "Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

days = st.slider(
    "Number of Days",
    1,
    30,
    7
)

goal = st.text_input("Study Goal")
st.caption(
"Example : Crack Amazon Interview,Learn DSA,Prepare for Semester,Master Python"
)
overview = st.empty()
overview.markdown(f"""
<div class="card">
<h2>📚 Personalized Study Overview</h2>
<table style="width:100%;font-size:18px;">
<tr>
<td><b>Subject</b></td>
<td>{subject if subject else "-"}</td>
</tr>

<tr>
<td><b>Study Hours</b></td>
<td>{hours}</td>
</tr>

<tr>
<td><b>Days</b></td>
<td>{days}</td>
</tr>

<tr>
<td><b>Difficulty</b></td>
<td>{level}</td>
</tr>

<tr>
<td><b>Goal</b></td>
<td>{goal if goal else "-"}</td>
</tr>
</table>

</div>
""", unsafe_allow_html=True)

st.sidebar.metric("📚 Subject", subject if subject else "-")

st.sidebar.metric("⏰ Daily Hours", hours)
st.write("")
st.subheader("🔥 Current Progress")
st.markdown(f"""
<div class="metric-card">
<h2>🔥</h2>
<h1>{st.session_state.streak}</h1>
Current Streak
</div>
""", unsafe_allow_html=True) 
   
st.subheader("⏱️ Focus Timer")

minutes = st.slider(
    "Study Session (Minutes)",
    15,
    120,
    25
)
st.markdown(f"""
<div class="card">
<h2>⏱ Focus Session</h2>
<h3>{minutes} Minutes</h3>
<p style="margin-top:20px;font-size:17px;">
</p>
</div>
""",unsafe_allow_html=True)
st.success(f"🎯 Focus Session Selected : {minutes} Minutes")

if (
    not st.session_state.timer_running
    and minutes != st.session_state.selected_minutes
):
    st.session_state.selected_minutes = minutes
    st.session_state.remaining_seconds = minutes * 60

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Start Session"):
        st.session_state.timer_running = True

with col2:
    if st.button("⏸ Pause Session"):
        st.session_state.timer_running = False

with col3:
    if st.button("🔄 Reset Session"):
        st.session_state.timer_running = False
        st.session_state.remaining_seconds = minutes * 60



if st.session_state.timer_running:

    st_autorefresh(interval=1000, key="timer")

    if st.session_state.remaining_seconds > 0:
        st.session_state.remaining_seconds -= 1

    else:
        st.session_state.timer_running = False
        st.success("🎉 Congratulations! Focus Session Completed.")
        st.balloons()
timer_placeholder = st.empty()

mins = st.session_state.remaining_seconds // 60
secs = st.session_state.remaining_seconds % 60

timer_placeholder.markdown(f"""
<div style="
background:#1e293b;
padding:25px;
border-radius:20px;
text-align:center;
margin-top:20px;
">

<h1 style="
font-size:55px;
color:#60a5fa;
">
⏳ {mins:02d}:{secs:02d}
</h1>

<p style="font-size:18px;">
Stay Focused 🚀
</p>

</div>
""",unsafe_allow_html=True)
if st.button("🚀 Generate AI Study Plan"):
    if subject.strip() == "":
        st.warning("⚠ Please enter a subject.")
        st.stop()
    prompt = f"""
You are an expert study mentor.
Create a personalized {days}-day study roadmap.
Subject: {subject}
Daily Study Time: {hours} hour(s)
Difficulty: {level}
Goal: {goal}
Instructions:
• Give exactly {days} days.
• Every day should contain:
  - Topics to study
  - Practice task
  - Revision task
  - Mini challenge (if possible)
Keep every day concise.
Example format:
Day 1
• Learn ...
• Practice ...
• Revise ...
Day 2
• ...
"""
    with st.spinner("🤖 Generating your personalized AI roadmap..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.plan = response.text
            st.session_state.streak_updated = False
            st.success("✅ Study Plan Generated Successfully!")
        except Exception as e:
            st.warning(
                "⚠ Gemini quota exceeded. Showing backup study plan."
            )
            topics = [
                "Basics",
                "Core Concepts",
                "Practice Questions",
                "Revision",
                "Mini Project",
                "Mock Test",
                "Final Revision"
            ]
            backup_plan = f"# 📚 {subject} Study Plan\n\n"
            for i in range(days):
                topic = topics[i % len(topics)]
                backup_plan += (
                    f"Day {i+1}\n"
                    f"• Study : {topic}\n"
                    f"• Practice : {hours} hour(s)\n"
                    f"• Revise previous concepts\n\n"
                )
            st.session_state.plan = backup_plan
            st.error(f"Error: {e}")
if st.session_state.plan:
    st.markdown("""
    <div class="card">
    <h2>📖 Personalized AI Study Plan</h2>
    </div>
    """, unsafe_allow_html=True)
    st.code(st.session_state.plan)
if st.session_state.plan:
    st.download_button(
        "📥 Download Study Plan (.txt)",
        data=st.session_state.plan,
        file_name="StudyPlan.txt",
        mime="text/plain"
    )
if st.button("📄 Export as PDF"):
    if st.session_state.plan == "":
        st.warning("⚠ Generate a study plan first.")
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, st.session_state.plan)
        pdf.output("StudyPlan.pdf")
        st.success("✅ PDF Created Successfully!")
        with open("StudyPlan.pdf", "rb") as file:
            st.download_button(
                "⬇ Download PDF",
                data=file,
                file_name="StudyPlan.pdf",
                mime="application/pdf"
            )
st.markdown("---")
st.header("🧠 AI Quiz Generator")
if st.button("🎯 Generate AI Quiz"):
    if subject.strip() == "":
        st.warning("⚠ Please enter a subject first.")
    else:
        quiz_prompt = f"""
You are an expert teacher.
Generate EXACTLY 5 MCQs.
Subject: {subject}
Difficulty: {level}
For each question use EXACTLY this format.
Question 1:
A.
B.
C.
D.
Correct Answer:
Explanation:
Question 2:
A.
B.
C.
D.
Correct Answer:
Explanation:
Repeat till Question 5.
Keep every question on separate lines.
Do NOT write everything in one paragraph.
"""
        with st.spinner("🤖 AI is preparing your quiz..."):
            try:
                quiz = model.generate_content(quiz_prompt)
                st.success("✅ Quiz Generated Successfully!")
                st.markdown("""
<div class="card">
<h2>📝 AI Quiz</h2>
</div>
""", unsafe_allow_html=True)
                st.markdown(
                    f"```text\n{quiz.text}\n```"
                )
            except Exception as e:
                st.error(f"❌ {e}")
subject_lower = subject.strip().lower()

subject_info = {
    "dsa": "💻 Data Structures & Algorithms",
    "dbms": "🗄️ Database Management System",
    "python": "🐍 Python Programming",
    "java": "☕ Java Programming",
    "ai": "🤖 Artificial Intelligence",
    "ml": "📈 Machine Learning",
    "web development": "🌐 Web Development",
    "os": "🖥️ Operating System",
    "cn": "🌐 Computer Networks",
    "oops": "📘 Object-Oriented Programming",
    "c": "⚙️ C Programming",
    "c++": "💠 C++ Programming",
    "cloud": "☁️ Cloud Computing",
    "devops": "🚀 DevOps",
    "react": "⚛️ React JS",
    "sql": "🗄️ SQL",
    "cyber security": "🔐 Cyber Security"
}

if subject_lower in subject_info:
    st.info(subject_info[subject_lower])
else:
    if subject.strip():
        st.info(f"📚 {subject.title()}")
st.subheader("✅ Daily Progress Tracker")
completed = sum(
    st.checkbox(f"Day {i+1} Completed", key=f"day_{i}")
    for i in range(days)
)
remaining = days - completed
progress = completed / days if days else 0
percentage = int(progress * 100)
st.progress(progress)
st.metric("🎯 Completion", f"{percentage}%")
st.markdown("---")
st.header("📊 Analytics Dashboard")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("✅ Completed", completed)
with c2:
    st.metric("📅 Remaining", remaining)
with c3:
    st.metric("🎯 Progress", f"{percentage}%")
fig = px.pie(
    values=[completed, remaining],
    names=["Completed", "Remaining"],
    hole=0.55,
    color=["Completed", "Remaining"],
    color_discrete_map={
        "Completed": "#22c55e",
        "Remaining": "#ef4444"
    }
)
st.plotly_chart(fig, use_container_width=True)
if completed > 0:
    fig2 = px.line(
        x=[f"Day {i+1}" for i in range(days)],
        y=[min(i + 1, completed) for i in range(days)],
        markers=True,
        title="Study Progress Over Time",
        labels={
            "x": "Days",
            "y": "Completed Days"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("📚 Complete at least one day to view analytics.")
study_hours = [
    hours if i < completed else 0
    for i in range(days)
]
fig3 = px.bar(
    x=[f"Day {i+1}" for i in range(days)],
    y=study_hours,
    text=study_hours,
    title="Daily Study Hours",
    labels={
        "x": "Days",
        "y": "Hours"
    }
)
st.plotly_chart(fig3, use_container_width=True)
if percentage == 100:
    st.success("🏆 Outstanding! You completed your entire study plan.")
elif percentage >= 80:
    st.success("🔥 Excellent Progress! Keep it up.")
elif percentage >= 50:
    st.info("👍 Great Job! Stay consistent.")
elif percentage >= 20:
    st.warning("📚 Nice start. Keep studying every day.")
else:
    st.error("⚡ Let's begin today's study session!")
st.caption("🚀 Small daily progress leads to big success.")
st.markdown("---")
badge = "🎖 Beginner"
if percentage >= 100:
    badge = "👑 Master Learner"
elif percentage >= 80:
    badge = "🥇 Gold"
elif percentage >= 50:
    badge = "🥈 Silver"
elif percentage >= 25:
    badge = "🥉 Bronze"
st.success(f"🏆 Current Badge : {badge}")
st.info(f"""
📅 Total Days : {days}
✅ Completed : {completed}
❌ Remaining : {remaining}
🎯 Progress : {percentage}%
""")
if completed == days and days > 0:
    st.balloons()
    st.success("🎉 Congratulations! You completed your study plan.")
if not st.session_state.streak_updated:
    st.session_state.streak += 1
    st.session_state.streak_updated = True

st.metric("🔥 Study Streak", st.session_state.streak)
st.markdown("---")
st.markdown("""
<div class="card">
<h2>📚 Recommended Learning Resources</h2>
<p>Best websites to master your subject.</p>
</div>
""", unsafe_allow_html=True)
resources = {
    "dsa": {
        "💻 LeetCode": "https://leetcode.com",
        "📘 GeeksforGeeks": "https://www.geeksforgeeks.org",
        "🚀 NeetCode": "https://neetcode.io"
    },
    "dbms": {
        "📘 SQLBolt": "https://sqlbolt.com",
        "💻 W3Schools SQL": "https://www.w3schools.com/sql",
        "📚 GeeksforGeeks DBMS": "https://www.geeksforgeeks.org/dbms"
    },
    "python": {
        "🐍 Python Docs": "https://docs.python.org/3/",
        "📘 W3Schools Python": "https://www.w3schools.com/python/",
        "💻 Real Python": "https://realpython.com"
    },
    "java": {
        "☕ Oracle Java": "https://docs.oracle.com/javase/tutorial/",
        "📘 W3Schools Java": "https://www.w3schools.com/java/",
        "💻 GeeksforGeeks Java": "https://www.geeksforgeeks.org/java/"
    },
    "os": {
        "📘 GeeksforGeeks OS": "https://www.geeksforgeeks.org/operating-systems/"
    },
    "cn": {
        "🌐 GeeksforGeeks CN": "https://www.geeksforgeeks.org/computer-networks/"
    },
    "oops": {
        "📘 GeeksforGeeks OOPS": "https://www.geeksforgeeks.org/object-oriented-programming/"
    },
    "ai": {
        "🤖 Google AI": "https://ai.google",
        "📘 Coursera AI": "https://coursera.org",
        "💻 DeepLearning.AI": "https://www.deeplearning.ai"
    },
    "ml": {
        "📈 Kaggle": "https://kaggle.com",
        "📘 Scikit Learn": "https://scikit-learn.org",
        "💻 Coursera ML": "https://coursera.org"
    }
}
default_resources = {
    "🎥 YouTube": "https://youtube.com",
    "📘 Coursera": "https://coursera.org",
    "💻 Udemy": "https://udemy.com"
}
selected_resources = resources.get(subject_lower, default_resources)
for title, link in selected_resources.items():
    st.markdown(f"### [{title}]({link})")
st.markdown("---")
st.subheader("🎯 Today's Goal")

today_goal = st.text_input(
    "Set Today's Goal",
    value=st.session_state.get("today_goal", "")
)

if st.button("💾 Save Goal"):

    st.session_state.today_goal = today_goal
    st.success("✅ Today's Goal Saved!")

st.markdown("---")

st.subheader("📝 Study Notes")
notes = st.text_area(
    "Write your notes here...",
    value=st.session_state.get("notes", ""),
    height=180
)
if st.button("💾 Save Notes"):
    st.session_state.notes = notes
    st.success("✅ Notes Saved Successfully!")
if st.session_state.get("notes"):
    st.download_button(
        "📥 Download Notes",
        st.session_state.notes,
        file_name="Study_Notes.txt"
    )
st.markdown("---")
quotes = [
    "🚀 Keep learning, keep growing!",
    "💪 Consistency beats intensity.",
    "🌱 Small progress is still progress.",
    "📚 Every day counts.",
    "🔥 Success comes from daily effort.",
    "⭐ Learn something today your future self will thank you for.",
    "🎯 Stay focused. Stay consistent."
]
st.info(random.choice(quotes))

st.subheader("💪 Daily Motivation")
if st.button("✨ Motivate Me"):
    try:
        with st.spinner("Generating Motivation..."):
            prompt = """
            Give one powerful motivational quote for a student preparing for exams or placements.
            Keep it under 25 words.
            """
            quote = model.generate_content(prompt)
        st.success(quote.text)
    except Exception:
        motivational_quotes = [
            "Believe in yourself. Every expert was once a beginner. 🚀",
            "Small daily improvements lead to big success. 🌱",
            "Success comes from consistency, not perfection. 💪",
            "Study now so your future self thanks you. ⭐"
        ]
        st.success(random.choice(motivational_quotes))

study_tips = [
    "📚 Revise before sleeping.",
    "💻 Practice coding every day.",
    "⏱ Follow the Pomodoro Technique.",
    "📝 Make short revision notes.",
    "🎯 Focus on concepts instead of memorizing.",
    "🔥 Practice interview questions regularly."
]
st.info(random.choice(study_tips))
st.markdown("---")
st.subheader("📊 Final Study Summary")
st.markdown(f"""
<div class="card">
<h3>📚 Your Study Plan</h3>
<table style="width:100%;font-size:17px;">
<tr>
<td><b>📘 Subject</b></td>
<td>{subject if subject else "-"}</td>
</tr>
<tr>
<td><b>📅 Duration</b></td>
<td>{days} Days</td>
</tr>
<tr>
<td><b>⏰ Daily Hours</b></td>
<td>{hours}</td>
</tr>
<tr>
<td><b>🎯 Goal</b></td>
<td>{goal if goal else "-"}</td>
</tr>
<tr>
<td><b>📈 Difficulty</b></td>
<td>{level}</td>
</tr>
<tr>
<td><b>🔥 Streak</b></td>
<td>{st.session_state.streak}</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown(f"""
<div style="
background:{card};
padding:30px;
border-radius:18px;
text-align:center;
margin-top:25px;
box-shadow:0 8px 20px rgba(0,0,0,.2);
">
<h2>🚀 AI Study Planner</h2>
<p style="font-size:17px;">
Plan Smarter • Learn Faster • Achieve More
</p>
<hr>
<p>
Built using ❤️ with
<b>Python</b>,
<b>Streamlit</b>,
<b>Gemini AI</b>,
<b>Plotly</b>,
<b>FPDF</b>
</p>
<p>
Designed & Developed by
<b>Aditi Verma</b>
</p>
<p style="font-size:14px;">
© 2026 AI Study Planner • All Rights Reserved
</p>
</div>
""", unsafe_allow_html=True)