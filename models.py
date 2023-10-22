from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


db = SQLAlchemy()

class EmployeeModel(db.Model):
  __tablename__ = 'employees'

  id = db.Column(db.Integer, primary_key = True)

  first_name = db.Column(db.String(255), nullable=False)
  middle_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255), nullable=False)

  emp_email = db.Column(db.String(255), nullable=False, unique=True)
  gender = db.Column(db.String(255), nullable=False)
  emp_dob=db.Column(db.String(), nullable=False)

  emp_phone = db.Column(db.Integer, nullable=False)
  emp_manager_id = db.Column(db.Integer, nullable=False)
  p_id = db.Column(db.Integer, nullable=False)

  dept_id = db.Column(db.Integer, nullable=False)
  #age = db.Cpolumn(db.Integer)
  emp_address = db.Column(db.String(255), nullable=False)

  def __init__(self,  first_name, last_name, middle_name, emp_email, emp_manager_id, 
               gender, emp_phone, p_id, emp_dob, dept_id, emp_address):
    #self.employee_id = employee_id
    self.first_name = first_name
    self.last_name = last_name
    self.emp_email = emp_email
    self.emp_phone = emp_phone
    self.emp_manager_id = emp_manager_id
    self.emp_dob=emp_dob
    self.gender = gender
    self.p_id = p_id
    self.middle_name = middle_name
    self.last_name = last_name
    self.dept_id = dept_id
    self.emp_address = emp_address

    def __repr__(self):
      return f"{self.first_name},{self.last_name}"
    

class ProjectModel(db.Model):
  __tablename__ = 'projects'

  p_id = db.Column(db.Integer, primary_key = True)

  p_name = db.Column(db.String(255), nullable=False)
  p_location = db.Column(db.String(255))
  p_client = db.Column(db.String(255), nullable=False)
  dept_id = db.Column(db.Integer, nullable=False)
  p_description = db.Column(db.String())

  def __init__(self, p_name, p_location, p_client, dept_id, p_description):
    self.p_name = p_name
    self.p_location = p_location
    self.p_client = p_client
    self.dept_id = dept_id
    self.p_description = p_description

    def __repr__(self):
      return f"{self.p_name}"
    

class DepartmentModel(db.Model):
  __tablename__ = 'departments'

  dept_id = db.Column(db.Integer, primary_key = True)

  dept_name = db.Column(db.String(255), nullable=False)
  dept_location = db.Column(db.String(255))
  dept_description = db.Column(db.String())

  def __init__(self, dept_name, dept_location, dept_description):
    self.dept_name = dept_name
    self.dept_location = dept_location
    self.dept_description = dept_description

  def update_row(self, dept_id,dept_name, dept_location, dept_description):
    self.dept_name = dept_name
    dept_id=dept_id
    self.dept_location = dept_location
    self.dept_description = dept_description

  def __repr__(self):
    return f"{self.dept_name}"
  

class RoleModel(db.Model):
  __tablename__ = 'roles'

  role_id = db.Column(db.Integer, primary_key=True)
  role_name = db.Column(db.String(60), unique=True)
  role_description = db.Column(db.String(200))
  #employees = db.relationship('Employee', backref='role',lazy='dynamic')

  def __repr__(self):
    return '{}'.format(self.name)


  



class PayrollModel(db.Model):
  __tablename__ = "payroll"

  pay_id = db.Column(db.Integer, primary_key=True)
    # employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
  pay_month = db.Column(db.String(), nullable=False)
  employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
  amount = db.Column(db.Integer, nullable=False)
  pay_date = db.Column(db.String(), nullable=False)
  #payroll = relationship("employees", back_populates = "employees")

  def __init__(self, pay_month,employee_id,amount,pay_date):
    self.pay_month=pay_month
    self.employee_id=employee_id
    self.pay_date=pay_date
    self.amount=amount

  def __str__(self):
    return f"<Payment {self.pay_id} - {self.amount} />"
  


class UserModel(db.Model):
  __tablename__ = "users"

  username = db.Column(db.String, primary_key=True)
    # employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
  Name = db.Column(db.String(), nullable=False)
  employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
  password = db.Column(db.String, nullable=False)
  #pay_date = db.Column(db.String(), nullable=False)
  #payroll = relationship("employees", back_populates = "employees")

  def __init__(self, username,employee_id,password,Name):
    #self.pay_month=pay_month
    self.username=username
    self.employee_id=employee_id
    self.Name=Name
    self.password=password

  def __str__(self):
    return f"<Payment {self.username} - {self.password} />"