import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import PetCard from './PetCard.tsx';
import './Pets.css'

interface Pet {
    id: number;
    name: string;
    age: number;
    species: string;
    breed: string;
    description: string;
    pictureUrl: string;
}

const PetsList: React.FC = () => {
    const { user } = useUser(); // Get user from context
    const [isUserApproved, setIsUserApproved] = useState<boolean>(false);
    const [hasSubmittedQuestionnaire, setHasSubmittedQuestionnaire] = useState<boolean>(false);
    const [pets, setPets] = useState<Pet[]>([]);
    const [error, setError] = useState<string>('');
    const [showFilter, setShowFilter] = useState<boolean>(false);
    const [speciesOptions, setSpeciesOptions] = useState<string[]>([]);
    const [breedOptions, setBreedOptions] = useState<string[]>([]);
    const [filter, setFilter] = useState({
        species: '',
        breed: '',
        status: 'AVAILABLE'
    });

    // Check if user is approved
    useEffect(() => {
        if (user) {
            setIsUserApproved(!!user.approved);
            checkQuestionnaireStatus();
        }
    }, [user]);

    // Check if user has submitted a questionnaire
    const checkQuestionnaireStatus = async () => {
        if (!user) return;
        
        try {
            const response = await fetch('http://localhost:5000/api/questionnaires/hasOpen', {
                method: 'GET',
                credentials: 'include',
            });
            
            if (response.ok) {
                const data = await response.json();
                setHasSubmittedQuestionnaire(data.has_open);
            }
        } catch (err) {
            console.error('Error checking questionnaire status:', err);
        }
    };

    // Fetch all pets initially
    useEffect(() => {
        fetchPets();
    }, []);

    const fetchPets = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/pets');
            const data: Pet[] = await response.json();
            setPets(data);

            // Extract unique species and breeds from the pet data
            const uniqueSpecies = Array.from(new Set(data.map(p => p.species).filter(Boolean)));
            const uniqueBreeds = Array.from(new Set(data.map(p => p.breed).filter(Boolean)));

            setSpeciesOptions(uniqueSpecies);
            setBreedOptions(uniqueBreeds);
            setError(''); // Clear any previous error
        } catch (err) {
            setError('Could not fetch pets. Please try again later.');
            console.error('Error fetching pets:', err);
        }
    };
    

    const fetchFilteredPets = async () => {
        try {
            const query = new URLSearchParams({
                species: filter.species,
                breed: filter.breed,
                status: filter.status
            }).toString();
            const response = await fetch(`http://localhost:5000/api/pets?${query}`);
            const data: Pet[] = await response.json();
            setPets(data);
            setError(''); // Clear any previous error
        } catch (err) {
            setError('Could not fetch filtered pets. Please try again later.');
            console.error('Error fetching filtered pets:', err);
        }
    };

    const handleFilterSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        fetchFilteredPets(); // Fetch filtered pets based on selected filters
        setShowFilter(false); // Close the filter popup
    };

    const renderPetCard = (pet: Pet) => (
        <PetCard 
            key={pet.id} 
            pet={pet}
            isUserApproved={isUserApproved}
            hasSubmittedQuestionnaire={hasSubmittedQuestionnaire}
        />
    );

    return (
        <div className="pets-list">
            <h2>Available Pets</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <button onClick={() => setShowFilter(!showFilter)} className="filter-btn">
                Filter Pets
            </button>

            {showFilter && (
                <div className="filter-popup-overlay">
                    <div className="filter-popup">
                        <h3>Filter Pets</h3>
                        <form onSubmit={handleFilterSubmit}>
                            <div>
                                <label>Species:</label>
                                <select
                                    value={filter.species}
                                    onChange={(e) => setFilter({ ...filter, species: e.target.value })}
                                >
                                    <option value="">-- Select Species --</option>
                                    {speciesOptions.map((option) => (
                                        <option key={option} value={option}>{option}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label>Breed:</label>
                                <select
                                    value={filter.breed}
                                    onChange={(e) => setFilter({ ...filter, breed: e.target.value })}
                                >
                                    <option value="">-- Select Breed --</option>
                                    {breedOptions.map((option) => (
                                        <option key={option} value={option}>{option}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label>Status:</label>
                                <select
                                    value={filter.status}
                                    onChange={(e) =>
                                        setFilter({ ...filter, status: e.target.value })
                                    }
                                >
                                    <option value="AVAILABLE">Available</option>
                                    <option value="ADOPTED">Adopted</option>
                                    <option value="PENDING">Pending</option>
                                </select>
                            </div>
                            <button type="submit">Apply Filters</button>
                            <button type="button" onClick={() => setShowFilter(false)}>Close</button>
                        </form>
                    </div>
                </div>
            )}

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