// src/pages/ConfirmPet.tsx
//import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ConfirmPet.css';

const ConfirmPet = () => {
    const { state } = useLocation();
    const navigate = useNavigate();
    const pet = state?.pet;

    if (!pet) {
        return <p>Pet data is missing. Please go back and select a pet.</p>;
    }

    const handleConfirm = () => {
        // Handle submission logic here
        alert(`You have selected ${pet.name} for adoption!`);
        navigate('/'); // Redirect to home or another page
    };

    return (
        <div className="confirm-container">
            <div className="confirm-card">
                <img src={`http://127.0.0.1:5000${pet.pictureUrl}`} alt={pet.name} className="confirm-image" />
                <h2>Confirm Adoption</h2>
                <p><strong>Name:</strong> {pet.name}</p>
                <p><strong>Age:</strong> {pet.age}</p>
                <p><strong>Breed:</strong> {pet.breed}</p>
                <p>{pet.description}</p>
                <button className="confirm-btn" onClick={handleConfirm}>Confirm</button>
                <button className="cancel-btn" onClick={() => navigate(-1)}>Cancel</button>
            </div>
        </div>
    );
};

export default ConfirmPet;
