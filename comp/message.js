import React from "react";

function Message({ sender, text }) {
  const isUser = sender === "user";
  return (
    <div className={`message ${isUser ? "user" : "bot"}`}>
      <div className="bubble">{text}</div>
    </div>
  );
}

export default Message;
