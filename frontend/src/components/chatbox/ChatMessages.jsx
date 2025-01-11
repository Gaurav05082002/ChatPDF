import React from "react";
import MessageBubble from "./MessageBubble";
import "./Chat.scss";

const ChatMessages = ({ messages }) => {
  return (
    <div className="chat-messages">
      {console.log("Messages in ChatMessages:", messages)}
      {messages.map((message, index) => (
        <MessageBubble key={index} message={message} />
      ))}
    </div>
  );
};

export default ChatMessages;
