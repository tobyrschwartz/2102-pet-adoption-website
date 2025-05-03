import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import './AdminManagePets.css';

interface Pet {
    pet_id: number;
    name: string;
    age: number;
    breed: string;
    species: string;
    description: string;
    status: string;
    pictureUrl: string;
}

const AdminManagePets: React.FC = () => {
    const { user, isLoading } = useUser();
    const isStaff = user && user.role >= 2;
    const navigate = useNavigate();
    
    const [pets, setPets] = useState<Pet[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [showAddForm, setShowAddForm] = useState<boolean>(false);
    const [showEditForm, setShowEditForm] = useState<boolean>(false);
    const [currentPet, setCurrentPet] = useState<Pet | null>(null);
    
    // Form state
    const [newPet, setNewPet] = useState({
        name: '',
        age: 0,
        species: '',
        breed: '',
        description: '',
        status: 'AVAILABLE',
        pictureUrl: '',
    });

    useEffect(() => {
        if (isLoading) return;
        if (!isStaff) {
            navigate('/unauthorized');
            return;
        }
        
        fetchPets();
    }, [user, isStaff, navigate]);

    const fetchPets = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://127.0.0.1:5000/api/pets', {
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch pets');
            }
            
            const data = await response.json();
            setPets(data);
            setError(null);
        } catch (err) {
            setError('Error loading pets. Please try again.');
            console.error('Error fetching pets:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setNewPet({
            ...newPet,
            [name]: name === 'age' ? parseInt(value) || 0 : value,
        });
    };

    const handleEditInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        if (!currentPet) return;
        
        const { name, value } = e.target;
        setCurrentPet({
            ...currentPet,
            [name]: name === 'age' ? parseInt(value) || 0 : value,
        });
    };

    const handleAddPet = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/api/pets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(newPet),
            });
            
            if (!response.ok) {
                throw new Error('Failed to add pet');
            }
            
            // Reset form and refresh pets
            setNewPet({
                name: '',
                age: 0,
                species: '',
                breed: '',
                description: '',
                status: 'AVAILABLE',
                pictureUrl: '',
            });
            setShowAddForm(false);
            fetchPets();
        } catch (err) {
            setError('Error adding pet. Please try again.');
            console.error('Error adding pet:', err);
        }
    };

    const handleUpdatePet = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!currentPet) return;
        
        try {
            const response = await fetch(`http://localhost:5000/api/pets/${currentPet.pet_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(currentPet),
            });
            
            if (!response.ok) {
                throw new Error('Failed to update pet');
            }
            
            setShowEditForm(false);
            setCurrentPet(null);
            fetchPets();
        } catch (err) {
            setError('Error updating pet. Please try again.');
            console.error('Error updating pet:', err);
        }
    };

    const handleDeletePet = async (petId: number) => {
        if (!window.confirm('Are you sure you want to delete this pet?')) {
            return;
        }
        
        try {
            const response = await fetch(`http://localhost:5000/api/pets/${petId}`, {
                method: 'DELETE',
                credentials: 'include',
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete pet');
            }
            
            fetchPets();
        } catch (err) {
            setError('Error deleting pet. Please try again.');
            console.error('Error deleting pet:', err);
        }
    };

    const handleUpdateStatus = async (petId: number, newStatus: string) => {
        try {
            const response = await fetch(`http://localhost:5000/api/pets/${petId}/status`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ status: newStatus }),
            });
            
            if (!response.ok) {
                throw new Error('Failed to update pet status');
            }
            
            fetchPets();
        } catch (err) {
            setError('Error updating pet status. Please try again.');
            console.error('Error updating pet status:', err);
        }
    };

    const handleEditPet = (pet: Pet) => {
        setCurrentPet(pet);
        setShowEditForm(true);
    };

    // Admin version of PetCard with admin actions
    const AdminPetCard: React.FC<{ pet: Pet }> = ({ pet }) => (
        <div className="admin-pet-card" key={pet.pet_id}>
            <img 
                src={`http://localhost:5000${pet.pictureUrl}`} 
                alt={pet.name} 
                className="pet-image" 
            />
            <h3>{pet.name}</h3>
            <p>Age: {pet.age}</p>
            <p>Species: {pet.species}</p>
            <p>Breed: {pet.breed}</p>
            <p>Status: {pet.status}</p>
            <p>{pet.description}</p>
            <div className="admin-actions">
                <button 
                    className="edit-btn" 
                    onClick={() => handleEditPet(pet)}
                >
                    Edit
                </button>
                <button 
                    className="delete-btn" 
                    onClick={() => handleDeletePet(pet.pet_id)}
                >
                    Delete
                </button>
                <select
                    value={pet.status}
                    onChange={(e) => handleUpdateStatus(pet.pet_id, e.target.value)}
                    className="status-select"
                >
                    <option value="AVAILABLE">Available</option>
                    <option value="ADOPTED">Adopted</option>
                    <option value="PENDING">Pending</option>
                </select>
            </div>
        </div>
    );

    // Apply scrollable container style directly to the wrapper div
    const scrollableContainerStyle: React.CSSProperties = {
        height: '100vh',
        overflowY: 'auto',
        width: '100%',
        position: 'relative'
    };

    return (
        <div style={scrollableContainerStyle}>
            <div className="admin-pets-container">
                <h1>Manage Pets</h1>
                
                {error && <div className="error-message">{error}</div>}
                
                <button 
                    className="add-pet-btn"
                    onClick={() => setShowAddForm(true)}
                >
                    Add New Pet
                </button>
                
                <div className="admin-pet-list">
                    {loading ? (
                        <p>Loading pets...</p>
                    ) : pets.length > 0 ? (
                        pets.map(pet => <AdminPetCard key={pet.pet_id} pet={pet} />)
                    ) : (
                        <p>No pets found. Add some pets to get started.</p>
                    )}
                </div>
            </div>
            
            {/* Add Pet Form */}
            {showAddForm && (
                <div className="modal-overlay" style={{ overflow: 'auto' }}>
                    <div className="modal-content">
                        <h2>Add New Pet</h2>
                        <form onSubmit={handleAddPet}>
                            <div className="form-group">
                                <label htmlFor="name">Name:</label>
                                <input
                                    type="text"
                                    id="name"
                                    name="name"
                                    value={newPet.name}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="age">Age:</label>
                                <input
                                    type="number"
                                    id="age"
                                    name="age"
                                    value={newPet.age}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="species">Species:</label>
                                <input
                                    type="text"
                                    id="species"
                                    name="species"
                                    value={newPet.species}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="breed">Breed:</label>
                                <input
                                    type="text"
                                    id="breed"
                                    name="breed"
                                    value={newPet.breed}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="description">Description:</label>
                                <textarea
                                    id="description"
                                    name="description"
                                    value={newPet.description}
                                    onChange={handleInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="pictureUrl">Image URL:</label>
                                <input
                                    type="text"
                                    id="pictureUrl"
                                    name="pictureUrl"
                                    value={newPet.pictureUrl}
                                    onChange={handleInputChange}
                                    placeholder="/static/images/pet1.jpg"
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="status">Status:</label>
                                <select
                                    id="status"
                                    name="status"
                                    value={newPet.status}
                                    onChange={handleInputChange}
                                >
                                    <option value="AVAILABLE">Available</option>
                                    <option value="ADOPTED">Adopted</option>
                                    <option value="PENDING">Pending</option>
                                </select>
                            </div>
                            
                            <div className="form-actions">
                                <button type="submit" className="submit-btn">Add Pet</button>
                                <button 
                                    type="button" 
                                    className="cancel-btn"
                                    onClick={() => setShowAddForm(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
            
            {/* Edit Pet Form */}
            {showEditForm && currentPet && (
                <div className="modal-overlay" style={{ overflow: 'auto' }}>
                    <div className="modal-content">
                        <h2>Edit Pet</h2>
                        <form onSubmit={handleUpdatePet}>
                            <div className="form-group">
                                <label htmlFor="edit-name">Name:</label>
                                <input
                                    type="text"
                                    id="edit-name"
                                    name="name"
                                    value={currentPet.name}
                                    onChange={handleEditInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-age">Age:</label>
                                <input
                                    type="number"
                                    id="edit-age"
                                    name="age"
                                    value={currentPet.age}
                                    onChange={handleEditInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-species">Species:</label>
                                <input
                                    type="text"
                                    id="edit-species"
                                    name="species"
                                    value={currentPet.species}
                                    onChange={handleEditInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-breed">Breed:</label>
                                <input
                                    type="text"
                                    id="edit-breed"
                                    name="breed"
                                    value={currentPet.breed}
                                    onChange={handleEditInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-description">Description:</label>
                                <textarea
                                    id="edit-description"
                                    name="description"
                                    value={currentPet.description}
                                    onChange={handleEditInputChange}
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-pictureUrl">Image URL:</label>
                                <input
                                    type="text"
                                    id="edit-pictureUrl"
                                    name="pictureUrl"
                                    value={currentPet.pictureUrl}
                                    onChange={handleEditInputChange}
                                />
                            </div>
                            
                            <div className="form-group">
                                <label htmlFor="edit-status">Status:</label>
                                <select
                                    id="edit-status"
                                    name="status"
                                    value={currentPet.status}
                                    onChange={handleEditInputChange}
                                >
                                    <option value="AVAILABLE">Available</option>
                                    <option value="ADOPTED">Adopted</option>
                                    <option value="PENDING">Pending</option>
                                </select>
                            </div>
                            
                            <div className="form-actions">
                                <button type="submit" className="submit-btn">Update Pet</button>
                                <button 
                                    type="button" 
                                    className="cancel-btn"
                                    onClick={() => {
                                        setShowEditForm(false);
                                        setCurrentPet(null);
                                    }}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminManagePets;