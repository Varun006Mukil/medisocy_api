from typing import List


class MyAccountModel:
    is_verify : bool
    is_upload : bool
    profile_list : List
    
    def __init__(self,is_verify:bool,is_upload:bool,profile_list:List)->None:
        self.is_verify = is_verify
        self.is_upload = is_upload
        self.profile_list = profile_list
    
    def to_json(self)->dict:
        return {
            "is_verify":self.is_verify,
            "is_upload":self.is_upload,
            "profile_list": self.profile_list
        }  