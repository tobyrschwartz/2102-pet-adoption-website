import React from 'react';
import { useNavigate } from 'react-router-dom';

const Unauthorized: React.FC = () => {
    const navigate = useNavigate();

    const handleGoBack = () => {
        navigate(-1); // Navigate to the previous page
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>403 - Unauthorized</h1>
            <p>You do not have permission to view this page.</p>
            <button onClick={handleGoBack} style={{ padding: '10px 20px', marginTop: '20px' }}>
                Go Back
            </button>
        </div>
    );
};

export default Unauthorized;