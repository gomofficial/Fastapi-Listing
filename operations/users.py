from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from utils.secrets import password_manager
from exceptions import UserNotFoundError, UserAlreadyExists, UserAuthenticationError
import sqlalchemy as sa
from schema.output import RegisterOutput, UserOutput
from sqlalchemy.exc import IntegrityError
from utils.jwt import JWTHandler

class UsersOperation:
    def __init__(self, db_session:AsyncSession) -> None:
        self.db_session = db_session

    async def create(self,username:str,email:str,password:str):
        user_pwd = password_manager.hash(password)
        user = User()
        user.username = username
        user.email    = email
        user.password = user_pwd
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExists

        return RegisterOutput(username=user.username,id=user.id)
    
    async def get_user_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFoundError

            return UserOutput(username = user_data.username, email = user_data.email,
                              is_staff = user_data.is_staff, is_active = user_data.is_active,
                              id = user_data.id)
        
    async def update_username(self, old_username: str, new_username: str) -> User:
        query = sa.select(User).where(User.username == old_username)
        update_query = (
            sa.update(User)
            .where(User.username == old_username)
            .values(username=new_username)
        )
        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFoundError

            await session.execute(update_query)
            await session.commit()

            user_data.username = new_username
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

            if not password_manager.verify(password,user.password):
                raise UserAuthenticationError
            
            return JWTHandler.generate(username)
 