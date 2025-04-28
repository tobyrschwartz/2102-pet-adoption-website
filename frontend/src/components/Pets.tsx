// src/components/PetsList.tsx
import React, { useState, useEffect } from 'react';

interface Pet {
    id: number;
    name: string;
    age: number;
    breed: string;
    temperament: string;
    pictureUrl: string;
}

const PetsList: React.FC = () => {
    const [pets, setPets] = useState<Pet[]>([]);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        const fetchPets = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/pets');
                const data: Pet[] = await response.json();
                setPets(data);
            } catch (err) {
                setError('Could not fetch pets. Please try again later.');
                console.error('Error fetching pets:', err);
            }
        };

        fetchPets();
    }, []);

    const renderPetCard = (pet: Pet) => (
        <div className="pet-card" key={pet.id}>
            <img src={`http://127.0.0.1:5000${pet.pictureUrl}`} alt={pet.name} className="pet-image" />
            <h3>{pet.name}</h3>
            <p>Age: {pet.age}</p>
            <p>Breed: {pet.breed}</p>
            <p>Temperament: {pet.temperament}</p>
            <button className="select-btn">Select Pet</button>
        </div>
    );

    return (
        <div className="pets-list">
            <h2>Available Pets</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div className="pet-list-container">
                {pets.length > 0 ? (
                    pets.map(renderPetCard)
                ) : (
                    <p>No pets available at this moment.</p>
                )}
            </div>
        </div>
    );
};

export default PetsList;