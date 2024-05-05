import React from "react";
import { useNavigate } from "react-router-dom";
import "./homepage.css";

function Home() {
  const navigate = useNavigate();
  const recommend = () => {
    navigate(`/recommendations`);
  };
  return (
    <div id="main">
      <div id="title">
        <p>Canticum</p>
      </div>
      <div id="input-box">
        <input id="song-input" type="text" placeholder="search for a song" />
        <div id="go-button">
          <button onClick={() => recommend()}>go!</button>
        </div>
      </div>
      <div id="desc-div">
        <h1>about Cancticum</h1>
        <text>description</text>
        <h1>directions</h1>
        <text>directions</text>
      </div>
    </div>
  );
}

export default Home;
