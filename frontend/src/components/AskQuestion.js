import React, { useState } from 'react';
import axios from 'axios';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5000/ask_question', { question });
      setAnswer(response.data.answer);
    } catch (error) {
      alert("Error fetching answer");
    }
  };

  return (
    <div>
      <input 
        type="text" 
        value={question} 
        onChange={(e) => setQuestion(e.target.value)} 
        placeholder="Ask a question" 
      />
      <button onClick={handleSubmit}>Ask</button>
      <p>{answer}</p>
    </div>
  );
};

export default AskQuestion;
