
from pydantic import BaseModel, model_validator


class CustomBaseModel(BaseModel):
    @model_validator(mode="after")
    def check_no_empty_values(cls, model):
        def validate(value: any):
            # Check for empty string (whitespace only too)
            if isinstance(value, str) and not value.strip():
                raise ValueError("Empty strings are not allowed")

            # Check for empty list
            elif isinstance(value, list):
                if not value:
                    raise ValueError("Empty lists are not allowed")
                for v in value:
                    validate(v)

            # Check for empty dict
            elif isinstance(value, dict):
                if not value:
                    raise ValueError("Empty dicts are not allowed")
                for v in value.values():
                    validate(v)

            # Check for nested Pydantic models
            elif isinstance(value, BaseModel):
                for v in value.__dict__.values():
                    validate(v)

            return value

        validate(model)
        return model