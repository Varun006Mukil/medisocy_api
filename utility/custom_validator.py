import re

def custom_validator(validation, data: dict):
    try:
        for rule in validation:
            field = rule['field']
            data_type = rule['data_type']
            validation_type = rule['validate']
            
            # Get the value from request
            value = data.get(field)
            # Check for empty or None value
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ValueError(f"Field '{field}' is required and cannot be empty.")
                
            # Validate data type if no specific validation type
            if validation_type == "":
                if data_type == "int":
                    if not isinstance(value, int):
                        raise TypeError(f"Field '{field}' must be of type {data_type}.")
                elif data_type == "str":
                    if not isinstance(value, str):
                        raise TypeError(f"Field '{field}' must be of type {data_type}.")
                elif data_type == "bool":
                    if not isinstance(value, bool):
                        raise TypeError(f"Field '{field}' must be of type {data_type}.")
                elif data_type == "list_str":
                        if not isinstance(value, list):
                            raise TypeError(f"Field '{field}' must be a list.")
                        if not value:
                             raise ValueError(f"Field '{field}' must not be an empty list.")
                        if not all(isinstance(item, str) for item in value):
                         raise TypeError(f"All items in '{field}' must be of type str.")
                elif data_type == "list_int":
                        if not isinstance(value, list):
                            raise TypeError(f"Field '{field}' must be a list.")
                        if not value:
                             raise ValueError(f"Field '{field}' must not be an empty list.")
                        if not all(isinstance(item, str) for item in value):
                         raise TypeError(f"All items in '{field}' must be of type int.")     
                            
            
            # Additional validation based on 'validate'
            if validation_type == "email":
                if not is_valid_email(value):  # Ensure `is_valid_email` is implemented properly
                    raise ValueError(f"Field '{field}' must be a valid email address.")
                
        # If all validations pass, return the data
        return data
    except Exception as e:
        raise Exception(f"Validation error: {str(e.args[0])}") from e

    
    
def is_valid_email(email):
    # Regex pattern for basic email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))   