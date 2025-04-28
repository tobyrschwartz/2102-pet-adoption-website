// src/components/PetCard.tsx
import React from 'react';

interface Pet {
    id: number;
    name: string;
    age: number;
    breed: string;
    temperament: string;
    pictureUrl: string;
}

interface PetCardProps {
    pet: Pet;
}

const PetCard: React.FC<PetCardProps> = ({ pet }) => (
    <div className="pet-card" key={pet.id}>
        <img src={`http://127.0.0.1:5000${pet.pictureUrl}`} alt={pet.name} className="pet-image" />
        <h3>{pet.name}</h3>
        <p>Age: {pet.age}</p>
        <p>Breed: {pet.breed}</p>
        <p>Temperament: {pet.temperament}</p>
        <button className="select-btn">Select Pet</button>
    </div>
);

export default PetCard;
