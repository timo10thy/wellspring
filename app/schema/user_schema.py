from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# id =Column(Integer, primary_key=True, nullable=False, index=True)
#     name = Column(String(100),nullable=False)
#     email=Column(String(100), nullable=False)
#     password=Column(String(200),nullable=False)
#     role= Column(Enum('ADMIN','USER'),nullable=False)
#     image= Column(String(500), nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     update_at = Column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now(),  
#     nullable=False
# )

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    user_name:str

class UserResponse(BaseModel):
    name:str
    email:str
    user_name:str
    role:str
    image:Optional[str]
    created_at:datetime
    updated_at:datetime
