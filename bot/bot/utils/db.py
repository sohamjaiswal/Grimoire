import os
from surrealdb import Surreal
from surrealdb.ws import ConnectionState

from dotenv import load_dotenv
load_dotenv()

class DB:
  def __init__(self, db: Surreal):
    self.db = db

  async def test_connect(self):
    if self.db.client_state != ConnectionState.CONNECTED:
      print("Disconnected, connecting...")
      await self.db.connect()
      await self.db.signin({"user": os.environ["DB_USER"], "pass": os.environ["DB_PASSWORD"]})
      await self.db.use("grimoire", "grimoire")
      print("Connected to database")
    else:
      print("Already connected to database")

db = DB(Surreal(os.environ["DB_HOST"]))