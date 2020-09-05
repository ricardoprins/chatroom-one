"""
If you've never worked with NoSQL before, it is structured in the following manner:

Databases contain Collections, which contain Documents - and these are the equivalent to the SQL records in a database.

In order to proceed with this tutorial, go to the MongoDB website, set up an account there(it's free!),
download MongoDB Compass(it's free forever even though it says it isn't), and you should be all set.

After you're done with that, create a free cluster in Atlas, connect to it using Compass and create a database.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from . import config

load_dotenv()


class MongoDB:
    client: AsyncIOMotorClient = None


db = MongoDB()


async def get_nosql_db() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        str(os.getenv('MONGODB_URL')), maxPoolSize=config.MAX_CONNECTIONS_COUNT, minPoolSize=config.MIN_CONNECTIONS_COUNT)


async def close_mongo_connection():
    db.client.close()
