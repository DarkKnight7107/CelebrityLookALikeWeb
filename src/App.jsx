import React, { useState } from "react";
import "./App.css";
import defaultPerson from "./defaultperson.jpg";

function App() {
  const [username, setUsername] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(defaultPerson);
  const [processedImage, setProcessedImage] = useState(defaultPerson);
  const [loading, setLoading] = useState(false);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setProcessedImage(defaultPerson); // Reset processed image
  };

  const handleSubmitToBackend = async () => {
    if (!selectedFile) {
      alert("Please upload an image first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("username", username);
    formData.append("image", selectedFile);

    try {
      console.log("Sending request to backend...");
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Data from backend:", data);

      if (data.image_url) {
        await waitForImage(data.image_url);
        setProcessedImage(data.image_url); // Set the processed image in second img tag
      } else {
        alert("Error processing image.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const waitForImage = async (imageUrl) => {
    let attempts = 0;
    const maxAttempts = 5;

    while (attempts < maxAttempts) {
      try {
        console.log(`Checking image availability: ${imageUrl} (Attempt ${attempts + 1})`);
        const response = await fetch(imageUrl, { method: "HEAD" });

        if (response.ok) {
          console.log("Processed image is available!");
          return;
        }
      } catch (error) {
        console.log("Image not available yet...");
      }

      await new Promise((resolve) => setTimeout(resolve, 2000)); // Wait 2s before retrying
      attempts++;
    }

    throw new Error("Processed image not available after multiple attempts.");
  };

  return (
    <div className="container">
      {!submitted ? (
        <div className="outermost-div">
          <div className="initial-text-container">
            <h1>Find Out Which Celebrity You Look Like!</h1>
          </div>
          <div className="form-container-div">
            <form onSubmit={handleNameSubmit} className="form-container">
              <h3 className="name-req">What would you like us to call you?</h3>
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
          </div>
        </div>
      ) : (
        <div className="welcome-container">
          <h1>Hello, {username}!</h1>
          <div className="upload-section">
            <div className="image-wrapper">
              {/* User-uploaded image */}
              <div className="image-container">
                <img src={preview} alt="User Preview" className="image-preview" />
              </div>
              {/* Processed image */}
              <div className="image-container">
                <img src={processedImage} alt="Processed Person" className="image-preview" />
              </div>
            </div>
            <input
              type="file"
              accept=".png, .jpg, .jpeg"
              onChange={handleFileChange}
              className="file-input"
            />
            <button onClick={handleSubmitToBackend} className="submit-button">
              {loading ? "Processing..." : "Submit to Backend"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
