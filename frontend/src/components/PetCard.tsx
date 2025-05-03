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
    isUserApproved?: boolean;
    hasSubmittedQuestionnaire?: boolean;
}

const PetCard: React.FC<PetCardProps> = ({ 
    pet, 
    isUserApproved = false, 
    hasSubmittedQuestionnaire = false 
}) => {
    const navigate = useNavigate();

    const handleSelect = () => {
        if (!isUserApproved) {
            if (hasSubmittedQuestionnaire) {
                alert('Your application is still under review. You will be able to select pets once approved.');
            } else {
                alert('Please complete the adoption questionnaire before selecting a pet.');
                navigate('/questionnaire');
            }
            return;
        }
        
        // If approved, proceed with pet selection
        navigate('/confirm', { state: { pet } });
    };

    return (
        <div className="pet-card" key={pet.id}>
            <img src={`http://127.0.0.1:5000${pet.pictureUrl}`} alt={pet.name} className="pet-image" />
            <h3>{pet.name}</h3>
            <p>Age: {pet.age}</p>
            <p>Breed: {pet.breed}</p>
            <p>{pet.description}</p>
            
            <button 
                className="select-btn" 
                onClick={handleSelect}
            >
                {isUserApproved ? "Select Pet" : "Express Interest"}
            </button>
            
            {!isUserApproved && (
                <div style={{ 
                    marginTop: '10px', 
                    fontSize: '0.8em', 
                    padding: '5px',
                    borderRadius: '5px',
                    backgroundColor: hasSubmittedQuestionnaire ? '#e6f7ff' : '#ffffcc',
                    color: '#333'
                }}>
                    {hasSubmittedQuestionnaire ? 
                        "Your application is under review" : 
                        "Complete questionnaire to adopt"}
                </div>
            )}
        </div>
    );
};

export default PetCard;