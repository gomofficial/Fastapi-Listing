from  fastapi import APIRouter, Body, Depends
from  schema._input import *
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.listings import ListingOperation
from schema import jwt
from utils.auth import JWTHandler
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

listing_router = APIRouter()

@listing_router.post("/")
async def create( db_session: Annotated[AsyncSession, Depends(get_db)],
                    data: ListingInput = Body(),
                    token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):

    '''
        description : list of all listings \n
        id : UUID "id of the listing" \n
        body : \n
            type : APARTMENT or HOUSE \n
            available : true or false \n
            address   : string \n
        output :
            listing
    '''
    listing = await ListingOperation(db_session).create(token_data.username, data.model_dump())
    
    return listing

@listing_router.get("/all")
async def list(db_session: Annotated[AsyncSession, Depends(get_db)]):
    '''
        description : \n
            list of all listings \n
        inputs:\n
            no inputs needed
    '''
    
    listings = await ListingOperation(db_session).get_list()

    return listings

@listing_router.get("/")
async def detail(db_session: Annotated[AsyncSession, Depends(get_db)], id:UUID):
    '''
        description : \n
            returns a listings
        id : \n
            UUID "id of the listing"
        output : \n
            listing 
    '''
    listings = await ListingOperation(db_session).get(id)

    return listings

@listing_router.put("/")
async def update(db_session: Annotated[AsyncSession, Depends(get_db)], id:UUID,
                               data: ListingInput = Body(),
                               token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    '''
        description : \n
            list of all listings \n
        id :\n
            UUID "id of the listing" \n
        body : \n
            type : APARTMENT or HOUSE \n
            available : true or false \n
            address   : string \n
            output : listing
    '''
    listings = await ListingOperation(db_session).update(id, token_data.username, data.model_dump())

    return listings

@listing_router.delete("/")

async def delete(db_session: Annotated[AsyncSession, Depends(get_db)], id:UUID,
                               token_data:jwt.JWTPayload = Depends(JWTHandler.verify_token)):
    '''
        description : list of all listings \n
        id : \n
            UUID "id of the listing" \n
        body : \n
            None
        output :\n 
            listing
    '''
    listings = await ListingOperation(db_session).delete(id)

    return listings

