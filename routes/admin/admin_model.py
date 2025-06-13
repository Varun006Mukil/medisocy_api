class AdminDetails:
    user_id: int
    name: str
    role: str
    status: bool

    def __init__(self, user_id: int, name: str, role: str, status: bool) -> None:
        self.user_id = user_id
        self.name = name
        self.role = role
        self.status = status

    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
        }

