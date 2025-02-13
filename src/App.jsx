import React, { useState } from "react";
import "./App.css";
import defaultPerson from "./defaultperson.jpg";

function App() {
  const [username, setUsername] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(defaultPerson);
  
  const handleNameSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };
  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };
  
  return (
    <div className="container">
      {!submitted ? (
        <form onSubmit={handleNameSubmit} className="form-container">
          <input
            type="text"
            placeholder="Enter your name"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="text-input"
            required
          />
          <button type="submit" className="submit-button">Submit</button>
        </form>
      ) : (
        <div className="welcome-container">
          <h1>Hello, {username}!</h1>
          <div className="upload-section">
            <div className="image-wrapper">
              <div className="image-container">
                <img src={preview} alt="User Preview" className="image-preview" />
              </div>
              <div className="image-container">
                <img src={defaultPerson} alt="Default Person" className="image-preview" />
              </div>
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="file-input"
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
