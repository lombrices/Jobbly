from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    lastname: Optional[str]
    phone_number: int
    address: Optional[str]
    rut: int
    age: int
    calification: float


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLoginBase(BaseModel):
    mail: EmailStr
    pass_hash: str  # Para crear y recibir el hash en lugar de la contraseña directa
    id_user: int

class UserLoginCreate(UserLoginBase):
    pass

class UserLogin(UserLoginBase):
    id: int

    class Config:
        from_attributes = True

class WorkerBase(BaseModel):
    id_user: int

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int

    class Config:
        from_attributes = True


class PetitionerBase(BaseModel):
    id_user: int

class PetitionerCreate(PetitionerBase):
    pass

class Petitioner(PetitionerBase):
    id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    id_worker: int
    title: str
    subtitle: str
    content: str
    init_date: date
    finish_date: Optional[date] = None
    price: int

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True

class PetitionerServiceBase(BaseModel):
    id_service: int
    id_petitioner: int
    petition_date: date
    solved: bool

class PetitionerServiceCreate(PetitionerServiceBase):
    pass

class PetitionerService(PetitionerServiceBase):
    id: int

    class Config:
        from_attributes = True


class EvaluationPetitionerBase(BaseModel):
    id_petitioner_service: int
    content: str
    calification: int

class EvaluationPetitionerCreate(EvaluationPetitionerBase):
    pass

class EvaluationPetitioner(EvaluationPetitionerBase):
    id: int

    class Config:
        from_attributes = True

class EvaluationWorkerBase(BaseModel):
    id_petitioner_service: int
    content: str
    calification: int

class EvaluationWorkerCreate(EvaluationWorkerBase):
    pass

class EvaluationWorker(EvaluationWorkerBase):
    id: int

    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    id_petitioner: int
    title: str
    subtitle: str
    content: str
    init_date: date
    finish_date: Optional[date] = None
    price: int

class RequestCreate(RequestBase):

    pass

class Request(RequestBase):
    id: int

    class Config:
        from_attributes = True

class WorkerRequestBase(BaseModel):
    id_worker: int
    id_request: int
    petition_date: date
    solved: bool

class WorkerRequestCreate(WorkerRequestBase):
    pass

class WorkerRequest(WorkerRequestBase):
    id: int

    class Config:
        orm_mode = True

class PetitionerReviewBase(BaseModel):
    id_worker_request: int
    content: str
    calification: int

class PetitionerReviewCreate(PetitionerReviewBase):
    pass

class PetitionerReview(PetitionerReviewBase):
    id: int

    class Config:
        from_attributes = True

class WorkerReviewBase(BaseModel):
    id_worker_request: int
    content: str
    calification: int

class WorkerReviewCreate(WorkerReviewBase):
    pass

class WorkerReview(WorkerReviewBase):
    id: int

    class Config:
        from_attributes = True
