from fastapi import APIRouter, Form, Query, File, UploadFile
from routes.common.common_request_model import RefreshTokenRequest, VerifyOtpRequest
from routes.common.common_service import *
from utility.custom_response import CustomResponse
import shutil
import os


common_router = APIRouter()


@common_router.get("/get_otp/{mobile}")
async def get_otp(mobile: str):
    try:
        result = await getOtp(mobileNo=int(mobile))
        return CustomResponse(
            status=True,
            data=result,
            message="Otp send to mobile number successfully..!",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)


@common_router.post("/verify_otp")
async def verify_otp(request: VerifyOtpRequest):
    try:
        result = await verifyOtp(data=request)
        return CustomResponse(
            status=True,
            data=result,
            message="Otp verified successfully..!",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)


@common_router.get("/general_list")
async def general_list():
    try:
        result = await GeneralList()
        return CustomResponse(status=True, message="Success", code=200, data=result)
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@common_router.get("/service-list")
async def service_list(
    page: int = Query(1, alias="page", ge=1), size: int = Query(15, alias="size", ge=1)
):
    try:
        print()
        result = await getServiceList(page, size)
        return CustomResponse(
            status=True, message="Success", code=200, data={"category_list": result}
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@common_router.get("/subcategory-list")
async def SubcatagoryList(
    service_id: int = Query(0, alias="service_id"),
    doctors_id: int = Query(1, alias="doctors_id"),
):
    try:
        result = await getSubcatagoryList(service_id, doctors_id)
        return CustomResponse(
            status=True,
            message="Successfully fetched main and sub category",
            code=200,
            data=result,
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@common_router.post("/refresh_token")
async def refresh_token(request: RefreshTokenRequest):
    try:
        res = await refreshToken(rToken=request.refresh_token)
        return res
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)

@common_router.post("/image_load")
async def upload_images(file:UploadFile = File(...),Tag: str = Form(...)):
    try:
        UPLOAD_DIR = "/app/images"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        if file:
            origin = os.path.basename(file.filename)
            _,ext = os.path.splitext(origin)
            filename = f"medisocy_{Tag}_{datetime.datetime.now():%M_%S}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            relative_path = os.path.join("images", filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_url = f"{relative_path}"
            result = await ImageUpload(file_url, Tag)
	
        return CustomResponse(
            status=True,
            message="Files uploaded successfully",
            code=200,
            data=result,
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)

@common_router.get("/state/{id}")
async def get_state(id: int):
    try:
        result = await getCommonData(id=id,tag="state")
        return CustomResponse(
            status=True,
            data=result,
            message="Data Arrived...",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)
    
@common_router.get("/district/{id}")
async def get_district( id: int,):
    try:
        result = await getCommonData(id=id,tag="districts")
        return CustomResponse(
            status=True,
            data=result,
            message="Data Arrived...",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)
    
@common_router.get("/country")
async def get_country():
    try:
        result = await getCommonData(id=None,tag="country")
        return CustomResponse(
            status=True,
            data=result,
            message="Data Arrived...",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)

@common_router.get("/degrees")
async def get_degrees():
    try:
        result = await getQualificationData(id=0,tag="degrees")
        return CustomResponse(
            status=True,
            data=result,
            message="Data Arrived...",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)

@common_router.get("/education/{id}")
async def get_education(id:int):
    try:
        result = await getQualificationData(id=id,tag="education")
        return CustomResponse(
            status=True,
            data=result,
            message="Data Arrived...",
            code=200,
        )
    except Exception as error:
        return CustomResponse(status=False, message=str(error), code=400)
