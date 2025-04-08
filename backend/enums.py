from enum import Enum


class Role(Enum):
    """
    Enum for user roles in the system.
    Each role has a corresponding permission level.
    """
    GUEST = 0 # base permission level
    USER = 1 # anyone who is logged in
    STAFF = 2 # any staff who works at the shelter
    ADMIN = 3 # highest permission level (can add and remove staff)

class ApplicationStatus(Enum):
    """
    Enum for application statuses.
    Each status represents a stage in the application process.
    """
    PENDING = "Pending" # application is pending review
    APPROVED = "Approved" # application has been approved
    REJECTED = "Rejected" # application has been rejected

class PetStatus(Enum):
    """
    Enum for pet statuses.
    Each status represents the current state of a pet in the system.
    """
    AVAILABLE = "Available" # pet is available for adoption
    ADOPTED = "Adopted" # pet has been adopted
