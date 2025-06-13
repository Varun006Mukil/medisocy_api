from pydantic import BaseModel
from typing import List


class OtpResponseModel:
    otp: int
    transaction_id : str
    
    def __init__(self,otp:int,transaction_id:str)-> None:
        self.otp = otp
        self.transaction_id = transaction_id
    
    def to_json(self)->dict:
        return{
        "otp" : self.otp,
        "transaction_id" : self.transaction_id
        }          
        


class UserDetails:
    user_id : int
    name : str
    role : str
    status: bool
    category_id : int
    
    def __init__(self, user_id: int, name: str, role: str,status:bool,category_id:int) -> None:
        self.user_id = user_id
        self.name = name
        self.role = role
        self.status = status
        self.category_id = category_id

    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "status" : self.status,
            "category_id": self.category_id
        }   
        
class LoginResponse:
    access_token: str
    refresh_token: str
    user_id: str
    name: str
    status: bool
    category_id : int

    def __init__(
        self, access_token: str, refresh_token: str, user_id: str, name: str,status:bool,category_id:int
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.name = name
        self.status = status
        self.category_id = category_id

    def to_json(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "user_id": self.user_id,
            "name": self.name,
            "status" : self.status,
            "category_id": self.category_id
        }
    

class SubServiceList(): 
    id: int
    name: str
    status: bool

    class Config:
        extra = "ignore"  

    def __init__(self, id: int, name: str, status: bool) -> None:
        self.id = id
        self.name = name
        self.status = status

    def  from_json(data,value):
        return data(
            id= value['id'],
            name = value['name'],
            status = value['status']
        )    

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }


class SubCategoryListResponse():
    main_List: List
    sub_list: List

    def __init__(self, main_List: list, sub_list: list) -> None:
        self.main_List = main_List  
        self.sub_list = sub_list    

    def to_json(self) -> dict:
        return {
            "main_List": self.main_List,
            "sub_list": self.sub_list
        }
    
class CommonList:
    gender: List[str]
    marital_status: List[str]
    country: List
    languages: List
    qualification: List
    home_visit : dict
    video_call : dict


    def __init__(
        self,
        gender: List[str],
        marital_status: List[str],
        country: List,
        languages: List,
        qualification: List,
        home_visit :dict,
        video_call :dict
    ) -> None:
        self.gender = gender
        self.marital_status = marital_status
        self.country = country
        self.languages = languages
        self.qualification = qualification
        self.home_visit = home_visit
        self.video_call =video_call

    def to_json(self) -> dict:
        return {
            "gender": self.gender,
            "marital_status": self.marital_status,
            "country": self.country,
            "languages": self.languages,
            "qualification": self.qualification,
            "home_visit" : self.home_visit,
            "video_call" : self.video_call
        }

        
    



