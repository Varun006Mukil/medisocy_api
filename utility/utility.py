from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pymysql import DatabaseError
from database import get_connection
import datetime
from routes.common.common_model import UserDetails
from settings import Settings
import jwt
from utility.custom_response import CustomResponse


settings = Settings()


# Function to execute store procedure
async def execute_stored_procedure(proc_name, params=None, is_one=False):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc(procname=proc_name, args=params or [])
            result = []

            while True:
                if is_one : 
                    row = cursor.fetchone()
                    if row:
                        columns = [col[0] for col in cursor.description]   
                        result.append(dict(zip(columns,row))) 
                    else:
                        result.append([])
                else:
                    row = cursor.fetchall()
                    if row:
                        columns = [col[0] for col in cursor.description]
                        row_set = [dict(zip(columns,row)) for row in row]
                        result.append(row_set)
                    else:
                        result.append([])
                if not cursor.nextset():
                    break
            conn.commit()
            return result[0] if is_one and result else result
    except DatabaseError as e:
        conn.rollback()
        raise Exception(str(e.args[1])) from e
    except Exception as e:
        conn.rollback()
        raise Exception(f"Unknown error in `{proc_name}`: {str(e)}") from e
    finally:
        conn.close()


# Function to execute query or function
async def execute_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            print(row)
            return row[0] if row else None
    except DatabaseError as e:
        raise Exception(f"DB Error: {str(e.args[1])}") from e
    except Exception as e:
        raise Exception(f"Unknown errordd: {str(e)}") from e
    finally:
        conn.close()
    # Function create access token and return token.


def create_access_token(user:UserDetails) -> str:
    print(user.user_id)
    try:
        payload = {
            "user_id": user.user_id,
            "username": user.name,
            "role": user.role,
            "exp": datetime.datetime.utcnow()
                   + datetime.timedelta(minutes=120),  # Access token expiry
            "iat": datetime.datetime.utcnow(),
            "aud": "mmp",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    except Exception as error:
        raise Exception(str(error)) from error


def create_refresh_token(user:UserDetails) -> str:
    try:
        payload = {
            "user_id": user.user_id,
            "role": user.role,
            "type": "refresh",
            "exp": datetime.datetime.utcnow()
                   + datetime.timedelta(minutes=180),  # Refresh token expiry
            "iat": datetime.datetime.utcnow(),
            "aud": "mmp",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
    except Exception as error:
        raise Exception(str(error)) from error


def token_validator(request: Request):
    token = request.headers.get("Authorization")
    print(token)
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        if token.startswith("Bearer "):
            token_parts = token.split(" ")
            if len(token_parts) == 2:
                decoded = jwt.decode(
                    token_parts[1],
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                    audience="mmp",
                    options={
                        "require_iat": True,
                        "require_exp": True,
                    },
                    leeway=30,
                )
                id = decoded.get("user_id")
                role = decoded.get("role")
                result = execute_query("select check_user(%s,%s)", [int(id), role])
                if result:
                    return {"user_id": id}
                else:
                    raise HTTPException(status_code=401, detail="Unauthorized token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = ".".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": loc.replace("body.", ""),  # remove 'body.' prefix
            "message": err.get("msg"),
            "type": err.get("type")
        })
    return CustomResponse(
        code=400,
        status=False,
        message=str(errors),
    )
