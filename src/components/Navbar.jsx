import React, { useState, useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";
import zaakyLogo from "../assets/zaakylogo.png";
import { assets } from "../assets/assets";
import { StoreContext } from "../components/context/storeContext";

const Navbar = ({ setShowLogin }) => {
  const location = useLocation();
  const [menu, setMenu] = useState("home");
  const { cartItems } = useContext(StoreContext);

  const totalItems = Object.values(cartItems).reduce(
    (sum, qty) => sum + qty,
    0
  );

  return (
    <nav className="navbar">
      {/* Logo */}
      <Link to="/" onClick={() => setMenu("home")} className="logo-wrapper">
        <img src={zaakyLogo} alt="Zaaky.jo Logo" className="logo-img" />
      </Link>

      {/* Menu */}
      <div className="navbar-menu">
        <Link
          to="/"
          onClick={() => setMenu("home")}
          className={menu === "home" ? "active" : ""}
        >
          Home
        </Link>
        <a
          href="#explore-menu"
          onClick={() => setMenu("menu")}
          className={menu === "menu" ? "active" : ""}
        >
          Menu
        </a>
        <a
          href="#app-download"
          onClick={() => setMenu("mobile-app")}
          className={menu === "mobile-app" ? "active" : ""}
        >
          Mobile App
        </a>
        <a
          href="#footer"
          onClick={() => setMenu("contact-us")}
          className={menu === "contact-us" ? "active" : ""}
        >
          Contact Us
        </a>
      </div>

      {/* Icons */}
      <div className="navbar-icons">
        <img src={assets.search_icon} alt="Search" className="icon" />
        <Link to="/cart" className="navbar-basket">
          <img src={assets.basket_icon} alt="Basket" className="icon" />
          {totalItems > 0 && <div className="dot">{totalItems}</div>}
        </Link>
        <button onClick={() => setShowLogin(true)} className="sign-in-btn">
          Sign In
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
