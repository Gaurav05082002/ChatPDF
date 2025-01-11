import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.scss";

const FileUpload = () => {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setPdfFiles((prevFiles) => [...prevFiles, ...files]);
  };

  const handleSubmit = async () => {
    if (pdfFiles.length === 0) {
      alert("Please upload at least one file.");
      return;
    }
    console.log("Uploaded files:", pdfFiles);

    const formData = new FormData();
    pdfFiles.forEach((file) => {
      formData.append("pdf_files", file);
    });
    setIsProcessing(true);
    try {
      const result = await axios.post("http://localhost:5000/upload_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(result.data.message);
      setPdfFiles([]); // Clear files on success
    } catch (error) {
      alert("Error uploading files");
    } finally {
      setIsProcessing(false);
    }
  };

  const removeFile = (index) => {
    setPdfFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  return (
    <div className="file-upload-container">
      <div className="file-drop-area">
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          accept=".pdf"
          className="file-input"
        />
        <div className="file-drop-text">
          <span>📤</span>
          <p>Drag & drop any file here</p>
          <p>
            or <span className="browse-link">browse file</span> 
          </p>
        </div>
      </div>

      {pdfFiles.length > 0 && (
        <ul className="file-list">
          {pdfFiles.map((file, index) => (
            <li key={index} className="file-item">
              <span>{file.name}</span>
              <button className="remove-file-btn" onClick={() => removeFile(index)}>
                ✖
              </button>
            </li>
          ))}
        </ul>
      )}

      <button className="upload-button" onClick={handleSubmit} disabled={isProcessing}>
        {isProcessing ? "Processing..." : "Submit & Process"}
      </button>
    </div>
  );
};

export default FileUpload;
