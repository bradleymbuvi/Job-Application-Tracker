import click
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

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='contacts')

    def __repr__(self):
        return f'<Contact(name={self.name}, email={self.email})>'


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

@click.group()
def cli():
    """Job Application Tracker CLI"""
    pass

@cli.group()
def company():
    pass

@company.command()
@click.argument("name")
@click.option("--website")
@click.option("--contact_info")
def create(name, website=None, contact_info=None):
    try:
        new_company = Company(name=name, website=website, contact_info=contact_info)
        session.add(new_company)
        session.commit()
        click.echo(f"Company '{name}' created successfully!")
    except Exception as e:
        click.echo(f"Error: {e}")

@company.command()
def list():
    companies = session.query(Company).all()
    if companies:
        for company in companies:
            click.echo(company)
    else:
        click.echo("No companies found.")

@company.command()
@click.argument("company_id", type=int)
def delete(company_id):
    try:
        company = session.query(Company).get(company_id)
        if company:
            session.delete(company)
            session.commit()
            click.echo(f"Company '{company.name}' deleted successfully!")
        else:
            click.echo(f"Company with ID {company_id} not found.")
    except Exception as e:
        click.echo(f"Error: {e}")

@company.command()
@click.argument("company_id", type=int)
def find(company_id):
    company = session.query(Company).get(company_id)
    if company:
        click.echo(company)
    else:
        click.echo(f"Company with ID {company_id} not found.")

@company.command()
@click.argument("company_id", type=int)
def jobs(company_id):
    company = session.query(Company).get(company_id)
    if company:
        if company.jobs:
            click.echo(f"Jobs for company '{company.name}':")
            for job in company.jobs:
                click.echo(f"\t- {job}")
        else:
            click.echo(f"No jobs found for company '{company.name}'.")
    else:
        click.echo(f"Company with ID {company_id} not found.")


@cli.group()
def job():
    pass

@job.command()
@click.argument("company_name")
@click.argument("title")
@click.option("--description")
@click.option("--applied_date")
@click.option("--link")
def create(company_name, title, description=None, applied_date=None, link=None):
    # Implement your create logic here
    pass

@job.command()
@click.argument("job_id", type=int)
def delete(job_id):
    try:
        job = session.query(Job).get(job_id)
        if job:
            session.delete(job)
            session.commit()
            click.echo(f"Job '{job.title}' deleted successfully!")
        else:
            click.echo(f"Job with ID {job_id} not found.")
    except Exception as e:
        click.echo(f"Error: {e}")

@job.command()
@click.argument("job_id", type=int)
def find(job_id):
    job = session.query(Job).get(job_id)
    if job:
        click.echo(job)
    else:
        click.echo(f"Job with ID {job_id} not found.")

if __name__ == "__main__":
    cli()