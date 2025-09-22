import React, { useContext, useState } from "react";
import "./FoodItem.css";
import { assets } from "../../assets/assets";
import { StoreContext } from "../context/storeContext";

const FoodItem = ({
  id,
  name,
  price,
  description,
  image,
  rating = 0,
  showQuantity = true,
}) => {
  const { cartItems, addToCart, removeFromCart } = useContext(StoreContext);
  const [userRating, setUserRating] = useState(rating);

  const handleRatingClick = (value) => {
    setUserRating(value);
    // Optional: send to backend or context
    // e.g., updateRating(id, value);
  };

  return (
    <div className="food-item">
      <div className="food-item-img-container">
        <img
          className="food-item-image"
          src={image}
          alt={name || "Food item"}
        />
        {showQuantity && (
          <div className="food-item-quantity">
            <img
              src={assets.remove_icon_red}
              alt="Remove"
              onClick={() => removeFromCart(id)}
            />
            <span>{cartItems[id] || 0}</span>
            <img
              src={assets.add_icon_green}
              alt="Add"
              onClick={() => addToCart(id)}
            />
          </div>
        )}
      </div>

      <div className="food-item-info">
        <div className="food-item-name-rating">
          <p>{name}</p>
          <div className="food-item-stars">
            {[...Array(5)].map((_, i) => (
              <span
                key={i}
                className={i < userRating ? "star filled" : "star"}
                onClick={() => handleRatingClick(i + 1)}
              >
                ★
              </span>
            ))}
          </div>
        </div>
        <p className="food-item-desc">{description}</p>
        <p className="food-item-price">${price}</p>
      </div>
    </div>
  );
};

export default FoodItem;
