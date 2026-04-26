from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str

    
class LoginRequest(BaseModel):
    username: str
    password: str
    
