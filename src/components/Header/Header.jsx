import React from "react";
import "./Header.css";
import mansafHeader from "../../assets/mansaf-header.png"; // Make sure this path matches your image file

const Header = () => {
  return (
    <div className="header" style={{ backgroundImage: `url(${mansafHeader})` }}>
      <div className="header-contents">
        <h2>Order your Jordanian Zaaky food from here...</h2>
        <p>All Jordanian Arabian lovely food is accessible now</p>
        <button>View Menu</button>
      </div>
    </div>
  );
};

export default Header;
