import streamlit as st
import google.generativeai as genai
import re
from extract_text import extract_text_from_image, extract_text_from_pdf

genai.configure(api_key="AIzaSyBrNuQLmvyU7OPtbRJUxe1UyemRIeDsKDo")  
model = genai.GenerativeModel("gemini-2.5-pro") 


def generate_mcq_questions(concept_text):
    short_text = concept_text[:1000] 

    prompt = f"""
You are a professional JEE question paper setter.

Generate exactly 40 high-quality JEE-style multiple-choice questions (MCQs) from the notes below.
each option should be in new line and there should be gap between question and options and s
pace between two questions
Use this format for every question:

Q1. [Question]  

A. Option 1  

B. Option 2  

C. Option 3  

D. Option 4  


Answer: [Correct Option]  

Explanation: [Brief explanation]


NOTES:
\"\"\"

{short_text}

\"\"\"

Return only the questions in the format. No extra text or comments.
"""

    response = model.generate_content(prompt)
    return response.text.strip()

st.set_page_config(page_title="🧠 JEE MCQ Generator", layout="centered")
st.title("📚 JEE MCQ Generator from Notes")
st.markdown("Upload your class notes (image or PDF) and get **JEE-style MCQs** with answers and explanations.")

uploaded_file = st.file_uploader("📁 Upload Notes (Image or PDF)", type=["pdf", "png", "jpg", "jpeg"])


if uploaded_file:
    file_type = uploaded_file.type

    with st.spinner("🔍 Extracting text from your file..."):
        if "pdf" in file_type:
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = extract_text_from_image(uploaded_file)

    st.subheader("📝 Extracted Notes Preview:")
    st.text_area("Preview", extracted_text[:1500], height=200)

    
    if st.button("🚀 Generate JEE MCQs"):
        with st.spinner("🤖 Generating questions using Gemini..."):
            questions = generate_mcq_questions(extracted_text)

        
        st.subheader("📘 JEE-Style MCQs:")

      
        mcq_blocks = re.split(r"\n(?=Q\d+\.)", questions)

        for mcq in mcq_blocks:
            st.markdown(f"""
            <div style="background-color:#f9f9f9;padding:15px;border-radius:10px;margin-bottom:20px;">
            <pre style="font-size:15px;line-height:1.6;">{mcq.strip()}</pre>
            </div>
            """, unsafe_allow_html=True)




