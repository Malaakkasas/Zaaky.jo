import React, { useContext, useState } from "react";
import { StoreContext } from "../../components/context/storeContext";
import { Link } from "react-router-dom";
import "./Cart.css";

const Cart = () => {
  const { cartItems, food_list, removeFromCart } = useContext(StoreContext);
  const [promoCode, setPromoCode] = useState("");
  const [discount, setDiscount] = useState(0);

  const deliveryFee = 2;

  const subtotal = food_list.reduce((total, item) => {
    const quantity = cartItems[item._id] || 0;
    return total + item.price * quantity;
  }, 0);

  const applyPromo = () => {
    if (promoCode.toLowerCase() === "zaaky10") {
      setDiscount(0.1); // 10% off
    } else {
      setDiscount(0);
    }
  };

  const discountedTotal = subtotal - subtotal * discount;
  const grandTotal = discountedTotal + deliveryFee;

  const hasItems = food_list.some((item) => cartItems[item._id] > 0);

  return (
    <div className="cart">
      <div className="cart-items">
        <div className="cart-items-title">
          <p>Item</p>
          <p>Title</p>
          <p>Price</p>
          <p>Quantity</p>
          <p>Total</p>
          <p>Remove</p>
        </div>
        <hr />

        {hasItems ? (
          food_list.map((item) => {
            const quantity = cartItems[item._id];
            if (quantity > 0) {
              return (
                <div className="cart-items-item" key={item._id}>
                  <div className="cart-item-image">
                    <img src={item.image} alt={item.name} />
                  </div>
                  <p>{item.name}</p>
                  <p>{item.price} JOD</p>
                  <p>{quantity}</p>
                  <p>{item.price * quantity} JOD</p>
                  <button
                    className="cart-item-remove"
                    onClick={() => removeFromCart(item._id)}
                  >
                    ✕
                  </button>
                </div>
              );
            }
            return null;
          })
        ) : (
          <p className="empty-cart-message">
            Your cart is empty. Try adding some Mansaf 🍽️
          </p>
        )}

        {hasItems && (
          <>
            <div className="cart-summary">
              <p>Subtotal: {subtotal.toFixed(2)} JOD</p>
              {discount > 0 && (
                <p>Discount: -{(subtotal * discount).toFixed(2)} JOD</p>
              )}
              <p>Delivery Fee: {deliveryFee.toFixed(2)} JOD</p>
              <h3>Total: {grandTotal.toFixed(2)} JOD</h3>
            </div>

            <div className="promo-code">
              <input
                type="text"
                placeholder="Enter promo code"
                value={promoCode}
                onChange={(e) => setPromoCode(e.target.value)}
              />
              <button onClick={applyPromo}>Submit</button>
            </div>

            <Link to="/placeorder">
              <button className="checkout-btn">PROCEED TO CHECKOUT</button>
            </Link>
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
