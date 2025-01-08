import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [pdfFiles, setPdfFiles] = useState(null);

  const handleFileChange = (event) => {
    setPdfFiles(event.target.files);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    Array.from(pdfFiles).forEach(file => {
      formData.append("pdf_files", file);
    });

    try {
      const result = await axios.post('http://localhost:5000/upload_pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert(result.data.message);
    } catch (error) {
      alert("Error uploading files");
    }
  };

  return (
    <div>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleSubmit}>Submit & Process</button>
    </div>
  );
};

export default FileUpload;
