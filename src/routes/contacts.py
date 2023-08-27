from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts

from fastapi_limiter.depends import RateLimiter
from ..services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/contacts')

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    The read_contacts function returns a list of contacts.
        ---
        get:
          summary: Get all contacts.
          description: Returns a list of all the contacts in the database.
          responses:
            200:
              description: A JSON array containing contact objects, each with an id, name and email address field.  If no records are found, an empty array is returned instead.
    
    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    The read_contact function returns a contact by its ID.
        If the contact does not exist, it raises an HTTP 404 error.
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactCreate, db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactCreate object as input and returns the newly created contact.
    
    :param body: ContactCreate: Pass the data from the request body to the function
    :param db: Session: Pass the database session to the repository layer
    :return: A contactcreate object, which is a pydantic model
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes a ContactUpdate object as input, which is validated by Pydantic.
        If the contact does not exist, an HTTP 404 error is raised.
    
    :param body: ContactUpdate: Pass the contact information to be updated
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Get the database connection from the dependency injection
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
        Returns:
            Contact: The deleted Contact object.
    
    :param contact_id: int: Get the contact_id from the request
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_notes function returns a list of notes.
        The function takes in three parameters: skip, limit, and db.
        Skip is the number of records to skip before returning results. Limit is the maximum number of records to return.
    
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A list of notes
    :doc-author: Trelent
    """
    notes = await repository_contacts.get_contact(skip, limit, current_user, db)
    return contacts