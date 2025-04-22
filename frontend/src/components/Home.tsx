//import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div>
            <h1>Adopt a pet today!</h1>
            <p>Click on a type of pet to get started.</p>
            <Link to="/login">Login</Link>
        </div>
    );
};
export default Home;