from flask import Flask, request, render_template, redirect
from models import PayrollModel, UserModel, db, EmployeeModel, ProjectModel, DepartmentModel
from sqlalchemy import insert, update

app = Flask(__name__, template_folder="templates")

# database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrms.db'
app.config['SQLALCHEMY_track_modifications'] = False
db.init_app(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
  return render_template("landing.html")

@app.route('/admin_dashboard')
def admin_dashboard():
  return render_template("admin_dashboard.html")

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    emp=EmployeeModel.query.filter_by(id=id).first()
    dept=DepartmentModel.query.filter_by(dept_id=emp.dept_id).first()
    project=ProjectModel.query.filter_by(p_id=emp.p_id).first()
    payroll=PayrollModel.query.filter_by(employee_id=emp.id).first()
    
    return render_template('profile.html',current_user=emp, dept=dept, project=project,payroll=payroll)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

  if request.method == "GET":
    return render_template("admin_login.html")

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form['password']

    if username=='admin' and password=='admin@2023':
      return render_template('admin_dashboard.html')
    else:
      return('Incorrect admin credentials!!')
  return redirect("/")
  

@app.route('/login', methods=['GET', 'POST'])
def login():

  if request.method == "GET":
    return render_template("login.html")

  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form['password']

    user = UserModel.query.filter_by(username=username).first()
    user_data = UserModel.query.filter_by(username=username, password=password).first()
    #emp_id = user_data.employee_id
    #print(user_data.employee_id,user_data.username)
    emp=EmployeeModel.query.filter_by(id=user_data.employee_id).first()
    #print(emp.first_name)
    if user is None:
      return('No username present')
      #return render_template('login.html')
    elif user_data:
      #flash("You are now logged in!!","success")
      return render_template("user_dashboard.html", current_user=emp)
    else:
      return('Incorrect Username or Password')
      #return render_template('login.html')
  return redirect('/')

@app.route('/logout')
def logout():
  return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():

  if request.method == "GET":
    return render_template("register.html")

  if request.method == 'POST':
    username = request.form.get('username')
    employee_id = request.form['employee_id']
    Name = request.form['Name']
    password = request.form['password']

    user_id = UserModel.query.filter_by(employee_id=employee_id).first()
    user_name = UserModel.query.filter_by(username=username).first()
    emp_id = EmployeeModel.query.filter_by(id=employee_id).first()

    #print(emp_id)
    if emp_id:
      if user_id:
        return f'Sorry! User with employee id "{employee_id}" already exists.'
      elif user_name:
        return f'Sorry! User "{username}" already exists.'
      else:
        user = UserModel(username=username,
                        employee_id=employee_id,
                        Name=Name,
                        password=password)
        db.session.add(user)
        db.session.commit()
        render_template('header.html')
    else:
      return f'Sorry! employee with id "{employee_id}" does not exist.'
  return redirect('/')

@app.route('/add_employee', methods=["GET", "POST"])
def add_employee():
  if request.method == "GET":
    return render_template("employees/add_employee.html", dept_list=dept_list(), projects_list=project_list())

  if request.method == 'POST':
    first_name = request.form.get('first_name')
    last_name = request.form['last_name']
    emp_email = request.form['emp_email']
    emp_address = request.form['emp_address']
    middle_name = request.form['middle_name']
    emp_dob = request.form['emp_dob']
    dept_id = request.form['dept_id']
    p_id = request.form['p_id']
    emp_phone = request.form['emp_phone']
    emp_manager_id = request.form['emp_manager_id']
    gender = request.form['gender']

    email = EmployeeModel.query.filter_by(emp_email=emp_email).first()
    if email:
      return f'Sorry! employee with email id "{emp_email}" already exists.'
  
    employee = EmployeeModel(first_name=first_name,
                            middle_name=middle_name,
                            last_name=last_name,
                            emp_email=emp_email,
                            gender=gender,
                            emp_manager_id=emp_manager_id,
                            emp_phone=emp_phone, 
                            p_id=p_id, 
                            emp_dob=emp_dob, 
                            dept_id=dept_id,
                            emp_address=emp_address)
    db.session.add(employee)
    db.session.commit()
    return redirect('/employee_list')


@app.route('/employee_list', methods=['GET'])
def retrieveEmployees():
  employee_list = EmployeeModel.query.all()
  return render_template("employees/list_employee.html", employee_list = employee_list)


@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
  employee = EmployeeModel.query.filter_by(id=id).first()
  if request.method == 'POST':
    if employee:
      db.session.delete(employee)
      db.session.commit()
      return redirect('/employee_list')
    abort(404)
  return render_template('employees/delete_employee.html')


@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
  employee = EmployeeModel.query.filter_by(id=id).first()

  if request.method == 'POST':
    if employee:     
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      emp_email = request.form['emp_email']
      emp_address = request.form['emp_address']
      middle_name = request.form['middle_name']
      emp_dob = request.form['emp_dob']
      dept_id = request.form['dept_id']
      p_id = request.form['p_id']
      emp_phone = request.form['emp_phone']
      emp_manager_id = request.form['emp_manager_id']
      gender = request.form['gender']
      stmt = (update(EmployeeModel).where(EmployeeModel.id == id).values(first_name=first_name,
                                                                          middle_name=middle_name,
                                                                          last_name=last_name,
                                                                          emp_email=emp_email,
                                                                          gender=gender,
                                                                          emp_manager_id=emp_manager_id,
                                                                          emp_phone=emp_phone, 
                                                                          p_id=p_id, 
                                                                          emp_dob=emp_dob, 
                                                                          dept_id=dept_id,
                                                                          emp_address=emp_address)
              )
      db.session.execute(stmt)
      db.session.commit()
      return redirect('/employee_list')
    else:
      return f'Sorry! Employee with id "{id}" does not exist.'
  return render_template('employees/edit_employee.html', employee = employee)

@app.route('/add_project', methods=["GET", "POST"])
def add_project():
  if request.method == "GET":
    return render_template("projects/add_project.html", dept_list=dept_list())

  if request.method == 'POST':
    p_name = request.form.get('p_name')
    p_location = request.form['p_location']
    p_client = request.form['p_client']
    dept_id = request.form['dept_id']
    p_description = request.form['p_description']

    project = ProjectModel(p_name=p_name,
                           p_client=p_client,
                           dept_id=dept_id,
                           p_location=p_location,
                           p_description=p_description)
    db.session.add(project)
    db.session.commit()
    return redirect('/project_list')


@app.route('/project_list', methods=['GET'])
def retrieveProjects():
  project_list = ProjectModel.query.all()
  return render_template("projects/list_project.html", project_list = project_list)


@app.route('/delete_project/<int:p_id>', methods=['GET', 'POST'])
def delete_project(p_id):
  project = ProjectModel.query.filter_by(p_id=p_id).first()
  if request.method == 'POST':
    if project:
      db.session.delete(project)
      db.session.commit()
      return redirect('/project_list')
    #abort(404)
  return render_template('projects/delete_project.html')

@app.route('/edit_project/<int:p_id>', methods=['GET', 'POST'])
def edit_project(p_id):
  project = ProjectModel.query.filter_by(p_id=p_id).first()

  if request.method == 'POST':
    if project:     
      p_name = request.form['p_name']
      p_location = request.form['p_location']
      p_client = request.form['p_client']
      dept_id = request.form['dept_id']
      p_description = request.form['p_description']
      stmt = (update(ProjectModel).where(ProjectModel.p_id == p_id).values(p_name=p_name,
                                                                           p_location=p_location,
                                                                           p_client=p_client,
                                                                           dept_id=dept_id,
                                                                           p_description=p_description)
              )
      db.session.execute(stmt)
      db.session.commit()
      return redirect('/project_list')
    else:
      return f'Sorry! Project "{p_name}" with id "{p_id}" does not exist.'
  return render_template('projects/edit_project.html', project = project)


def dept_list():
  depts = DepartmentModel.query.all()
  depts_list = [(dept.dept_id,dept.dept_name) for dept in depts]
  return depts_list

def project_list():
  projects_query = ProjectModel.query.all()
  projects_list = [(projects.p_id,projects.p_name) for projects in projects_query]
  return projects_list
  
@app.route('/add_department', methods=["GET", "POST"])
def add_department():
  if request.method == "GET":
    return render_template("department/add_department.html")

  if request.method == 'POST':
    dept_name = request.form.get('dept_name')
    dept_location = request.form['dept_location']
    dept_desc = request.form['dept_description']

    department = DepartmentModel(dept_name=dept_name,
                           dept_location=dept_location,
                           dept_description=dept_desc)
    db.session.add(department)
    db.session.commit()
    return redirect('/department_list')


@app.route('/department_list', methods=['GET'])
def retrieveDepartment():
  department_list = DepartmentModel.query.all()
  return render_template("department/list_department.html", department_list = department_list)


@app.route('/delete_department/<int:dept_id>', methods=['GET', 'POST'])
def delete_department(dept_id):
  department = DepartmentModel.query.filter_by(dept_id=dept_id).first()
  if request.method == 'POST':
    if department:
      db.session.delete(department)
      db.session.commit()
      return redirect('/department_list')
    abort(404)
  return render_template('department/delete_department.html')

@app.route('/edit_department/<int:dept_id>', methods=['GET', 'POST'])
def edit_department(dept_id):
  department = DepartmentModel.query.filter_by(dept_id=dept_id).first()
  if request.method == 'POST':
    if department:     
      name = request.form['dept_name']
      location = request.form['dept_location']
      desc = request.form['dept_description']
      stmt = (update(DepartmentModel).where(DepartmentModel.dept_id == dept_id).values(
                                                                                dept_name=name,
                                                                                dept_location=location,
                                                                                dept_description=desc
                                                                                )
              )
      db.session.execute(stmt)
      db.session.commit()
      return redirect('/department_list')
    else:
      return f'Sorry! Department "{name}" with id "{dept_id}" does not exist.'
  return render_template('department/edit_department.html', department = department)


@app.route('/add_payroll', methods=["GET", "POST"])
def add_payroll():
  if request.method == "GET":
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    return render_template("payroll/add_payroll.html",months=months)

  if request.method == 'POST':
    pay_month = request.form['pay_month']
    employee_id = request.form['employee_id']
    amount = request.form['amount']
    pay_date = request.form['pay_date']

    record = EmployeeModel.query.filter_by(id=employee_id).first()
    if record:
      stmt = insert(PayrollModel).values(pay_month=pay_month, employee_id=employee_id,amount=amount,pay_date=pay_date)
      db.session.execute(stmt)
      db.session.commit()    
      return redirect('/payroll_list')
    else:
      return f'Sorry! Employee with id "{employee_id}" does not exist.'


@app.route('/payroll_list', methods=['GET'])
def retrievePayrolls():
  payroll_list = PayrollModel.query.all()
  return render_template("payroll/list_payroll.html", payroll_list = payroll_list)


@app.route('/delete_payroll/<int:pay_id>', methods=['GET', 'POST'])
def delete_payroll(pay_id):
  payroll = PayrollModel.query.filter_by(pay_id=pay_id).first()
  if request.method == 'POST':
    if payroll:
      db.session.delete(payroll)
      db.session.commit()
      return redirect('/payroll_list')
    abort(404)
  return render_template('payroll/delete_payroll.html')

@app.route('/edit_payroll/<int:pay_id>', methods=['GET', 'POST'])
def edit_payroll(pay_id):
  payroll = PayrollModel.query.filter_by(pay_id=pay_id).first()
  if request.method == 'POST':
    if payroll:     
      pay_month = request.form['pay_month']
      #employee_id = request.form['employee_id']
      amount = request.form['amount']
      pay_date = request.form['pay_date']
      stmt = (update(PayrollModel).where(PayrollModel.pay_id == pay_id).values(pay_month=pay_month, 
                                                                                       #employee_id=employee_id,
                                                                                       amount=amount,
                                                                                       pay_date=pay_date)
              )
      db.session.execute(stmt)
      db.session.commit()
      return redirect('/payroll_list')
    else:
      return f'Sorry! Payroll with id "{pay_id}" does not exist.'
  return render_template('payroll/edit_payroll.html', payroll = payroll)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
