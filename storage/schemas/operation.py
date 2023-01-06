from pydantic import BaseModel


class Operation(BaseModel):
    id: int
    type: str
    current_operation: object


class OperationBase(BaseModel):
    id: int
    unix_time: int
    description: str
    amount: int
    mcc: int


class ManualOperation(OperationBase):
    category: str
