from  fastapi import APIRouter, Body, Depends
from utils.celery_worker import weather_forcast

bots_router = APIRouter()


@bots_router.post('/')
async def get_weather(days:int, city:str):
    '''
        description : weather api using celery \n
        id : \n
            city "city name query param" \n
            days "days number query param" \n
        body : \n
            None
        output :\n 
            csv file
    '''
    task = weather_forcast.delay(days=days, city=city)

    return {"taskId":task.task_id, "message": "your task is in task queue and will be saved in Forcast.csv"}