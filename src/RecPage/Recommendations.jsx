import React from "react";
import { useLocation } from "react-router-dom"; // Import useLocation to access the passed state
import "./rec.css";

function Recommendations() {
  const location = useLocation(); // Access location object

  // Accessing recommendations directly from location state
  const recommendations = location.state?.recommendations;

  return (
    <div>
      <h1>Here are some recommendations</h1>
      {recommendations && recommendations.length > 0 ? (
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              <p><strong>Track:</strong> {rec.track_name}</p>
              <p><strong>Artist:</strong> {rec.artists}</p>
              <p><strong>Album:</strong> {rec.album_name}</p>
              <p><strong>Popularity:</strong> {rec.popularity}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No recommendations to display.</p>
      )}
    </div>
  );
}

export default Recommendations;
