"""The module for managing pet-related operations."""
from flask import jsonify
from enums import PetStatus
from mock_data import get_mock_pet, get_mock_pet_list

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
    # This is a mock function
    new_pet = {
        "name": pet_data.get("name"),
        "species": pet_data.get("species"),
        "breed": pet_data.get("breed"),
        "age": pet_data.get("age"),
        "description": pet_data.get("description"),
        "status": pet_data.get("status", PetStatus.AVAILABLE)
    }
    return jsonify(new_pet), 201

def get_pet(pet_id):
    """
    Retrieve a specific pet by its ID.
    
    :param pet_id: ID of the pet to retrieve
    :return: JSON response with the pet details
    """
    # This is a mock function
    pet = get_mock_pet(pet_id)
    return jsonify(pet), 200

def get_all_pets():
    """
    Retrieve all pets.
    
    :return: JSON response with a list of pets
    """
    # This is a mock function
    pets = get_mock_pet_list()
    return jsonify(pets), 200

def get_pets_by_status(status):
    """
    Retrieve pets by their status.
    
    :param status: Status of the pets to retrieve
    :return: JSON response with a list of pets matching the status
    """
    # This is a mock function
    pets = [get_mock_pet(1, status)]
    return jsonify(pets), 200

def update_pet_status(pet_id, status):
    """
    Update the status of a pet.
    
    :param pet_id: ID of the pet to update
    :param status: New status for the pet
    :return: JSON response with the updated pet details
    """
    # This is a mock function
    updated_pet = {
        "pet_id": pet_id,
        "status": status
    }
    return jsonify(updated_pet), 200
