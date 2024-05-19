from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from utils.secrets import password_manager
from exceptions import UserNotFoundError, UserAlreadyExists, UserAuthenticationError
import sqlalchemy as sa
from schema.output import UserOutput
from sqlalchemy.exc import IntegrityError
from utils.auth import JWTHandler

class UsersOperation:
    def __init__(self, db_session:AsyncSession) -> None:
        self.db_session = db_session


    async def create(self, data):
        user_pwd             = password_manager.hash_password(data["password"])
        user                 = User()
        user.fullname        = data["fullname"]
        user.username        = data["username"]
        user.email           = data["email"]
        user.hashed_password = user_pwd
        user.DoB             = data["DoB"]
        user.gender          = data["gender"]
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExists

        return UserOutput.model_validate(user.__dict__)
    


    async def get_user_profile(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFoundError

            return UserOutput.model_validate(user_data.__dict__)
        


    async def update(self, username, data) -> User:
        query = sa.select(User).where(User.username == username)
        update_query = sa.update(User).where(User.username == username).values(**data)
        
        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFoundError

            await session.execute(update_query)
            await session.commit()

            return UserOutput.model_validate(user_data.__dict__)


    async def update_password(self, username, data) -> User:
        query = sa.select(User).where(User.username == username)
        update_query = sa.update(User).where(User.username == username).values(hashed_password = password_manager.hash_password(data['password_1']))
        
        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFoundError
            if not password_manager.verify(data['old_password'],user_data.hashed_password):
                raise UserAuthenticationError
            
            await session.execute(update_query)
            await session.commit()
            
            return user_data
        

    async def user_delete_account(self, username:str)-> None:

        delete_query = sa.delete(User).where(User.username==username)

        async with self.db_session as session:
            await session.execute(delete_query)
            await session.commit()
    


    async def login(self, username:str, password:str)-> str:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise UserAuthenticationError

            if not password_manager.verify(password,user.hashed_password):
                raise UserAuthenticationError
            
            return JWTHandler.generate(username)


