import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import io
from chains  import Chain

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    with io.BytesIO(file.getvalue()) as f:
        reader = PdfReader(f)
        text = [page.extract_text() for page in reader.pages if page.extract_text()]
    return " ".join(text)

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(io.BytesIO(file.getvalue()))
    return " ".join([para.text for para in doc.paragraphs if para.text])


def app(llm):
    st.title('Document Processor')

    uploaded_file = st.file_uploader("Upload your file (PDF or DOCX)", type=['pdf', 'docx'])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.pdf'):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            text = extract_text_from_docx(uploaded_file)

        st.subheader("Extract Text From The Document")    
        if st.button('Extract_text'):
            st.write('Extracted Text:')
            st.write(text)

        st.subheader("Summarize The Document")    
        if st.button('Summarize'):
           new_text = llm.summarize_text(text)
           st.write("Summary of the document")
           st.write(new_text)


        st.subheader("Ask a question based on the document")
        user_question = st.text_input("Ask a question")
        if user_question:
            answer = llm.answer_question(text, user_question)
            st.write('Answer:', answer)

        st.subheader("Translate Document")
        
        target_language = st.text_input("Target Language (e.g., Spanish, German)")
        if st.button('Translate'):
            translated_text = llm.translate_text(text, target_language)
            st.write('Translated Text:')
            st.write(translated_text)

        st.subheader("Classify Your Document")    
        if st.button('Classify Document'):
            doc_type = llm.classify_document(text)
            st.write('Document Type:', doc_type)

        st.subheader("Detect Anomalies in Your Document")
        if st.button('Detect Anomalies'):
            anomalies = llm.detect_anomalies(text)

            st.write('Detected Anomalies:', anomalies)


    
if __name__ == '__main__':
    chain = Chain()
    app(chain)
    
