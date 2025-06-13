from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from routes.customer import customer_view
from routes.common import common_view
from routes.doctor import doctor_view
from utility.utility import custom_validation_exception_handler

app = FastAPI()

app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.include_router(common_view.common_router, prefix="/common")
app.include_router(customer_view.router, prefix="/customer")
app.include_router(doctor_view.doctor_routers, prefix="/doctor")


@app.get("/")
def read_root():
    return "API is working"
