from peewee import (Model, CharField, AutoField, BooleanField, DateTimeField,
                    PostgresqlDatabase)
from os import getenv
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host="localhost",
    port=5432
)

class BaseModel(Model):
    class Meta:
        database = db

class LetterTable(BaseModel):
    LetterId = AutoField(primary_key=True)
    LetterContent = CharField(null=True)
    Uuid = CharField(unique=True, null=False)
    IsWatched = BooleanField(default=False)
    TimeDelete = DateTimeField(default=None, null=True)

def init_db():
    db.connect()
    db.create_tables([LetterTable])
    db.close()

init_db()