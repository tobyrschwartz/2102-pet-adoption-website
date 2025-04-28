// src/components/Navbar.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { useUser } from '../context/UserContext'; 
import './Navbar.css'

const Navbar: React.FC = () => {

    const { user } = useUser();
    const isStaff = user && user.role >= 2;
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to = "/pets">Pet List</Link></li>
                {!user && <li><Link to="/login">Login</Link></li>}
                {!user && <li><Link to="/register">Register</Link></li>}
                {user && <li><Link to="/logout">Logout</Link></li>}
                {isStaff && <li><Link to="/admin/dashboard">Admin Dashboard</Link></li>}
            </ul>
        </nav>
    );
};

export default Navbar;