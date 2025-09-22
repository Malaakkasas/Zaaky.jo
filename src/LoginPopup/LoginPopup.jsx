import React, { useState } from "react";
import assets from "../assets/assets";
import "./LoginPopup.css";

const LoginPopup = ({ setShowLogin }) => {
  const [currState, setCurrState] = useState("Login");

  return (
    <div className="login-popup">
      <div className="login-popup-container">
        <img
          src={assets.cross_icon}
          alt="Close"
          className="login-popup-close"
          onClick={() => setShowLogin(false)}
        />

        <h2 className="login-popup-title">{currState}</h2>

        <div className="login-popup-inputs">
          {currState === "Sign Up" && (
            <input type="text" placeholder="Your name" required />
          )}
          <input type="email" placeholder="Your email" required />
          <input type="password" placeholder="Password" required />
        </div>

        <button className="login-popup-submit">
          {currState === "Sign Up" ? "Create account" : "Login"}
        </button>

        <div className="login-popup-condition">
          <input type="checkbox" required />
          <p>
            By continuing, I agree to the{" "}
            <span className="link-text">terms of use</span> &{" "}
            <span className="link-text">privacy policy</span>.
          </p>
        </div>

        <div className="login-popup-create-account">
          {currState === "Login" ? (
            <p>
              Create a new account?{" "}
              <span onClick={() => setCurrState("Sign Up")}>Click here</span>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <span onClick={() => setCurrState("Login")}>Login here</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPopup;
