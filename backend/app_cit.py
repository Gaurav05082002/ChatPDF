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
    text_with_pages = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page_num, page in enumerate(pdf_reader.pages, 1):  # page_num starts from 1
            page_text = page.extract_text() or ""
            if page_text:
                text_with_pages.append((page_text, page_num))  # store text with page number
    return text_with_pages

def get_text_chunks(text_with_pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    text_chunks = []
    # print("int get_text_chunks")
    for text, page_num in text_with_pages:
        chunks = text_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            # Each chunk is associated with the source page number
            text_chunks.append({"chunk": chunk, "page_num": page_num, "chunk_num": i + 1})
    # print("text_chunks"  , text_chunks)       
    return text_chunks



def get_vector_store(text_chunks):
    try:
        print("Starting vector store creation...")

        # Initialize embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Separate text and metadata (page numbers)
        texts = [chunk["chunk"] for chunk in text_chunks]
        metadatas = [{"page": chunk["page_num"], "chunk_num": chunk.get("chunk_num", 0)} for chunk in text_chunks]

        # Create FAISS vector store with texts and corresponding metadata
        vector_store = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
        
        # Save the vector store locally
        vector_store.save_local("faiss_index")
        print("Vector store successfully created and saved.")

    except Exception as e:
        print(f"Error in vector store creation: {str(e)}")
        raise



def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details.
    If the answer is not in the provided context, just say, "Answer is not available in the context."
    
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    
    # Initialize the language model
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # Load the QA chain
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    def custom_answer_func(question, context_docs):
        # response = {
        #                 "answer": "Your answer text here",
        #                 "citations": "No citations available" 
        #             }

        # return response

        try:
            # Extract text and metadata for citations
            context_texts = [doc.page_content for doc in context_docs]
            metadata_list = [doc.metadata for doc in context_docs]
            # print("context_texts" ,   context_texts )
            # print("metadata_list" , metadata_list)
            # Combine all retrieved contexts into a single string
            combined_context = "\n".join(context_texts)
            input_data = {
            "input_documents": context_docs,  # Providing the context documents
            "question": question
            }

            #    Run the chain to get the answer using `invoke`
            result = chain.invoke(input_data)
            # Run the chain to get the answer
            # result = chain.invoke(question=question, context=combined_context)

            # Generate citations from metadata
            citations = ", ".join(
                f"Page {meta.get('page', 'unknown')}" for meta in metadata_list if 'page' in meta
            )
            output_text = result.get("output_text", "No response generated").strip()

            # Format the final response
            if output_text:
                return f"{output_text}\n\nCitations: {citations if citations else 'No citations available'}"
            else:
                return "Answer is not available in the context."

        except Exception as e:
            print(f"Error in generating the answer: {str(e)}")
            return "An error occurred while generating the answer."

    return custom_answer_func


# Routes
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        files = request.files.getlist('pdf_files')
        if not files:
            return jsonify({"error": "No files uploaded"}), 400
        
        raw_text = get_pdf_text(files)
        # print("get_pdf_text_output" , raw_text)
        # if not raw_text.strip():
        #     return jsonify({"error": "No text extracted from PDFs"}), 400
        
        text_chunks = get_text_chunks(raw_text)
        # print("output of get_text_chunks" , text_chunks)
        get_vector_store(text_chunks)
        # print(raw_text)
        return jsonify({"message": "Files processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        print("Received request at /ask_question")
        
        # Parse the request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Extract the question from the request
        question = data.get("question")
        print(f"Question received: {question}")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Load embeddings and FAISS index
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        print("Loading FAISS index...")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        
        # Perform similarity search
        docs = new_db.similarity_search(question)
        if not docs:
            print("No relevant context found for the question")
            return jsonify({"error": "No relevant context found for the question"}), 404

        # Log the number of documents retrieved
        print(f"Retrieved {len(docs)} documents for context.")

        # Run the conversational chain
        print("Context found, running conversational chain...")
        chain = get_conversational_chain()

        # Generate response using the custom chain function
        answer = chain(question, docs)

        if not answer:
            print("No response generated")
            return jsonify({"error": "No response generated"}), 500

        print(f"Answer generated: {answer}")
        return jsonify({"answer": answer}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Main entry point
if __name__ == "__main__":
    app.run(debug=True)