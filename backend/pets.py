"""The module for managing pet-related API operations."""
from flask import jsonify, request
from enums import PetStatus

def get_all_pets():
    """
    Retrieve all pets in the system.
    
    :return: JSON response with a list of all pets
    """
    # This is a mock function
    pets = [
        {
            "pet_id": 1,
            "name": "Buddy",
            "species": "Dog",
            "breed": "Golden Retriever",
            "age": 3,
            "description": "Friendly and energetic medium-sized dog",
            "status": PetStatus.AVAILABLE,
            "image_url": "https://example.com/pet1.jpg"
        },
        {
            "pet_id": 2,
            "name": "Whiskers",
            "species": "Cat",
            "breed": "Tabby",
            "age": 2,
            "description": "Calm and affectionate small-sized cat",
            "status": PetStatus.AVAILABLE,
            "image_url": "https://example.com/pet2.jpg"
        }
    ]
    return jsonify(pets), 200

def get_pet(pet_id):
    """
    Retrieve a specific pet by its ID.
    
    :param pet_id: ID of the pet to retrieve
    :return: JSON response with the pet details
    """
    # This is a mock function
    pet = {
        "pet_id": pet_id,
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "description": "Friendly and energetic medium-sized dog",
        "status": PetStatus.AVAILABLE,
        "image_url": "https://example.com/pet1.jpg"
    }
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
    updated_pet = {
        "pet_id": pet_id,
        "name": data.get("name", "Buddy"),
        "species": data.get("species", "Dog"),
        "breed": data.get("breed", "Golden Retriever"),
        "age": data.get("age", 3),
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
    # In a real implementation, we would parse query parameters
    # like species, breed, age range, etc.
    species = request.args.get("species", "")
    breed = request.args.get("breed", "")
    status = request.args.get("status", PetStatus.AVAILABLE)
    # Just mocked results for now
    pets = [
        {
            "pet_id": 1,
            "name": "Buddy",
            "species": "Dog" if species == "Dog" or not species else species,
            "breed": "Golden Retriever" if breed == "Golden Retriever" or not breed else breed,
            "age": 3,
            "description": "Friendly and energetic medium-sized dog",
            "status": status,
            "image_url": "https://example.com/pet1.jpg"
        }
    ]
    return jsonify(pets), 200
