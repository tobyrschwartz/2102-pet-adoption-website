import React, {useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

const Logout: React.FC = () => {
    const { setUser } = useUser();
    const navigate = useNavigate();
    const [message, setMessage] = useState("Logging out...");

    useEffect(() => {
            fetch("http://localhost:5000/logout", {
                method: "POST",
                credentials: "include",
            })
            .then((res) => res.json())
            .then((data) => {
                if (data) {
                    setMessage(data.message);
                    
                  }
            })
            .catch((err) => console.error("Failed to fetch user:", err));
            setUser(null);
        }, []);

    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Logout</h1>
            <p>{message}</p>
            <button onClick={() => navigate('/login')} style={{ padding: '10px 20px', cursor: 'pointer' }}>
                Go to Login
            </button>
        </div>
        
        </div>
    );
};

export default Logout;