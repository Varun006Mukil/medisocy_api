from utility.custom_base_model import CustomBaseModel


class VerifyOtpRequest(CustomBaseModel):
    otp: str
    trx_id: str
    mobile: str
    role: str
    fcm_token: str


class RefreshTokenRequest(CustomBaseModel):
    refresh_token: str
