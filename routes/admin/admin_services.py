from routes.admin.admin_model import AdminDetails
from routes.common.common_model import LoginResponse
from utility.utility import (
    create_access_token,
    create_refresh_token,
    execute_stored_procedure,
)


async def adminLogin(name=None):
    try:
        users = await execute_stored_procedure(
            proc_name="admin_validate", params=[name], is_one=True
        )
        if users:
            user_details = AdminDetails(
                user_id=users.get("id"),
                name=users.get("name"),
                role="admin",
                status=users.get("status"),
            )
            result = await createTokens(user=user_details)
            return result
        else:
            return Exception("something went wrong...!")
    except Exception as e:
        raise Exception(str(e.args))


async def createTokens(user):
    try:
        ac_token = create_access_token(user=user)
        rf_token = create_refresh_token(user=user)
        result = LoginResponse(
            access_token=ac_token,
            refresh_token=rf_token,
            user_id=user.user_id,
            name=user.name,
            category_id=None,
            status=user.status,
        ).to_json()
        return result
    except Exception as e:
        raise Exception(str(e.args))


async def getDoctors(id=None, tag=None):
    try:
        data = await execute_stored_procedure(
            proc_name="get_doctor_details",
            params=[id, tag],
        )
        return data

    except Exception as e:
        raise Exception(str(e))
