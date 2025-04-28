import React, { useState, useEffect } from 'react';
import PetCard from './PetCard.tsx';
import './Pets.css'

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
    const [showFilter, setShowFilter] = useState<boolean>(false);
    const [filter, setFilter] = useState({
        species: '',
        breed: '',
        status: 'AVAILABLE'
    });

    // Fetch all pets initially
    useEffect(() => {
        fetchPets();
    }, []);

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

    const fetchFilteredPets = async () => {
        try {
            const query = new URLSearchParams({
                species: filter.species,
                breed: filter.breed,
                status: filter.status
            }).toString();
            const response = await fetch(`http://127.0.0.1:5000/api/pets/search?${query}`);
            const data: Pet[] = await response.json();
            setPets(data);
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
        <PetCard key={pet.id} pet={pet} />
    );

    return (
        <div className="pets-list">
            <h2>Available Pets</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {/* Filter Button */}
            <button onClick={() => setShowFilter(!showFilter)} className="filter-btn">
                Filter Pets
            </button>

            {/* Filter Popup */}
            {showFilter && (
                <div className="filter-popup-overlay">
                    <div className="filter-popup">
                        <h3>Filter Pets</h3>
                        <form onSubmit={handleFilterSubmit}>
                            <div>
                                <label>Species:</label>
                                <input
                                    type="text"
                                    value={filter.species}
                                    onChange={(e) =>
                                        setFilter({ ...filter, species: e.target.value })
                                    }
                                    placeholder="Enter species"
                                />
                            </div>
                            <div>
                                <label>Breed:</label>
                                <input
                                    type="text"
                                    value={filter.breed}
                                    onChange={(e) =>
                                        setFilter({ ...filter, breed: e.target.value })
                                    }
                                    placeholder="Enter breed"
                                />
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