import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./rec.css";

function Recommendations() {
  const location = useLocation();
  const { selectedSong } = location.state || {};
  const [recommendations, setRecommendations] = useState([]);

  // Fetch song recommendations from /recommender api
  useEffect(() => {
    if (selectedSong) {
      fetch(
        `http://127.0.0.1:5000/recommender?input_song_name=${encodeURIComponent(
          selectedSong.track_name
        )}&input_artist=${encodeURIComponent(selectedSong.artists)}`
      )
        .then((response) => response.json())
        .then((data) => setRecommendations(data))
        .catch((error) => {
          console.error("Error fetching recommendations:", error);
          alert("Failed to fetch recommendations.");
        });
    }
  }, [selectedSong]);

  return (
    <div>
      <p id="back-home-link">
        <a href="/">back to home</a>
      </p>
      <h1>Here are some recommendations 🎵</h1>
      {recommendations && recommendations.length > 0 ? (
        <ul id="recommendations-list">
          {recommendations.map((rec, index) => (
            <li key={index}>
              <p>
                <strong>Track:</strong> {rec.track_name}
              </p>
              <p>
                <strong>Artist:</strong> {rec.artists}
              </p>
              <p>
                <strong>Album:</strong> {rec.album_name}
              </p>
              <p>
                <strong>Popularity:</strong> {rec.popularity}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p id="no-rec-text">No recommendations to display.</p>
      )}
    </div>
  );
}

export default Recommendations;
