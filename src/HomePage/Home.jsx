import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./homepage.css";

function Home() {
  const navigate = useNavigate();
  const [songName, setSongName] = useState(""); // To hold the song name

  const recommend = () => {
    if (!songName.trim()) {
      alert("Please enter a song name.");
      return;
    }
    // Perform a fetch request to the Flask API
    fetch(
      `http://localhost:5000/recommender?input_song_name=${encodeURIComponent(
        songName
      )}&num_recommendations=5`
    )
      .then((response) => response.json())
      .then((data) => {
        // Handle the response data from the Flask API here
        console.log(data); // Log data or set it to state
        navigate("/recommendations", { state: { recommendations: data } });
      })
      .catch((error) => {
        console.error("Error fetching recommendations:", error);
        alert("Failed to fetch recommendations.");
      });
  };

  return (
    <div id="main">
      <div id="title">
        <h1>Canticum</h1>
      </div>
      <div id="input-box">
        <input
          id="song-input"
          type="text"
          placeholder="search for a song"
          value={songName}
          onChange={(e) => setSongName(e.target.value)}
        />
        <div id="go-button">
          <button onClick={recommend}>go!</button>
        </div>
      </div>
    </div>
  );
}

export default Home;
