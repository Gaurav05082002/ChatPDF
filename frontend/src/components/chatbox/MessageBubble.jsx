// MessageBubble.jsx
import React from "react";
import Loader from "../loader/Loader"; // Import the Loader component
import "./Chat.scss";

const MessageBubble = ({ message, isLoading }) => {
  const isSentByUser = message.sender === "user";

  return (
    <div className={`message-bubble ${isSentByUser ? "sent" : "received"}`}>
      {isLoading ? (
        <Loader /> // Show loader if message is being prepared
      ) : (
        <p>{message.text}</p> // Show message when ready
      )}
    </div>
  );
};

export default MessageBubble;
