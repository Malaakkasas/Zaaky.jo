import React from "react";
import { assets } from "../../assets/assets";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer" id="footer">
      <div className="footer-content">
        {/* Left Section: Logo + Social Icons */}
        <div className="footer-section footer-left">
          <img
            src={assets.logo}
            alt="Zaaky.jo Logo"
            className="footer-logo-img"
          />
          <div className="footer-social-icons">
            <img src={assets.facebook_icon} alt="Facebook" />
            <img src={assets.twitter_icon} alt="Twitter" />
            <img src={assets.linkedin_icon} alt="LinkedIn" />
          </div>
        </div>

        {/* Center Section: Navigation */}
        <div className="footer-section footer-center">
          <h2>COMPANY</h2>
          <ul>
            <li>Home</li>
            <li>About Us</li>
            <li>Delivery</li>
            <li>Privacy Policy</li>
          </ul>
        </div>

        {/* Right Section: Contact Info */}
        <div className="footer-section footer-right">
          <h2>GET IN TOUCH</h2>
          <ul>
            <li>+962-6-123-4567</li>
            <li>contact@zaaky.jo</li>
          </ul>
        </div>
      </div>

      {/* Footer Bottom */}
      <p className="footer-bottom">
        © {new Date().getFullYear()} Zaaky.jo. All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
