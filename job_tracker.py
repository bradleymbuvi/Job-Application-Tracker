from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    website = Column(String(120))
    contact_info = Column(String(255))

    # Define a relationship with Job model (one-to-many)
    jobs = relationship("Job", backref="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String(80), nullable=False)
    description = Column(String(255))
    applied_date = Column(String(20))
    link = Column(String(120))

    # Define property method to ensure applied date format
    @property
    def applied_date(self):
        return self._applied_date

    @applied_date.setter
    def applied_date(self, value):
        # Validate date format (YYYY-MM-DD)
        if not value or len(value) != 10 or not value.isdigit() or not (value[4] == "-" and value[7] == "-"):
            raise ValueError("Invalid applied date format (YYYY-MM-DD)")
        self._applied_date = value

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company.name}')>"

engine = create_engine("sqlite:///job_tracker.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()