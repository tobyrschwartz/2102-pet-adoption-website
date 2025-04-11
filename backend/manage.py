"""The module for managing pet-related operations."""
from flask import jsonify
from enums import PetStatus

# pylint: disable=R0913,R0917
def create_pet(name, species, breed, age, description, status=PetStatus.AVAILABLE):
    """
    Create a new pet with the given details.
    
    :param name: Name of the pet
    :param species: Species of the pet (e.g., Dog, Cat)
    :param breed: Breed of the pet
    :param age: Age of the pet in years
    :param description: Description including size and other details
    :param status: Adoption status of the pet (default: Available)
    :return: JSON response with the created pet details
    """
    # This is a mock function
    new_pet = {
        "name": name,
        "species": species,
        "breed": breed,
        "age": age,
        "description": description,
        "status": status
    }
    return jsonify(new_pet), 201

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
        "status": PetStatus.AVAILABLE
    }
    return jsonify(pet), 200

def get_all_pets():
    """
    Retrieve all pets.
    
    :return: JSON response with a list of pets
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
            "status": PetStatus.AVAILABLE
        },
        {
            "pet_id": 2,
            "name": "Whiskers",
            "species": "Cat",
            "breed": "Tabby",
            "age": 2,
            "description": "Calm and affectionate small-sized cat",
            "status": PetStatus.AVAILABLE
        }
    ]
    return jsonify(pets), 200

def get_pets_by_status(status):
    """
    Retrieve pets by their status.
    
    :param status: Status of the pets to retrieve
    :return: JSON response with a list of pets matching the status
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
            "status": status
        }
    ]
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
