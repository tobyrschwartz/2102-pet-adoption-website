"""The module for managing pet-related operations."""
import sqlite3
from flask import jsonify
from enums import PetStatus

def get_db_connection():
    """
    Create a database connection to the SQLite database.
    :return: SQLite connection object
    """
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def create_pet(pet_data):
    """
    Create a new pet with the given details.
    
    :param pet_data: Dictionary containing pet details with the following keys:
                    - name: Name of the pet
                    - species: Species of the pet (e.g., Dog, Cat)
                    - breed: Breed of the pet
                    - age: Age of the pet in years
                    - description: Description including size and other details
                    - status: (optional) Adoption status of the pet
    :return: JSON response with the created pet details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pets (name, species, breed, age, description, status, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (pet_data['name'], pet_data['species'], pet_data['breed'], pet_data['age'],
            pet_data['description'],
            pet_data.get('status', PetStatus.AVAILABLE), pet_data.get('image_url', '')))
    conn.commit()
    pet_id = cursor.lastrowid
    conn.close()
    new_pet = {'pet_id': pet_id}

    return jsonify(new_pet), 201

def delete_pet(pet_id):
    """
    Delete a pet with the given ID.
    
    :param pet_id: ID of the pet to delete
    :return: JSON response indicating success or failure
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE pet_id = ?', (pet_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Pet not found"}), 404
    return jsonify({"message": "Pet deleted successfully"}), 200

def get_pet(pet_id):
    """
    Retrieve a specific pet by its ID.
    
    :param pet_id: ID of the pet to retrieve
    :return: JSON response with the pet details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets WHERE pet_id = ?', (pet_id,))
    pet = cursor.fetchone()
    conn.close()
    if pet is None:
        return jsonify({"error": "Pet not found"}), 404
    pet = dict(pet)
    return jsonify(pet), 200

def get_all_pets():
    """
    Retrieve all pets.
    
    :return: JSON response with a list of pets
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets')
    pets = cursor.fetchall()
    conn.close()
    if not pets:
        return jsonify({"error": "No pets found"}), 404
    # Convert pets to a list of dictionaries
    pets = [dict(pet) for pet in pets]
    return jsonify(pets), 200

def update_pet_status(pet_id, status):
    """
    Update the status of a pet.
    
    :param pet_id: ID of the pet to update
    :param status: New status for the pet
    :return: JSON response with the updated pet details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE pets SET status = ? WHERE pet_id = ?', (status, pet_id))
    conn.commit()
    cursor.execute('SELECT * FROM pets WHERE pet_id = ?', (pet_id,))
    updated_pet = cursor.fetchone()
    conn.close()
    if updated_pet is None:
        return jsonify({"error": "Pet not found"}), 404
    updated_pet = dict(updated_pet)
    return jsonify(updated_pet), 200

def update_pet(pet_data):
    """
    Update a pet with the given details from the request.

    :param pet_id: ID of the pet to update
    :return: JSON response with the updated pet details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pets SET (name, species, breed, age, description, status)
        VALUES (?, ?, ?, ?, ?, ?) WHERE pet_id = ?
    ''', (pet_data['name'], pet_data['species'], pet_data['breed'], pet_data['age'],
            pet_data['description'], pet_data.get('status', PetStatus.AVAILABLE),
            pet_data['pet_id']))
    conn.commit()
    cursor.execute('SELECT * FROM pets WHERE pet_id = ?', (pet_data['pet_id'],))
    updated_pet = cursor.fetchone()
    conn.close()
    if updated_pet is None:
        return jsonify({"error": "Pet not found"}), 404
    updated_pet = dict(updated_pet)
    return jsonify(updated_pet), 200

def search_pets(species: str = "", breed: str = "", status: PetStatus = PetStatus.AVAILABLE):
    """
    Search for pets based on query parameters.
    
    :return: JSON response with matching pets
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM pets WHERE 1=1"
    params = []
    if species:
        query += " AND species = ?"
        params.append(species)
    if breed:
        query += " AND breed = ?"
        params.append(breed)
    if status:
        query += " AND status = ?"
        params.append(status.value)
    cursor.execute(query, params)
    pets = cursor.fetchall()
    conn.close()
    if not pets:
        return jsonify({"error": "No pets found meeting that criteria!"}), 404
    # Convert pets to a list of dictionaries
    pets = [dict(pet) for pet in pets]

    return jsonify(pets), 200

def get_breeds():
    """
    Retrieve all unique breeds from the database.
    
    :return: JSON response with a list of unique breeds
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT breed FROM pets')
    breeds = cursor.fetchall()
    conn.close()
    if not breeds:
        return jsonify({"error": "No breeds found"}), 404
    # Convert breeds to a list of strings
    breeds = [breed[0] for breed in breeds]
    return jsonify(breeds), 200
def get_species():
    """
    Retrieve all unique species from the database.

    :return: JSON response with a list of unique species
    :raises: 404 if no species are found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT species FROM pets')
    species = cursor.fetchall()
    conn.close()
    if not species:
        return jsonify({"error": "No species found"}), 404
    # Convert species to a list of strings
    species = [specie[0] for specie in species]
    return jsonify(species), 200
