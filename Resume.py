import streamlit as st
from fpdf import FPDF
from docx import Document
import base64
from PIL import Image
from io import BytesIO
import os

# ✅ Page Configuration
st.set_page_config(page_title="GenAI Resume Builder", layout="centered")

# 🎨 Custom CSS Styling with Rain Animation & Hover
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    .stApp {
        font-family: 'Segoe UI', sans-serif;
        color: #ff0000;
        background: linear-gradient(#000000, #1a1a1a);
        animation: fadeIn 1s ease-in-out;
        position: relative;
    }

    .main > div {
        background-color: #1a1a1a;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(255,0,0,0.3);
        color: #ffffff;
        animation: fadeIn 1.5s ease-in-out;
    }

    input, textarea {
        background-color: #333 !important;
        color: #fff !important;
        border: 1px solid #ff0000 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    input:hover, textarea:hover {
        border-color: #ffffff !important;
        transform: scale(1.03);
        box-shadow: 0 0 10px rgba(255,255,255,0.2);
    }

    .rain {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }

    .drop {
        position: absolute;
        width: 2px;
        height: 20px;
        background: red;
        animation: fall 1s linear infinite;
    }

    @keyframes fall {
        to {
            transform: translateY(100vh);
            opacity: 0;
        }
    }

    .resume-preview:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255,0,0,0.6);
        transition: 0.4s ease-in-out;
    }
    </style>
    <div class="rain">
        """ + "\n".join([
            f'<div class="drop" style="left: {i}%; animation-delay: {i * 0.1}s;"></div>'
            for i in range(0, 100, 3)
        ]) + """
    </div>
""", unsafe_allow_html=True)

# 🧬 Title and Subtitle
st.title("🔧 GenAI Resume Builder")
st.markdown("<h4 style='color:#ff0000;'>Craft your resume with GenAI. Enter details and generate your pro resume!</h4>", unsafe_allow_html=True)

# 📷 Upload Image
st.header("🖼️ Upload Profile Picture")
image_file = st.file_uploader("Choose your photo (JPG or PNG)", type=['jpg', 'jpeg', 'png'])

# 📅 Personal Info
st.header("👤 Personal Info")
name = st.text_input("Full Name", placeholder="e.g. John Doe")
job_title = st.text_input("Job Title", placeholder="e.g. Full Stack Developer")

# 💼 Experience
st.header("🏢 Work Experience")
experience = st.text_area("Work Experience (one bullet per line)", placeholder="- Developer at ABC Corp\n- Intern at XYZ")

# 🎓 Education
st.header("🏫 Education")
school = st.text_input("School", placeholder="e.g. ABC High School")
college = st.text_input("College", placeholder="e.g. XYZ University")
degree = st.text_input("Degree", placeholder="e.g. B.Tech in IT")
edu_summary = st.text_area("Education Highlights (one bullet per line)", placeholder="- CGPA: 9.0\n- Technical Fest Winner")

# 🛠️ Skills
st.header("🛠️ Skills")
skills = st.text_area("Skills (comma-separated)", placeholder="Python, JavaScript, React, SQL")

# 🌐 Contact Info
st.header("📬 Contact")
linkedin = st.text_input("LinkedIn", placeholder="https://linkedin.com/in/yourname")
email = st.text_input("Email", placeholder="you@example.com")
facebook = st.text_input("Facebook", placeholder="https://facebook.com/yourprofile")
manual_contact = st.text_area("Other Contact (phone, location)", placeholder="Phone: +91-9876543210\nLocation: Mumbai, India")

# 🚀 Generate Resume
if st.button("🚀 Build My Resume"):
    if not all([name, job_title, experience, skills, email, degree]):
        st.warning("Please fill in all required fields.")
    elif not image_file:
        st.warning("Profile picture is required.")
    else:
        exp_lines = experience.strip().split('\n')
        edu_lines = edu_summary.strip().split('\n')
        skills_list = [s.strip() for s in skills.split(',')]

        # 📄 Resume HTML
        img = Image.open(image_file).convert("RGB")
        img = img.resize((120, 120))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        img_html = f'<img src="data:image/png;base64,{img_base64}" style="border-radius: 50%;width:120px;height:120px;object-fit:cover;"/>'

        resume_html = f"""
        <div class="resume-preview" style="background:#fff;color:#000;padding:30px;border-radius:10px;">
            <h1 style="text-align:center;color:#d10000;">{name}</h1>
            <div style="text-align:center;">{img_html}</div>
            <h3>{job_title}</h3>
            <hr>
            <h4 style="color:#d10000;">Summary</h4>
            <p>Motivated and skilled professional applying for {job_title}.</p>

            <h4 style="color:#d10000;">Experience</h4>
            <ul>{''.join([f'<li>{line}</li>' for line in exp_lines])}</ul>

            <h4 style="color:#d10000;">Education</h4>
            <p><b>School:</b> {school}<br><b>College:</b> {college}<br><b>Degree:</b> {degree}</p>
            <ul>{''.join([f'<li>{line}</li>' for line in edu_lines])}</ul>

            <h4 style="color:#d10000;">Skills</h4>
            <p>{' | '.join(skills_list)}</p>

            <h4 style="color:#d10000;">Contact</h4>
            <p><b>Email:</b> {email}<br><b>LinkedIn:</b> {linkedin}<br><b>Facebook:</b> {facebook}<br><b>Other:</b> {manual_contact}</p>
        </div>
        """

        st.markdown("### 🧾 Resume Preview")
        st.components.v1.html(resume_html, height=800, scrolling=True)

        # ✅ Generate PDF
        pdf = FPDF()
        pdf.add_page()

        # Save temporary image
        img_path = "profile_pic_temp.png"
        img.save(img_path, format="PNG")
        pdf.image(img_path, x=10, y=8, w=30)

        pdf.set_xy(45, 10)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, name, ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, job_title, ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Summary", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Motivated and skilled professional applying for {job_title}.")

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Experience", ln=True)
        pdf.set_font("Arial", '', 12)
        for exp in exp_lines:
            pdf.multi_cell(0, 10, f"- {exp.strip()}")

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Education", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"School: {school}\nCollege: {college}\nDegree: {degree}")
        for edu in edu_lines:
            pdf.multi_cell(0, 10, f"- {edu.strip()}")

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Skills", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ', '.join(skills_list))

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Contact", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Email: {email}\nLinkedIn: {linkedin}\nFacebook: {facebook}\nOther: {manual_contact}")

        pdf_bytes = pdf.output(dest='S').encode('latin1', 'replace')

        st.download_button(
            label="📄 Download PDF Resume",
            data=pdf_bytes,
            file_name=f"{name.replace(' ', '_')}_resume.pdf",
            mime="application/pdf"
        )

        if os.path.exists(img_path):
            os.remove(img_path)
