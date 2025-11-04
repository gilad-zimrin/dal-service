from pydantic import BaseModel, model_serializer

class SecureBaseModel(BaseModel):
    @model_serializer(mode='wrap')
    def serialize(self, handler):
        data = handler(self)
        data.pop('password', None)
        data.pop('Password', None)  # If casing varies
        return data

    class Config:
        extra = "forbid"