// src/components/PetCard.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Pets.css';

interface Pet {
    id: number;
    name: string;
    age: number;
    breed: string;
    description: string;
    pictureUrl: string;
}

interface PetCardProps {
    pet: Pet;
}

const PetCard: React.FC<PetCardProps> = ({ pet }) => {
    const navigate = useNavigate();

    const handleSelect = () => {
        navigate('/confirm', { state: { pet } });
    };

    return (
        <div className="pet-card" key={pet.id}>
            <img src={`http://127.0.0.1:5000${pet.pictureUrl}`} alt={pet.name} className="pet-image" />
            <h3>{pet.name}</h3>
            <p>Age: {pet.age}</p>
            <p>Breed: {pet.breed}</p>
            <p>{pet.description}</p>
            <button className="select-btn" onClick={handleSelect}>Select Pet</button>
        </div>
    );
};

export default PetCard;

