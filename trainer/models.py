import enum
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class StatusEnum(enum.Enum):
    TRAINING = "Training"
    TRAINED = "Trained"
    FAILED = "Failed"
    DEPLOYED = "Deployed"


class SelectedModel(Base):
    __tablename__ = "SelectedModel"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    prediction_field = Column(String, nullable=False)
    config = Column(String, nullable=False)
    status = Column(ENUM(StatusEnum))
    evaluation = Column(String)
