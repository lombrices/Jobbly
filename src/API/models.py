from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30))
    second_name = Column(String(30))
    lastname = Column(String(30))
    phone_number = Column(Integer, unique=True, nullable=False)
    address = Column(String(30))
    rut = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    calification = Column(REAL, nullable=False)

    # Define relaciones
    logins = relationship("UserLogin", back_populates="user")
    worker = relationship("Worker", back_populates="user", uselist=False)
    petitioner = relationship("Petitioner", back_populates="user", uselist=False)

class UserLogin(Base):
    __tablename__ = "user_login"

    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String(30), unique=True, nullable=False)
    pass_hash = Column(String(128), unique=True, nullable=False)  # Recomendación: almacenar contraseñas cifradas
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    user = relationship("User", back_populates="logins")

class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Definir relaciones
    user = relationship("User", back_populates="worker")
    service = relationship("Service", back_populates="worker")
    worker_request = relationship("WorkerRequest", back_populates="worker")

class Petitioner(Base):
    __tablename__ = "petitioner"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Definir relaciones
    user = relationship("User", back_populates="petitioner")
    request = relationship("Request", back_populates="petitioner")
    petitioner_service = relationship("PetitionerService", back_populates="petitioner")

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    id_worker = Column(Integer, ForeignKey("worker.id", ondelete="CASCADE"))
    title = Column(String(50), nullable = False)
    subtitle = Column(String(100), nullable = False)
    content = Column(Text)
    init_date = Column(Date, nullable=False)
    finish_date = Column(Date, nullable=True)
    price = Column(Integer, nullable=False)

    # Definir relaciones
    worker = relationship("Worker", back_populates="service")
    petitioner_service = relationship("PetitionerService", back_populates="service")
    
class PetitionerService(Base):
    __tablename__ = "petitioner_service"

    id = Column(Integer, primary_key=True, index=True)
    id_service = Column(Integer, ForeignKey("service.id", ondelete="CASCADE"))
    id_petitioner = Column(Integer, ForeignKey("petitioner.id", ondelete="CASCADE"))
    petition_date = Column(Date, nullable=False)
    solved = Column(Boolean)

    # Definir relaciones
    service = relationship("Service", back_populates="petitioner_service")
    petitioner = relationship("Petitioner", back_populates="petitioner_service")
    evaluation_petitioner = relationship("EvaluationPetitioner", back_populates="petitioner_service", uselist=False)
    evaluation_worker = relationship("EvaluationWorker", back_populates="petitioner_service", uselist=False)

class EvaluationPetitioner(Base):
    __tablename__ = "evaluation_petitioner"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner_service = Column(Integer, ForeignKey("petitioner_service.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner_service = relationship("PetitionerService", back_populates="evaluation_petitioner")

class EvaluationWorker(Base):
    __tablename__ = "evaluation_worker"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner_service = Column(Integer, ForeignKey("petitioner_service.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner_service = relationship("PetitionerService", back_populates="evaluation_worker")

class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    id_petitioner = Column(Integer, ForeignKey("petitioner.id", ondelete="CASCADE"))
    title = Column(String(100), nullable = False)
    subtitle = Column(String(100), nullable = False)
    content = Column(Text)
    init_date = Column(Date, nullable=False) 
    finish_date = Column(Date, nullable=True)
    price = Column(Integer, nullable=False)

    # Definir relaciones
    petitioner = relationship("Petitioner", back_populates="request")
    worker_request = relationship("WorkerRequest", back_populates="request")

class WorkerRequest(Base):
    __tablename__ = "worker_request"

    id = Column(Integer, primary_key=True, index=True)
    id_worker = Column(Integer, ForeignKey("worker.id", ondelete="CASCADE"))
    id_request = Column(Integer, ForeignKey("request.id", ondelete="CASCADE"))
    petition_date = Column(Date, nullable=False)
    solved = Column(Boolean)

    # Definir relaciones
    worker = relationship("Worker", back_populates="worker_request")
    request = relationship("Request", back_populates="worker_request")
    petitioner_review = relationship("PetitionerReview", back_populates="worker_request", uselist=False)
    worker_review = relationship("WorkerReview", back_populates="worker_request", uselist=False)

class PetitionerReview(Base):
    __tablename__ = "petitioner_review"

    id = Column(Integer, primary_key=True, index=True)
    id_worker_request = Column(Integer, ForeignKey("worker_request.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    worker_request = relationship("WorkerRequest", back_populates="petitioner_review")

class WorkerReview(Base):
    __tablename__ = "worker_review"

    id = Column(Integer, primary_key=True, index=True)
    id_worker_request = Column(Integer, ForeignKey("worker_request.id"), unique=True, nullable=False)
    content = Column(Text)
    calification = Column(Integer, nullable=False)

    # Definir relaciones
    worker_request = relationship("WorkerRequest", back_populates="worker_review")