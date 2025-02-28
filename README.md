# ChatPDF
ChatPDF is a web application designed for seamless interaction with PDFs. This project is divided into two parts: the **backend** and the **frontend**, which need to be run in separate terminals.
### Demo Images 
![page1](https://github.com/user-attachments/assets/cdbabda1-3928-43e1-a02b-b8d672b9e7b2)
![page2](https://github.com/user-attachments/assets/8f8fcc16-17fb-4d69-8eb2-99bb7b427c32)
![page3](https://github.com/user-attachments/assets/d8635d74-5391-48f2-95f7-067efa8b5cac)


https://github.com/user-attachments/assets/d7c173a0-0243-4d61-8110-af2b3930ed46



Uploading screen-capture.mp4…




## Clone the Repository

To begin, clone the repository using the following command:
```bash
git clone https://github.com/Gaurav05082002/ChatPDF.git
```

After cloning, navigate to the `ChatPDF` directory:
```bash
cd ChatPDF
```

---

## Backend Setup

The backend is built using Python. To set it up and run, follow these steps:
navigate to backend folder 
### 1. Install Required Dependencies
Ensure you have Python 3.10 or higher installed. Install the required Python packages by running:
```bash
pip install -r requirements.txt
```

### 2. Create a `.env` File
In the `backend/` folder, create a file named `.env` and add the following line to it:
```env
GOOGLE_API_KEY="<your_google_api_key>"
```

#### How to Get a Google API Key:
You can obtain a Google API key by following these steps:
1. Go to the [Google Ai Studio](https://aistudio.google.com/prompts/new_chat?gad_source=1&gclid=Cj0KCQiA4fi7BhC5ARIsAEV1YiZE3IUqYaco1sjh6khoZhz7q-ZcaCsQCuoFRKQMIaSN-0JX9PFG548aAp1cEALw_wcB).
2. On top left click on get api key button and create api key.
3. Copy the generated key and paste it into the `.env` file.

### 3. Start the Backend Server
Once all dependencies are installed and the `.env` file is set up, you can start the backend server. For Linux, use:
```bash
python3 app.py
```

The backend server should now be running.

---

## Frontend Setup

The frontend is built using React. To set it up and run, follow these steps:

### 1. Install Required Dependencies
Navigate to the `frontend/` folder and install the required dependencies using:
```bash
npm install
```

### 2. Start the Frontend
After the dependencies are installed, start the frontend server with:
```bash
npm start
```

This will launch the application in your default web browser. By default, the frontend runs on `http://localhost:3000`.

---

## Additional Notes

- **System Requirements**:
  - Python 3.10 or higher
  - Node.js and npm (latest stable versions)
  - A stable internet connection to access the Google API.

- **Folder Structure**:
  - `backend/`: Contains the server-side code.
  - `frontend/`: Contains the React application code.

- **Error Handling**:
  - Ensure the `.env` file is correctly set up.
  - Double-check the API key and permissions on the Google Cloud Console.

---
## Literature Part
- FAISS and Embeddings: How Does It Work?:
 -FAISS works by indexing embeddings for fast similarity search. Here's how:

 -Create Embeddings:

Use a pre-trained or custom model (e.g., OpenAI, BERT, or CLIP) to generate embeddings for your data (like text or images).
Indexing:

- Embeddings are indexed using FAISS. FAISS organizes them in a way that allows for efficient retrieval.
Indexing algorithms include exact search (brute force) and approximate nearest-neighbor search (faster for large datasets).
Search:

- A query (like a user's question) is also converted into an embedding.
FAISS compares the query embedding with the indexed embeddings to find the most similar entries.
Return Results:

- The most relevant documents, images, or data points are retrieved based on similarity scores.

## How Does FAISS Work in This Case?

### 1. Question Embedding
The input question is converted into an embedding using the **GoogleGenerativeAIEmbeddings** model.

### 2. FAISS Index
Precomputed embeddings for documents are stored in a **FAISS index** (`faiss_index`).

### 3. Similarity Search
The FAISS index is queried with the question's embedding to find the most similar document embeddings.

### 4. Context Retrieval
The documents corresponding to the most similar embeddings are retrieved and used as context for answering the question.

### 5. Response Generation
The retrieved documents and the input question are fed into a conversational AI model to generate an answer.

## Embeddings Model (models/embedding-001)
- **Purpose**: Converts text into vector representations for semantic understanding.
- **Functionality**: 
  - Transforms input text into dense vectors (embeddings).
  - Enables the system to find contextually similar chunks by measuring similarity between embeddings.
  
## Generative AI Model (Gemini-1.5-pro)
- **Purpose**: Processes the context and question to generate a human-like, detailed answer.
- **Functionality**: 
  - Takes the context and user question as input.
  - Uses advanced generative techniques to create a response that is coherent and contextually appropriate.



If you encounter any issues or have any questions, feel free to reach out. Happy coding!
Gaurav Patidar
gaurav05082002@gmail.com
7689816680
