from ninja import Schema


class MessageSchema(Schema):
    message: str | None


class LoginResponseSchema(Schema):
    token: str
    expired: str
