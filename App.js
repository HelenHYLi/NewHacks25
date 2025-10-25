import React, { useState } from "react";
import Message from "./comp/message.js";
import MessageInput from "./comp/messageInput.js";
import "./App.css";
import logo from './logo.svg'; //to change!!!

//import { GoogleGenerativeAI } from "@google/generative-ai"; //to add!!!

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! Where would you like to go?" }
  ]);

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const newMessage = { sender: "user", text };
    setMessages([...messages, newMessage]);

    if (text == "hi") {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "how are you doing?" }
      ])
    } else {

       //send user input to back end and get a response 
      try { 
        const response = await fetch ("connection to python", {
          method: "POST",
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

      // (Optional) Fake bot response
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "Got it! You said: " + text }
        ]);
      }, 800);
    }
  };

  return ( 
    <div className="chat-container">
      
      <div className="image">
        <img src={logo} className="App-logo" alt="logo" />
      </div>

      <div className="message-list">
        {messages.map((msg, i) => (
          <Message key={i} sender={msg.sender} text={msg.text} />
        ))}
      </div>

      <MessageInput onSend={handleSend} />
    </div>
    
  );
}

export default App;
