from fastapi import APIRouter, Depends
from routes.admin.admin_request_model import AdminLoginRequest
from routes.admin.admin_services import adminLogin, getDoctors
from utility.custom_response import CustomResponse
from utility.utility import execute_query, token_validator

admin_router = APIRouter()


@admin_router.post("/admin_login")
async def admin_login(data: AdminLoginRequest):
    try:
        isValid = await execute_query(
            query="select admin_check(%s, %s)", params=[data.name, data.password]
        )
        if isValid == 1:
            result = await adminLogin(name=data.name)
            return CustomResponse(
                status=True,
                data=result,
                message="user logined successfully...!",
                code=200,
            )
        else:
            return CustomResponse(
                status=False, message="Invalid username or password", code=400
            )
    except Exception as error:
        return CustomResponse(status=False, message=str(error.args[0]), code=400)


@admin_router.get("/pending_doctor")
async def pending_doctor(user=Depends(token_validator)):
    try:
        result = await getDoctors(id=0, tag="pending_doctors")
        return CustomResponse(
            status=True, message="Data Arrived Successfully...!", code=200, data=result
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@admin_router.get("/approved_doctor")
async def approved_doctor(user=Depends(token_validator)):
    try:
        result = await getDoctors(id=0, tag="approved_doctors")
        return CustomResponse(
            status=True, message="Data Arrived Successfully...!", code=200, data=result
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)


@admin_router.get("doctor_details/{id}")
async def doctor_details(id=int):
    try:
        result = await getDoctors(id=id, tag="doctor_details")
        return CustomResponse(
            status=True, message="Data Arrived Successfully...!", code=200, data=result
        )
    except Exception as e:
        return CustomResponse(status=False, message=str(e), code=400)
