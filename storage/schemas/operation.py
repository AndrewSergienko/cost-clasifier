from pydantic import BaseModel


class OperationBase(BaseModel):
    id: int | None
    description: str
    amount: int
    mcc: int

    class Config:
        orm_mode = True


class OperationReadBase(OperationBase):
    unix_time: int


class ManualOperationRead(OperationReadBase):
    category: str


