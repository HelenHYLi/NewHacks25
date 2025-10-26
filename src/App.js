import React, { useRef, useEffect, useState } from "react";
import Message from "./comp/message.js";
import MessageInput from "./comp/messageInput.js";
import "./App.css";

import plane from "./plane.png"

function App() {
  //default message 
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! Where would you like to go?" }
  ]);

  //handle the sending and recieving of messages 
  const handleSend = async (text) => {
    if (!text.trim()) return;

    //takes user input 
    const newMessage = { sender: "user", text };
    setMessages([...messages, newMessage]);

    //sends user input to the backend and retrieves response to display 
    const response = await fetch ("connection to python", //replace "connection to python" with the connection link to the backend
      { 
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({message: text}),
    });
  };

  //automatic scrolling down
  const messagesEndRef = useRef(null); 
  const scrollDown = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }
  useEffect (() => {
    scrollDown();
  }, [messages]);

  return ( 
    <div className="App-header">
      <div className="chat-container">
        <h1 className="App-name">Flightopolis</h1>
        <img src= {plane} className="App-logo" alt="logo" />
        <div className="message-list">
          {messages.map((msg, i) => (
            <Message key={i} sender={msg.sender} text={msg.text} />
          ))}
          <div ref={messagesEndRef}/> 
        </div>
        <MessageInput onSend={handleSend} />
      </div>
    </div>
  );
}

export default App;
