import React, { useRef, useEffect, useState } from "react";
import Message from "./comp/message.js";
import MessageInput from "./comp/messageInput.js";
import "./App.css";

//added logo
import plane from "./plane.png"

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! Where would you like to go?" }
  ]);

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const newMessage = { sender: "user", text };
    setMessages([...messages, newMessage]);

    //UPDATED ALL OF THE FOLLOWING ----------------------------------------------

    try { 
      const response = await fetch ("connection to python", { //NEED TO UPDATE THIS TO THE RIGHT LINK FOR THE CONNECTION
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({message: text}),
      });
      const data = await response.json(); 
      setMessages((prev) => [...prev, { sender: "bot", text: data.reply }]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "An error occured, please try again" },
      ]);
    }
  };

  //added the following for the automatic scrolling 
  const messagesEndRef = useRef(null); 
  const scrollDown = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }
  useEffect (() => {
    scrollDown();
  }, [messages]);

  //updated the interface 
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
