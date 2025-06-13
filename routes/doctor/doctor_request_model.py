from dataclasses import Field
from typing import List
from utility.custom_base_model import CustomBaseModel


class RegisterRequest(CustomBaseModel):
    name: str
    email: str
    mobile: str
    password: str


class ProfileAddressRequest(CustomBaseModel):
    gender: str
    dob: str
    marital_status: str
    image_path: int
    address: str
    country: int
    state: int
    city: int
    pincode: int


class ProfessionalDetailsRequest(CustomBaseModel):
    qualification_id: int
    graduation_id: int
    experience: int
    register_no: str


class SubCategoryRequest(CustomBaseModel):
    sub_category: int
    illness: List[int]


class LanguageRequest(CustomBaseModel):
    languages: List[int]


class HomeVisitRequest(CustomBaseModel):
    is_home: bool
    visit_type: List[int]
    travel_distance: str
    cost: str
    latitude: str
    longtitude: str


class VideoCallRequest(CustomBaseModel):
    is_video: bool
    time_solt: str
    cost: str

class DocumentData(CustomBaseModel):
    document_id: int
    image_id: int


class DocumentRequest(CustomBaseModel):
    document: List[DocumentData]


class InsuranceRequest(CustomBaseModel):
    is_insurance: bool
    insurance_no: str
    doc_imgs: int


class BankDetailsRequest(CustomBaseModel):
    account_name: str
    account_number: str
    ifsc_code: str
    bank_name: str
