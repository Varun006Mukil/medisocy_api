from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from routes.admin import admin_view
from routes.customer import customer_view
from routes.common import common_view
from routes.doctor import doctor_view
from utility.utility import custom_validation_exception_handler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
),

app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.include_router(admin_view.admin_router,prefix="/admin")
app.include_router(common_view.common_router, prefix="/common")
app.include_router(customer_view.router, prefix="/customer")
app.include_router(doctor_view.doctor_routers, prefix="/doctor")


@app.get("/")
def read_root():
    return "API is working"
