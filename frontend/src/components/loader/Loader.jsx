// Loader.js
import React from "react";
import "./Loader.scss"; // You'll add the styles here

const Loader = () => {
  return (
    <div className="loading-dots">
      <div className="loading-dots--dot"></div>
      <div className="loading-dots--dot"></div>
      <div className="loading-dots--dot"></div>
    </div>
  );
};

export default Loader;
