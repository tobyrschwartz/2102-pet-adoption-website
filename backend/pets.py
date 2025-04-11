"""The module for managing pet-related API operations."""
from flask import jsonify, request
from enums import PetStatus
from mock_data import get_mock_pet, get_mock_pet_list, BUDDY_PET

def get_all_pets():
    """
    Retrieve all pets in the system.
    
    :return: JSON response with a list of all pets
    """
    # This is a mock function
    pets = get_mock_pet_list()
    return jsonify(pets), 200

def get_pet(pet_id):
    """
    Retrieve a specific pet by its ID.
    
    :param pet_id: ID of the pet to retrieve
    :return: JSON response with the pet details
    """
    # This is a mock function
    pet = get_mock_pet(pet_id)
    return jsonify(pet), 200

def create_pet():
    """
    Create a new pet with the given details from the request.
    
    :return: JSON response with the created pet details
    """
    # This is a mock function
    data = request.json
    new_pet = {
        "pet_id": 3,
        "name": data.get("name"),
        "species": data.get("species"),
        "breed": data.get("breed"),
        "age": data.get("age"),
        "description": data.get("description"),
        "status": PetStatus.AVAILABLE,
        "image_url": data.get("image_url", "")
    }
    return jsonify(new_pet), 201

def update_pet(pet_id):
    """
    Update a pet with the given details from the request.

    :param pet_id: ID of the pet to update
    :return: JSON response with the updated pet details
    """
    # This is a mock function
    data = request.json
    pet_data = BUDDY_PET.copy()
    updated_pet = {
        "pet_id": pet_id,
        "name": data.get("name", pet_data["name"]),
        "species": data.get("species", pet_data["species"]),
        "breed": data.get("breed", pet_data["breed"]),
        "age": data.get("age", pet_data["age"]),
        "description": data.get("description", "Friendly dog"),
        "status": data.get("status", PetStatus.AVAILABLE),
        "image_url": data.get("image_url", "https://example.com/pet1.jpg")
    }
    return jsonify(updated_pet), 200

def delete_pet(pet_id):
    """
    Delete a pet from the system.
    
    :param pet_id: ID of the pet to delete
    :return: JSON response with a success message
    """
    # This is a mock function
    response = {
        "message": "Pet deleted successfully",
        "pet_id": pet_id
    }
    return jsonify(response), 200

def search_pets():
    """
    Search for pets based on query parameters.
    
    :return: JSON response with matching pets
    """
    # This is a mock function
    species = request.args.get("species", "")
    breed = request.args.get("breed", "")
    status = request.args.get("status", PetStatus.AVAILABLE)
    # Modify a copy of the pet data
    pet = get_mock_pet(1, status)
    pet["species"] = species if species else pet["species"]
    pet["breed"] = breed if breed else pet["breed"]
    return jsonify([pet]), 200
