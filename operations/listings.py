from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Listing, User
from uuid import UUID
from utils.secrets import password_manager
from exceptions import ListingNotFoundError, UserNotFoundError, InvalidPermission
import sqlalchemy as sa
from sqlalchemy.orm import selectinload
from schema.output import ListingOutput
from sqlalchemy.exc import IntegrityError
from utils.auth import JWTHandler


class ListingOperation:
    def __init__(self, db_session:AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username, data):
        listing                 = Listing()
        listing.type            = data["type"]
        listing.availableNow    = data["availableNow"]
        listing.address         = data["address"]
        
        user_query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise UserNotFoundError
            listing.owner   = user_data
            listing.ownerId = user_data.id
            user_data.listings.append(listing)

            session.add(listing)
            await session.commit()
        
        return ListingOutput(id=listing.id,
                             type=listing.type, availableNow=listing.availableNow,
                             owner=listing.owner.username, address=listing.address,
                             createdAt=listing.createdAt, updatedAt=listing.updatedAt)
    
    async def get_list(self):

        listing_query = sa.select(Listing)

        async with self.db_session as session:
            listings = await session.scalars(listing_query)

        return [ListingOutput(id=listing.id,
                             type=listing.type, availableNow=listing.availableNow,
                             owner=listing.owner.username, address=listing.address,
                             createdAt=listing.createdAt, updatedAt=listing.updatedAt) for listing in listings ]
    
    async def get(self, id):
        listing_query = sa.select(Listing).where(Listing.id == id)

        async with self.db_session as session:
            listings = await session.scalars(listing_query)

        return [ListingOutput(id=listing.id,
                             type=listing.type, availableNow=listing.availableNow,
                             owner=listing.owner.username, address=listing.address,
                             createdAt=listing.createdAt, updatedAt=listing.updatedAt) for listing in listings ]
    

    async def update(self, id, username ,data):
        query = sa.select(Listing).where(Listing.id == id)
        update_query = sa.update(Listing).where(Listing.id == id).values(**data)
        
        async with self.db_session as session:
            listing = await session.scalar(query)

            if listing is None:
                raise ListingNotFoundError
            
            if listing.owner.username != username:
                raise InvalidPermission

            await session.execute(update_query)
            await session.commit()

            return ListingOutput(id=listing.id,
                             type=listing.type, availableNow=listing.availableNow,
                             owner=listing.owner.username, address=listing.address,
                             createdAt=listing.createdAt, updatedAt=listing.updatedAt)
        

    async def delete(self, id:UUID)-> None:

        delete_query = sa.delete(Listing).where(Listing.id == id)

        async with self.db_session as session:
            await session.execute(delete_query)
            await session.commit()
    