"""Module containing mock data for testing purposes."""
from enums import PetStatus, ApplicationStatus

# Common pet data
BUDDY_PET = {
    "name": "Buddy",
    "species": "Dog",
    "breed": "Golden Retriever",
    "age": 3,
    "description": "Friendly and energetic medium-sized dog",
    "status": PetStatus.AVAILABLE,
    "image_url": "https://example.com/pet1.jpg"
}

WHISKERS_PET = {
    "name": "Whiskers",
    "species": "Cat",
    "breed": "Tabby",
    "age": 2,
    "description": "Calm and affectionate small-sized cat",
    "status": PetStatus.AVAILABLE,
    "image_url": "https://example.com/pet2.jpg"
}

def get_mock_pet(pet_id, status=PetStatus.AVAILABLE):
    """
    Get a mock pet with the specified ID.
    
    :param pet_id: ID to assign to the pet
    :param status: Status to assign to the pet
    :return: A pet dictionary with the specified ID and status
    """
    pet = BUDDY_PET.copy()
    pet["pet_id"] = pet_id
    pet["status"] = status
    return pet

def get_mock_pet_list(status=PetStatus.AVAILABLE):
    """
    Get a list of mock pets.
    
    :param status: Status to assign to the pets
    :return: A list of pet dictionaries
    """
    pet1 = get_mock_pet(1, status)
    pet2 = WHISKERS_PET.copy()
    pet2["pet_id"] = 2
    pet2["status"] = status
    return [pet1, pet2]

def get_mock_application(application_id, status=ApplicationStatus.PENDING):
    """
    Get a mock application with the specified ID and status.
    
    :param application_id: ID to assign to the application
    :param status: Status to assign to the application
    :return: An application dictionary
    """
    return {
        "application_id": application_id,
        "user_id": 1,
        "pet_id": 1,
        "submit_date": "2025-04-01",
        "status": status,
        "reviewer_id": None if status == ApplicationStatus.PENDING else 3,
        "review_date": None if status == ApplicationStatus.PENDING else "2025-04-07"
    }

def get_mock_application_list(user_id=1, status=None):
    """
    Get a list of mock applications.
    
    :param user_id: User ID for the applications
    :param status: Status to filter by (if None, returns mixed statuses)
    :return: A list of application dictionaries
    """
    if status:
        return [get_mock_application(1, status)]
    return [
        {
            "application_id": 1,
            "user_id": user_id,
            "pet_id": 1,
            "submit_date": "2025-04-07",
            "status": ApplicationStatus.PENDING,
            "reviewer_id": None,
            "review_date": None
        },
        {
            "application_id": 2,
            "user_id": user_id,
            "pet_id": 2,
            "submit_date": "2025-04-01",
            "status": ApplicationStatus.APPROVED,
            "reviewer_id": 3,
            "review_date": "2025-04-07"
        }
    ]
