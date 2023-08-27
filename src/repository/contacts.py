from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate, ContactResponse, ContactCreate
# new 
from sqlalchemy import and_




async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts from the database.
    
    
    :param skip: int: Determine how many contacts to skip
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to be returned.
            db (Session): A connection to the database.
        Returns:
            Contact: The requested Contact object.
    
    :param contact_id: int: Tell the function what contact to get
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactBase: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone_number=body.phone_number, birth_date=body.birth_date, additional_data=body.additional_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.
        Returns:
            Contact | None: The deleted Contact object or None if no such object exists in the database.
    
    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :return: A contact object, but the return type is specified as contact | none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactUpdate: Pass the data from the request body to the function
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def update_status_contact(contact_id: int, body: ContactResponse, db: Session) -> Contact | None:
    """
    The update_status_contact function updates the status of a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactResponse): The new status for this Contact.
            db (Session): A database session object that is used to query and commit changes to the database. 
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactResponse: Pass the data from the request body to the function
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.done = body.done
        db.commit()
    return contact

async def update_status_contact(contact_id: int, body: ContactCreate, db: Session) -> Contact | None:
    """
    The update_status_contact function updates the status of a contact in the database.
        
    
    :param contact_id: int: Identify the contact to update
    :param body: ContactCreate: Update the contact with the new data
    :param db: Session: Pass the database session to the function
    :return: The updated contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.done = body.done
        db.commit()
    return contact

# new

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function retrieves a list of contacts for a specific user with specified pagination parameters.
    
    :param skip: int: Specify the number of notes to skip
    :param limit: int: Specify the maximum number of notes to return
    :param user: User: Specify the user to retrieve contacts for
    :param db: Session: Pass the database session into the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_note(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to retrieve.
    :type note_id: int
    :param user: The user to retrieve the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The note with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new note for a specific user.

    :param body: The data for the note to create.
    :type body: NoteModel
    :param user: The user to create the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created note.
    :rtype: Note
    """
    tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
    note = Contact(title=body.title, description=body.description, tags=tags, user=user)
    db.add(Contact)
    db.commit()
    db.refresh(Contact)
    return Contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to remove.
    :type note_id: int
    :param user: The user to remove the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed note, or None if it does not exist.
    :rtype: Note | None
    """
    note = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to update.
    :type note_id: int
    :param body: The updated data for the note.
    :type body: NoteUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated note, or None if it does not exist.
    :rtype: Note | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Contact.user_id == user.id)).all()
        contact.title = body.title
        contact.description = body.description
        contact.done = body.done
        contact.tags = tags
        db.commit()
    return contact


async def update_status_contact(contact_id: int, body: ContactStatusUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates the status (i.e. "done" or "not done") of a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to update.
    :type note_id: int
    :param body: The updated status for the note.
    :type body: NoteStatusUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated note, or None if it does not exist.
    :rtype: Note | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.done = body.done
        db.commit()
    return contact