from routes.doctor.doctor_model import MyAccountModel
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
from utility.utility import execute_stored_procedure
import json


async def doctorRegister(data: RegisterRequest):
    try:
        await execute_stored_procedure(
            proc_name="doctor_register",
            params=[
                data.name,
                data.email,
                data.mobile,
                data.password,
            ],
            is_one=True,
        )
        return "Doctor registerd successfully...!"
    except Exception as e:
        raise Exception(str(e.args))


async def doctorCategoryUpdate(doctorId=None, catgoryId=None):
    try:
        await execute_stored_procedure(
            proc_name="doctor_category_update",
            params=[catgoryId, doctorId],
            is_one=True,
        )
        return "Doctor category updated successfully."
    except Exception as e:
        raise Exception(str(e.args))


async def checkAccount(id=None):
    try:
        result = await execute_stored_procedure(
            proc_name="my_account_check", params=[id],
            is_one=False
        )
        out = MyAccountModel(
            is_verify=result[0][0].get("status"),
            is_upload=result[0][0].get("is_upload"),
            profile_list=result[1])
        return out.to_json()
    except Exception as e:
        raise Exception(str(e.args)) from e


# add doctor address and profile details
async def addDoctorProfileAndAddress(
    data: ProfileAddressRequest = None, doctor_id=None
):
    try:
        await execute_stored_procedure(
            proc_name="AddDoctorProfileAndAddress",
            params=[
                doctor_id,
                data.gender,
                data.dob,
                data.marital_status,
                data.image_path,
                data.address,
                data.country,
                data.state,
                data.city,
                data.pincode,
            ],
        )
        return "Doctor profile and address added successfully...!"
    except Exception as e:
        raise Exception(str(e.args))


# doctor_professional
async def professionalDetails(data: ProfessionalDetailsRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="doctors_professional",
            params=[
                doctor_id,
                data.qualification_id,
                data.graduation_id,
                data.experience,
                data.register_no,
            ],
        )
        return "Doctor professional details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def subCategoryUpdate(data: SubCategoryRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="doctor_subcategory_update",
            params=[
                doctor_id,
                data.sub_category,  # ✅ Convert list to JSON
                json.dumps(data.illness),  # ✅ Handle missing illness key
            ],
        )
        return "Doctor sub category details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def languageUpdate(data: LanguageRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="language_updation",
            params=[
                doctor_id,
                json.dumps(data.languages),  # ✅ Convert list to JSON
            ],
        )
        return "Language updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def homeVisitUpdate(data: HomeVisitRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="update_home_visit",
            params=[
                doctor_id,
                data.is_home,  # ✅ Convert list to JSON
                json.dumps(data.visit_type),  # ✅ Convert list to JSON
                data.travel_distance,
                data.cost,
                data.latitude,
                data.longtitude,
            ],
        )
        return "Home visit details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def videoVisitUpdate(data: VideoCallRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="update_video_call",
            params=[
                doctor_id,
                data.is_video,  # ✅ Convert list to JSON
                data.time_solt,  # ✅ Convert list to JSON
                data.cost,
            ],
        )
        return "Video call details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def documentUpdate(data: DocumentRequest = None, doctor_id=None):
    try:
        document_json = json.dumps([doc.model_dump() for doc in data.document])
        await execute_stored_procedure(
            proc_name="doctor_document_update",
            params=[doctor_id, document_json],
        )
        return "Document details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def insuranceUpdate(data: InsuranceRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="doctor_insurance_update",
            params=[
                doctor_id,
                data.is_insurance,
                data.insurance_no,  # ✅ Convert list to JSON
                data.doc_imgs,  # ✅ Convert list to JSON
            ],
        )
        return "Insurance details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))


async def bankUpdate(data: BankDetailsRequest = None, doctor_id=None):
    try:
        await execute_stored_procedure(
            proc_name="doctor_bank_update",
            params=[
                doctor_id,
                data.account_name,
                data.account_number,  # ✅ Convert list to JSON
                data.ifsc_code,  # ✅ Convert list to JSON
                data.bank_name,  # ✅ Convert list to JSON
            ],
        )
        return "Bank details updated successfully...!"
    except Exception as e:
        raise Exception(str(e))
