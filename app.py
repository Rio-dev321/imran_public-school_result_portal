
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Imran Public School | Result Portal",
    page_icon="🎓",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #f3f6fb;
}
.main-title {
    background: linear-gradient(120deg, #101f43, #244b83);
    padding: 28px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}
.main-title h1 {
    color: white;
    font-size: 30px;
}
.main-title p {
    color: #dce8ff;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 13px;
    border-left: 5px solid #d6a83c;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}
.metric-label {
    color: #64748b;
    font-size: 14px;
}
.metric-value {
    color: #142b50;
    font-size: 27px;
    font-weight: bold;
}
.section-title {
    color: #142b50;
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SAMPLE STUDENT DATA ----------------

students = [
    {
        "name": "Ali Ahmed",
        "roll": "101",
        "class": "10th",
        "section": "A",
        "father": "Ahmed Khan",
        "subjects": {
            "English": 85,
            "Urdu": 78,
            "Mathematics": 92,
            "Physics": 88,
            "Chemistry": 80,
            "Biology": 90
        }
    },
    {
        "name": "Ayesha Noor",
        "roll": "102",
        "class": "10th",
        "section": "A",
        "father": "Muhammad Noor",
        "subjects": {
            "English": 90,
            "Urdu": 88,
            "Mathematics": 95,
            "Physics": 91,
            "Chemistry": 89,
            "Biology": 94
        }
    },
    {
        "name": "Usman Ali",
        "roll": "103",
        "class": "10th",
        "section": "B",
        "father": "Ali Hassan",
        "subjects": {
            "English": 45,
            "Urdu": 55,
            "Mathematics": 30,
            "Physics": 48,
            "Chemistry": 50,
            "Biology": 42
        }
    },
    {
        "name": "Fatima Khan",
        "roll": "104",
        "class": "10th",
        "section": "B",
        "father": "Khan Muhammad",
        "subjects": {
            "English": 82,
            "Urdu": 85,
            "Mathematics": 89,
            "Physics": 84,
            "Chemistry": 86,
            "Biology": 91
        }
    }
]

# ---------------- RESULT CALCULATIONS ----------------

def calculate_result(student):
    marks = student["subjects"]
    total = sum(marks.values())
    maximum = len(marks) * 100
    percentage = (total / maximum) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    elif percentage >= 33:
        grade = "E"
    else:
        grade = "F"

    status = (
        "PASS" if all(mark >= 33 for mark in marks.values())
        else "FAIL"
    )

    return total, maximum, percentage, grade, status


# ---------------- PDF GENERATOR ----------------

def generate_pdf(student):
    total, maximum, percentage, grade, status = (
        calculate_result(student)
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    heading = ParagraphStyle(
        "SchoolHeading",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17345D"),
        fontSize=19
    )

    elements = []

    elements.append(Paragraph(
        "IMRAN PUBLIC SCHOOL AND COLLEGE", heading
    ))
    elements.append(Paragraph(
        "STUDENT ACADEMIC RESULT CARD",
        ParagraphStyle(
            "Subheading",
            parent=styles["Heading2"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#B58A28")
        )
    ))
    elements.append(Spacer(1, 25))

    details = [
        ["Student Name", student["name"]],
        ["Roll Number", student["roll"]],
        ["Father Name", student["father"]],
        ["Class", student["class"]],
        ["Section", student["section"]]
    ]

    info_table = Table(details, colWidths=[140, 330])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#E8EEF7")),
        ("TEXTCOLOR", (0, 0), (-1, -1),
         colors.HexColor("#17345D")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold")
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 25))

    marks_data = [["Subject", "Obtained Marks", "Total Marks"]]

    for subject, marks in student["subjects"].items():
        marks_data.append([subject, marks, 100])

    marks_data.append(["TOTAL", total, maximum])

    marks_table = Table(
        marks_data,
        colWidths=[220, 125, 125]
    )

    marks_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#17345D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1),
         colors.HexColor("#E8EEF7")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")
    ]))

    elements.append(marks_table)
    elements.append(Spacer(1, 25))

    summary = [
        ["Percentage", f"{percentage:.2f}%"],
        ["Grade", grade],
        ["Final Status", status]
    ]

    summary_table = Table(summary, colWidths=[220, 250])
    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#E8EEF7")),
        ("PADDING", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold")
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 35))
    elements.append(Paragraph(
        "Principal Signature: __________________________",
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🎓 Result Portal")
    st.markdown("---")
    st.subheader("Navigation")
    st.info("🏫 Imran Public School and College")
    st.markdown("---")
    st.caption("Academic Session 2026")
    st.caption("Student Result Management System")


# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
    <h1>🎓 IMRAN PUBLIC SCHOOL AND COLLEGE</h1>
    <p>STUDENT RESULT MANAGEMENT PORTAL</p>
    <p>Academic Session 2026</p>
</div>
""", unsafe_allow_html=True)


# ---------------- DASHBOARD ----------------

results = [calculate_result(s) for s in students]

total_students = len(students)
passed_students = sum(1 for r in results if r[4] == "PASS")
failed_students = total_students - passed_students
average_percentage = sum(r[2] for r in results) / total_students

st.markdown('<p class="section-title">📊 Dashboard Overview</p>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

metrics = [
    (c1, "Total Students", total_students),
    (c2, "Passed Students", passed_students),
    (c3, "Failed Students", failed_students),
    (c4, "Average Percentage", f"{average_percentage:.1f}%")
]

for col, label, value in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)


# ---------------- STUDENT SEARCH ----------------

st.markdown('<p class="section-title">🔍 Search Student Result</p>',
            unsafe_allow_html=True)

search = st.text_input(
    "Enter Student Name or Roll Number",
    placeholder="Example: Ali Ahmed or 101"
)

if search:
    filtered_students = [
        s for s in students
        if search.lower() in s["name"].lower()
        or search.lower() in s["roll"].lower()
    ]
else:
    filtered_students = students

if filtered_students:

    student_options = {
        f'{s["name"]} | Roll No: {s["roll"]}': s
        for s in filtered_students
    }

    selected_label = st.selectbox(
        "Select Student",
        list(student_options.keys())
    )

    student = student_options[selected_label]

    total, maximum, percentage, grade, status = (
        calculate_result(student)
    )

    st.markdown("---")
    st.markdown('<p class="section-title">👨‍🎓 Student Details</p>',
                unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    d1.write(f"**Name:** {student['name']}")
    d2.write(f"**Roll Number:** {student['roll']}")
    d3.write(f"**Father Name:** {student['father']}")

    d1.write(f"**Class:** {student['class']}")
    d2.write(f"**Section:** {student['section']}")
    d3.write("**Session:** 2026")

    # SUBJECT MARKS

    st.markdown('<p class="section-title">📚 Subject-wise Marks</p>',
                unsafe_allow_html=True)

    marks_df = pd.DataFrame([
        {
            "Subject": subject,
            "Obtained Marks": marks,
            "Total Marks": 100,
            "Status": "PASS" if marks >= 33 else "FAIL"
        }
        for subject, marks in student["subjects"].items()
    ])

    st.dataframe(
        marks_df,
        use_container_width=True,
        hide_index=True
    )

    # RESULT SUMMARY

    st.markdown('<p class="section-title">🏆 Final Result</p>',
                unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("Total Marks", f"{total}/{maximum}")
    r2.metric("Percentage", f"{percentage:.2f}%")
    r3.metric("Grade", grade)
    r4.metric("Result", status)

    if status == "PASS":
        st.success("Congratulations! Student has passed.")
    else:
        st.error("Student has failed. Please check subject marks.")

    # PDF DOWNLOAD

    st.markdown('<p class="section-title">📄 Download Result</p>',
                unsafe_allow_html=True)

    pdf_file = generate_pdf(student)

    st.download_button(
        label="⬇️ Download Student Result PDF",
        data=pdf_file,
        file_name=f"Result_{student['roll']}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.warning("No student found. Please check the name or roll number.")


# ---------------- FOOTER ----------------

st.markdown("---")
st.markdown(
    "<center>© 2026 Imran Public School and College | "
    "Student Result Portal</center>",
    unsafe_allow_html=True
)
