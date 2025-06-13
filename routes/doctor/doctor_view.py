from fastapi import APIRouter, Request, Depends
from routes.doctor.doctor_request_model import (
    BankDetailsRequest,
    DocumentRequest,
    HomeVisitRequest,
    InsuranceRequest,
    LanguageRequest,
    ProfessionalDetailsRequest,
    ProfileAddressRequest,
    RegisterRequest,
    SubCategoryRequest,
    VideoCallRequest,
)
from routes.doctor.doctor_services import *
from utility.custom_response import CustomResponse
from utility.custom_validator import custom_validator
from utility.utility import token_validator

doctor_routers = APIRouter()


@doctor_routers.post("/register")
async def doctor_register(request: RegisterRequest):
    try:
        result = await doctorRegister(data=request)
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)


@doctor_routers.get("/check_account")
async def check_account(request: Request, user=Depends(token_validator)):
    try:
        userId = user.get("user_id")
        result = await checkAccount(id=userId)
        return CustomResponse(
            status=True, message="Data Arrived Successfully...!", code=200, data=result
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)


# doctor category update
@doctor_routers.get("/category/update/{category_id}")
async def doctor_category_update(category_id: int, user=Depends(token_validator)):
    try:
        result = await doctorCategoryUpdate(
            catgoryId=category_id, doctorId=user.get("user_id")
        )
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


# add doctor address and profile
@doctor_routers.post("/update/profile_address")
async def add_profile_address(
    request: ProfileAddressRequest, user=Depends(token_validator)
):
    try:
        result = await addDoctorProfileAndAddress(
            data=request, doctor_id=user.get("user_id")
        )
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)


# doctor professional
@doctor_routers.post("/update/professional_details")
async def professional_details(
    request: ProfessionalDetailsRequest, user=Depends(token_validator)
):
    try:
        result = await professionalDetails(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/sub_category")
async def sub_category_update(
    request: SubCategoryRequest, user=Depends(token_validator)
):
    try:
        result = await subCategoryUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/language")
async def language_update(request: LanguageRequest, user=Depends(token_validator)):
    try:
        result = await languageUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/home_visit")
async def home_visit(request: HomeVisitRequest, user=Depends(token_validator)):
    try:
        result = await homeVisitUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/video_call")
async def video_call(request: VideoCallRequest, user=Depends(token_validator)):
    try:
        result = await videoVisitUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/document")
async def document_update(request: DocumentRequest, user=Depends(token_validator)):
    try:
        result = await documentUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/insurance")
async def insurance_update(request: InsuranceRequest, user=Depends(token_validator)):
    try:
        result = await insuranceUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@doctor_routers.post("/update/bank_details")
async def bank_update(request: BankDetailsRequest, user=Depends(token_validator)):
    try:
        result = await bankUpdate(data=request, doctor_id=user.get("user_id"))
        return CustomResponse(status=True, message=result, code=200, data={})
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)
