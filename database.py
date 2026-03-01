from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Name your database file
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

# 2. Setup the session factory
SessionLocal = sessionmaker(bind=engine)
# 3. Create the Base class
Base = declarative_base()