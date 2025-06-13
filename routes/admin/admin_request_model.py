from utility.custom_base_model import CustomBaseModel


class AdminLoginRequest(CustomBaseModel):
    name: str
    password: str

class langugagesCreateRequest(CustomBaseModel):
    title:str

class langugagesUpdateRequest(CustomBaseModel):
    id:int
    title:str