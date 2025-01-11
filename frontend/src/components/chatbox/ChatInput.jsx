
import React, { useState } from "react";
import axios from "axios";
import "./Chat.scss";
import Loader from "../loader/Loader";

const ChatInput = ({ onNewMessage }) => {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false); 

  const handleSendMessage = async () => {
    if (input.trim()) {
      // Add user message
      onNewMessage({ sender: "user", text: input, citations: "" });
      setIsLoading(true); // Start loading
  
      try {
        // Send question to backend
        const response = await axios.post("http://localhost:5000/ask_question", {
          question: input.trim(),
        });
  
        // Extract answer and citations
        const { answer, citations } = response.data;
  
        // Ensure `answer` and `citations` are strings
        const formattedAnswer = typeof answer === "string" ? answer : JSON.stringify(answer);
        const formattedCitations = typeof citations === "string" ? citations : JSON.stringify(citations);
  
        // Add bot's response
        onNewMessage({
          sender: "bot",
          text: formattedAnswer,
          citations: formattedCitations,
        });
      } catch (error) {
        onNewMessage({
          sender: "bot",
          text: "Error fetching answer.",
          citations: "No citations available",
        });
      } finally {
        setIsLoading(false); // Stop loading
      }
  
      setInput(""); // Clear input field
    }
  };
  
  

  return (
    <div className="chat-input">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a question..."
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSendMessage(); // Trigger send message when Enter is pressed
          }
        }}
      />
      <div className={`message-bubble `}>
            {isLoading ? (
              <Loader /> // Show loader if message is being prepared
            ) : (
           <></>   // message when ready
            )}
          </div>
      <button onClick={handleSendMessage} 
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSendMessage(); // Trigger send message when Enter is pressed
          }
        }}
      >Send</button>
    </div>
  );
};

export default ChatInput;
