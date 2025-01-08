# ChatPDF

ChatPDF is a web application designed for seamless interaction with PDFs. This project is divided into two parts: the **backend** and the **frontend**, which need to be run in separate terminals.

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

If you encounter any issues or have any questions, feel free to reach out. Happy coding!
Gaurav Patidar
gaurav05082002@gmail.com
7689816680
