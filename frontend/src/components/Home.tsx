//import React from "react";
import { Link } from "react-router-dom";
const Home = () => {
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>Welcome to Pet Adoption</h1>
            <p>Your journey to finding a new friend starts here.</p>
            <Link to="/login" style={{ textDecoration: "none" }}>
                <button style={{ 
                    borderRadius: "20px", 
                    padding: "10px 20px", 
                    backgroundColor: "#007BFF", 
                    color: "white", 
                    border: "none", 
                    cursor: "pointer" 
                }}>
                    Login
                </button>
            </Link>
        </div>
    );
};

export default Home;
