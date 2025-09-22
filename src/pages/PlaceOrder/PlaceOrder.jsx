import React, { useContext, useState } from "react";
import { StoreContext } from "../../components/context/storeContext";
import "./PlaceOrder.css";

const PlaceOrder = () => {
  const { cartItems, food_list } = useContext(StoreContext);
  const [promoCode, setPromoCode] = useState("");
  const [discount, setDiscount] = useState(0);

  const deliveryFee = 2;

  // Calculate subtotal manually
  const subtotal = food_list.reduce((total, item) => {
    const quantity = cartItems[item._id] || 0;
    return total + item.price * quantity;
  }, 0);

  const discountedTotal = subtotal - subtotal * discount;
  const grandTotal = discountedTotal + deliveryFee;

  const applyPromo = () => {
    if (promoCode.toLowerCase() === "zaaky10") {
      setDiscount(0.1);
    } else {
      setDiscount(0);
    }
  };

  return (
    <div className="place-order">
      <div className="place-order-left">
        <p className="title">Delivery Information</p>
        <div className="multi-fields">
          <input type="text" placeholder="First name" />
          <input type="text" placeholder="Last name" />
        </div>
        <input type="email" placeholder="Email address" />
        <input type="text" placeholder="Street" />
        <div className="multi-fields">
          <input type="text" placeholder="City" />
          <input type="text" placeholder="Zip code" />
        </div>
        <div className="multi-fields">
          <input type="text" placeholder="Country" />
          <input type="text" placeholder="Phone" />
        </div>
      </div>

      <div className="place-order-right">
        <p className="title">Cart Totals</p>
        <div className="summary-details">
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
          <button onClick={applyPromo}>Apply</button>
        </div>

        <button className="checkout-btn">PROCEED TO PAYMENT</button>
      </div>
    </div>
  );
};

export default PlaceOrder;
