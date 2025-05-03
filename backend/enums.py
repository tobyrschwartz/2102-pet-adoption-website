"""The module containing all enums used in the application."""
from enum import Enum, IntEnum

class Role(IntEnum):
    """
    Enum for user roles in the system.
    Each role has a corresponding permission level.
    """
    GUEST = 0 # base permission level
    USER = 1 # anyone who is logged in
    STAFF = 2 # any staff who works at the shelter
    ADMIN = 3 # highest permission level (can add and remove staff)

class ApplicationStatus(str, Enum):
    """
    Enum for application statuses.
    Each status represents a stage in the application process.
    """
    PENDING = "Pending" # application is pending review
    APPROVED = "Approved" # application has been approved
    REJECTED = "Rejected" # application has been rejected

class QuestionType(str, Enum):
    """
    Enum for question types in the application form.
    Each type represents a different kind of question.
    """
    TEXT = "Text" # open-ended text response
    MULTIPLE_CHOICE = "Multiple Choice" # multiple choice question

class PetStatus(str, Enum):
    """
    Enum for pet statuses.
    Each status represents the current state of a pet in the system.
    """
    AVAILABLE = "Available" # pet is available for adoption
    ADOPTED = "Adopted" # pet has been adopted
