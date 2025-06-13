from itertools import groupby
from operator import itemgetter
import jwt
import json
from routes.common.common_model import (
    CommonList,
    LoginResponse,
    OtpResponseModel,
    SubCategoryListResponse,
    SubServiceList,
    UserDetails,
)
from routes.common.common_request_model import VerifyOtpRequest
from settings import Settings
from utility.utility import *


settings = Settings()


async def userValidate(phone=None, fcm=None, role=None):
    try:
        users = await execute_stored_procedure(
            proc_name="user_validate", params=[phone, role, fcm], is_one=True
        )
        if users:
            user_details = UserDetails(
                user_id=users.get("id"),
                name=users.get("name"),
                role=role,
                status=users.get("status"),
                category_id=users.get("category_id", 0),
            )
            result = await createTokens(user=user_details)
            return result
        else:
            return Exception("something went wrong...!")
    except Exception as e:
        raise Exception(str(e.args))


async def getOtp(mobileNo=None):
    try:
        result = await execute_stored_procedure(
            proc_name="otp_creation", params=[mobileNo], is_one=True
        )
        outRes = OtpResponseModel(
            otp=result.get("otp"), transaction_id=result.get("transaction_id")
        )
        return outRes.to_json()
    except Exception as error:
        raise Exception(str(error.args))


async def verifyOtp(data: VerifyOtpRequest = None):
    try:
        result = await execute_stored_procedure(
            proc_name="verify_otp",
            params=[
                data.otp,
                data.trx_id,
                data.mobile,
                data.role,
                data.fcm_token,
            ],
            is_one=True,
        )
        if result:
            user_details = UserDetails(
                user_id=result.get("id"),
                name=result.get("name"),
                role=result,
                status=result.get("status"),
                category_id=result.get("category_id", 0),
            )
            outRes = await createTokens(user=user_details)
            return outRes
    except Exception as error:
        raise Exception(str(error.args))


async def createTokens(user: UserDetails):
    try:
        ac_token = create_access_token(user=user)
        rf_token = create_refresh_token(user=user)
        result = LoginResponse(
            access_token=ac_token,
            refresh_token=rf_token,
            user_id=user.user_id,
            name=user.name,
            status=user.status,
            category_id=user.category_id,
        ).to_json()
        return result
    except Exception as e:
        raise Exception(str(e.args))


async def refreshToken(rToken=None):
    try:
        if rToken is not None:
            decoded = jwt.decode(
                rToken,
                settings.SECRET_KEY,
                algorithms="HS256",
                audience="mmp",
                options={
                    "require_iat": True,
                    "require_exp": True,
                },
                leeway=30,
            )
            if decoded["type"] == "refresh" and decoded["role"] == "doctor":
                users = await execute_stored_procedure(
                    "get_user", [decoded["user_id"]], is_one=True
                )
                user_details = UserDetails(
                    user_id=users.get("id"),
                    name=users.get("name"),
                    role="doctor",
                    status=users.get("status"),
                    category_id=users.get("category_id", 0),
                )
                outresult = await createTokens(user=user_details)
                return outresult
            else:
                raise Exception("InvalidTokenError")

    except Exception as error:
        raise Exception(str(error)) from error


async def GeneralList():
    try:
        result = await execute_stored_procedure(
            proc_name="get_general",
        )
        outRes = CommonList(
            gender=["Male", "Female", "Transgeder"],
            marital_status=[
                "Single",
                "Married",
                "Divorced",
                "Widowed",
                "Separated",
                "Cohabiting",
                "Engaged",
            ],
            country=result[0] if result[0] else [],
            languages=result[1] if result[1] else [],
            qualification=result[2] if result[2] else [],
            home_visit={
                "visiting_type": [],
                "distance": ["10KM", "20KM", "50KM", "100KM"],
            },
            video_call={"time_slot": ["15 Mins", "30 Mins"]},
        )
        return outRes.to_json()
    except Exception as e:
        raise Exception(f"Service Fetch Failed: {str(e)}")


# service list pagination
async def getServiceList(page: int, size: int):
    try:
        services = await execute_stored_procedure(
            proc_name="get_services_list", params=[page, size]
        )
        return services

    except Exception as e:
        raise Exception(str(e)) from e


async def getSubcatagoryList(service_id: int, doctors_id: int):
    try:
        result = await execute_stored_procedure(
            proc_name="get_subcategory", params=[service_id, doctors_id]
        )
        outRes = {
            "sub_category": (
                [
                    {
                        "id": item["id"],
                        "name": item["name"],
                        "status": item["status"],
                        "illness": json.loads(item["sub_categories"]),
                    }
                    for item in result[0]
                ]
                if result
                else []
            )
        }
        return outRes
    except Exception as e:
        raise Exception(str(e)) from e

async def ImageUpload(image: int, tag: str):
    try:
        result = await execute_stored_procedure(
            proc_name="image_upload", params=[image, tag],is_one=True
        )
        outResult = {"image_id": result.get("image_id"),"image_path":image}
        return outResult
    except Exception as e:
        raise Exception(str(e)) from e

async def getCommonData(id=None,tag=None):
    try:
        result = await execute_stored_procedure(
            proc_name="get_common_data", params=[id, tag]
        )
        outResult = {
            f"{tag}_list": result[0]     
        }
        return outResult
    except Exception as e:
        raise Exception(str(e)) from e

async def getQualificationData(id=None,tag=None):
    try:
        result = await execute_stored_procedure(
            proc_name="get_qualification_data", params=[id, tag]
        )
        outResult = {
            f"{tag}_list": result[0]
        }
        return outResult
    except Exception as e:
        raise Exception(str(e)) from e
