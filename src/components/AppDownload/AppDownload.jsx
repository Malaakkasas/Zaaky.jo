import React from "react";
import { assets } from "../../assets/assets";
import "./AppDownload.css"; // ✅ This links your CSS

const AppDownload = () => {
  return (
    <div className="app-download" id="app-download">
      <h2>
        تجربة أفضل <br />
        <span>Download Zaaky App</span>
      </h2>
      <div className="app-download-platforms">
        <img src={assets.play_store} alt="Download on Play Store" />
        <img src={assets.app_store} alt="Download on App Store" />
      </div>
    </div>
  );
};

export default AppDownload;
