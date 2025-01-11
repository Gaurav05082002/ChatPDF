import React from "react";
import "./Chat.scss";

const MessageBubble = ({ message }) => {
  const isSentByUser = message.sender === "user";

  return (
    <div className={`message-bubble ${isSentByUser ? "sent" : "received"}`}>
      <p>{message.text}</p>
      {/* {message.citations && <h3>{message.citations}</h3>} */}
    </div>
  );
};

export default MessageBubble;
