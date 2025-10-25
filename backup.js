import React, { useState, useRef } from "react";
import logo from './logo.svg';
import './App.css';
import './comp/message.js'
import styles from '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';

import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

function MyButton() {
  return (
    <button>Find the best price and date!</button>
  )
}

function App() {
  // Track what the user types
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");

  // Store Gemini’s results
  const [analysis, setAnalysis] = useState(null);

  // Loading & error state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleMessage = (text) => {
    
  }
  const handlenAnalyze = async() => {
    //call the back end 
  }

  const [messages, setMessages] = useState([
    { message: "Hello! How can I help you?", sender: "Gemini" }
  ]);

  const handleSend = (message) => {
    const newMessage = { message, sender: "user", direction: "outgoing" };
    setMessages([...messages, newMessage]);
  };

  return ( 
     <div className="App">
     <header className="App-header">
       <MyButton />
       <img src={logo} className="App-logo" alt="logo" />
       <p>
         Edit <code>src/App.js</code> and save to reload.
       </p>
       <a
         className="App-link"
         href="https://reactjs.org"
         target="_blank"
         rel="noopener noreferrer"
       >
         Learn React
       </a>
     </header>
   </div>
    
  );
}

export default App;