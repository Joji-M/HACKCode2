import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');





function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [temp, setTemp] = useState("");
  const [humidity, setHumidity] = useState("");
  const [light, setLight] = useState("");
  const [ultrasonic, setUltrasonic] = useState("");
  const [inputData, setInputData] = useState(""); // Add to top with other state

  const handleSend = () => {
    socket.emit('send_to_pico', inputData);
    setInputData(""); // clear input
  };

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    socket.on('temp', (data) => setTemp(data));
    socket.on('humidity', (data) => setHumidity(data));
    socket.on('light', (data) => setLight(data));
    socket.on('ultrasonic', (data) => setUltrasonic(data));
    return () => {
      socket.off('picture_taken');
      socket.off('temp');
      socket.off('humidity');
      socket.off('light');
      socket.off('ultrasonic');
    };
  }, []);

  return (
  
    <>
    <div className="app">
      <h2>Sensor Data</h2>
      <p> Temp: {temp} °C</p>
      <p> Humidity: {humidity} %</p>
      <p> Light: {light}</p>
      <p> Distance: {ultrasonic}</p>
    </div>
    <div className="input-box" style={{ marginTop: '20px' }}>
      <input
      type="text"
      value={inputData}
      onChange={(e) => setInputData(e.target.value)}
      placeholder="Enter message to send to Pico"
      style={{ padding: '8px', marginRight: '8px' }}
    />
  <button onClick={handleSend} style={{ padding: '8px 12px' }}>
    Send
  </button>
</div>
</>
    
  );
}

export default App;
