from pydantic import field_validator, BaseModel, model_validator

class Signup(BaseModel):
    password:str
    confirm_pasword:str

    @field_validator('password')
    @classmethod
    def password_length(cls,v):
        if len(v)<8 or not any (c.isdigit() for c in v ):
            raise ValueError("min 8 characters at least one digit")
        return v

    @model_validator(mode='after')
    def password_match(self):
        if self.password!=self.confirm_password:
            raise ValueError("Passwords do not match")
        return self