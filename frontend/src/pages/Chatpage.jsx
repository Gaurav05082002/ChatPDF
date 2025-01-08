import React, { useState } from "react";
import ChatHeader from "../components/chatbox/ChatHeader";
import ChatMessages from "../components/chatbox/ChatMessages";
import ChatInput from "../components/chatbox/ChatInput";
import FileUpload from "../components/fileupload/FileUpload";

// import "../components/Chat.scss"

const Chatpage = () => {
    const [messages, setMessages] = useState([
      { sender: "bot", text: "Hello! Please upload pdf and let's chat?" },
    ]);
  
    const handleNewMessage = (newMessage) => {
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    };
  
    return (
      <div className="chat-container">
        <ChatHeader />
        <FileUpload/>
        <ChatMessages messages={messages} />
        <ChatInput onNewMessage={handleNewMessage} />
      </div>
    );
  };

export default Chatpage;
