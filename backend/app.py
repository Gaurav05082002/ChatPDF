from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from flask_cors import CORS


# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")
genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            if page:
                text += page.extract_text() or ""
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. 
    If the answer is not in the provided context, just say, "Answer is not available in the context."
    
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# Routes
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        files = request.files.getlist('pdf_files')
        if not files:
            return jsonify({"error": "No files uploaded"}), 400
        
        raw_text = get_pdf_text(files)
        if not raw_text.strip():
            return jsonify({"error": "No text extracted from PDFs"}), 400
        
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        print(raw_text)
        return jsonify({"message": "Files processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        print("Received request at /ask_question")
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        question = data.get("question")
        print(f"Question received: {question}")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Loading FAISS index...")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(question)

        if not docs:
            print("No relevant context found for the question")
            return jsonify({"error": "No relevant context found for the question"}), 404

        print("Context found, running conversational chain...")
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

        answer = response.get("output_text", "No response generated")
        print(f"Answer generated: {answer}")
        return jsonify({"answer": answer}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
