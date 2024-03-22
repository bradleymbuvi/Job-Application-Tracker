import click
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    website = Column(String(120))
    contact_info = Column(String(255))

    # Define a relationship with Job model (one-to-many)
    jobs = relationship("Job", backref="company")

    # Define a relationship with Contact model (one-to-many)
    contacts = relationship("Contact", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='contacts')
    job_applications = relationship('JobApplication', back_populates='contact', overlaps='job_applications_list')

    
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
    status = Column(String(20), default="applied")

    # Define property method to ensure applied date format
    @property
    def applied_date(self):
        return self._applied_date

    @applied_date.setter
    def applied_date(self, value):
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid applied date format (YYYY-MM-DD)")

        self._applied_date = value
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company.name}')>"
    
class JobApplication(Base):
    __tablename__ = 'job_applications'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    applied_date = Column(String)
    link = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref='job_applications')
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship('Contact', backref='job_applications_list')

    def __repr__(self):
        return f'<JobApplication(title={self.title}, company={self.company.name}, contact={self.contact.name})>'


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
        click.echo("Companies:")
        for company in companies:
            click.echo(f"- {company.name}")
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
def contact():
    pass

@contact.command()
@click.argument("company_name")
@click.argument("name")
@click.argument("email")
@click.option("--job_title")
@click.option("--job_description")
@click.option("--applied_date")
@click.option("--link")
def add(company_name, name, email, job_title=None, job_description=None, applied_date=None, link=None):
    try:
        company = session.query(Company).filter(Company.name == company_name).first()
        if not company:
            raise ValueError(f"Company '{company_name}' not found.")

        new_contact = Contact(name=name, email=email, company=company)
        session.add(new_contact)

        if job_title and job_description and applied_date:
            new_job_application = JobApplication(
                title=job_title,
                description=job_description,
                applied_date=applied_date,
                link=link,
                company=company,
                contact=new_contact
            )
            session.add(new_job_application)

        session.commit()
        click.echo(f"Contact '{name}' added successfully!")
    except Exception as e:
        click.echo(f"Error: {e}")



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
    try:
        # Find company by name (assuming unique company names)
        company = session.query(Company).filter_by(name=company_name).first()
        if not company:
            click.echo(f"Company '{company_name}' not found. Please create the company first.")
            return

        # Validate and create new job record
        new_job = Job(company=company, title=title, description=description, applied_date=applied_date, link=link)
        session.add(new_job)
        session.commit()
        click.echo(f"Job '{title}' for company '{company_name}' created successfully!")
    except Exception as e:
        click.echo(f"Error: {e}")


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
@click.option("--status", type=str, help="Status to update the job application to")
def update_status(job_id, status):
    try:
        job_application = session.query(JobApplication).get(job_id)
        if job_application:
            job_application.status = status
            session.commit()
            click.echo(f"Job application {job_id} status updated to '{status}'")
        else:
            click.echo(f"Job application with ID {job_id} not found.")
    except Exception as e:
        click.echo(f"Error: {e}")

@job.command()
def list():
    jobs = session.query(Job).all()
    if jobs:
        click.echo("Jobs:")
        for job in jobs:
            click.echo(f"- {job}")
    else:
        click.echo("No jobs found.")


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