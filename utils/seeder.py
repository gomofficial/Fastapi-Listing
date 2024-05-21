import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from db import models,local_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from utils.secrets import password_manager
from utils.enums import GenderEnum
from faker import Faker
import random
from settings import *

import argparse

parser = argparse.ArgumentParser(description='My Python Script')


parser.add_argument('--count', type=int, default=0, help='An integer argument')


args = parser.parse_args()

count_value = args.count


class Seeder:
    def __init__(self, db_session:Session) -> None:
        self.db_session = db_session
        self.faker      = Faker()

    def create_user(self, count_value):
        for i in range(count_value):
            pwd                  = self.faker.password()
            user_pwd             = password_manager.hash_password(pwd)
            user                 = models.User()
            user.fullname        = self.faker.file_name()
            username             = self.faker.user_name()
            user.username        = username
            user.email           = self.faker.email()
            user.hashed_password = user_pwd
            user.DoB             = self.faker.date_of_birth()
            user.gender          = random.choice(list(GenderEnum))
            with self.db_session as session:
                try:
                    session.add(user)
                    session.commit()
                    print(f"User username: {username}, password: {pwd} ")
                except Exception as e:
                    print(e)


seeder = Seeder(local_engine.SessionLocal())

seeder.create_user(count_value)