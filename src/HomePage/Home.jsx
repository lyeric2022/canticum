import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./homepage.css";

function Home() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedSong, setSelectedSong] = useState(null);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      alert("Please enter a song name.");
      return;
    }
    const response = await fetch(
      `http://127.0.0.1:5000/search?query=${encodeURIComponent(searchQuery)}`
    );
    const data = await response.json();
    setSearchResults(data.results);
  };

  const handleSelectSong = (song) => {
    setSelectedSong(song);
    console.log(selectedSong);
  };

  const handleRecommendations = () => {
    if (!selectedSong) {
      alert("Please hit ENTER or select a song.");
      return;
    }
    navigate("/recommendations", { state: { selectedSong } });
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch(); // Trigger search when Enter key is pressed
    }
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
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <div id="go-button">
          <button onClick={handleRecommendations}>Go!</button>
        </div>
      </div>
      {searchResults && searchResults.length > 0 ? (
        <ul id="search-results-list">
          {!selectedSong ? (
            <h2>Please select a song:</h2>
          ) : (
            <h2>
              Currently selected: {selectedSong.track_name} by{" "}
              {selectedSong.artists}
            </h2>
          )}
          {searchResults.map((song) => (
            <li
              className="search-result"
              key={song.track_id}
              onClick={() => handleSelectSong(song)}
            >
              {song.track_name} - {song.artists}
            </li>
          ))}
        </ul>
      ) : (
        <p>No matching songs found.</p>
      )}
    </div>
  );
}

export default Home;
