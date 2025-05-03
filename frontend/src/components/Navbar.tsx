// src/components/Navbar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useUser } from '../context/UserContext'; 
import './Navbar.css';

const Navbar: React.FC = () => {
    const { user } = useUser();
    const location = useLocation();
    const isStaff = user && user.role >= 2;

    const links = [
        { to: '/', label: 'Home' },
        { to: '/pets', label: 'Pet List' },
        !user && { to: '/login', label: 'Login' },
        !user && { to: '/register', label: 'Register' },
        isStaff && { to: '/admin/dashboard', label: 'Admin Dashboard' },
        user && { to: '/logout', label: 'Logout' },
    ].filter(Boolean) as { to: string, label: string }[];

    return (
        <nav className="navbar">
            <ul className="navbar-list">
                {links.map(link => (
                    <li key={link.to}>
                        <Link
                            to={link.to}
                            className={`navbar-link ${
                                location.pathname === link.to ? 'active' : 'inactive'
                            }`}
                        >
                            {link.label}
                        </Link>
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default Navbar;
