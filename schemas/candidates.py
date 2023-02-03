from pydantic import BaseModel,EmailStr,validator,Field
from typing import Optional
from bson import ObjectId
from schemas.user import User


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class CandidateObject(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: str
    nationality: str
    city: str
    salary: int
    gender: str
    
    @validator('skills')
    def skills_match(cls,v):
        if not v in ['java','c#','python','mongodb']:
            raise ValueError("skills must be in ['java','c#','python','mongodb']")
        return v

    @validator('gender')
    def gender_match(cls,v):
        if not v in ['Male', 'Female', 'Not Specific']:
            raise ValueError("skills must be in ['Male', 'Female', 'Not Specific']")
        return v


class Candidates(CandidateObject):
    id: Optional[PyObjectId] = Field(alias='_id') 
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class VerifyUser(User):
    id: Optional[PyObjectId] = Field(alias='_id') 
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        