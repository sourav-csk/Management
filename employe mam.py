import http.server
import urllib.parse
import json
import os

PORT = 8000
DATA_FILE = 'employees.json'
employees = []

# ------------------ DATA HANDLING ------------------

def load_employees():
    global employees
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            employees = json.load(f)
    else:
        employees = []

def save_employees():
    with open(DATA_FILE, 'w') as f:
        json.dump(employees, f, indent=4)

# ------------------ HTTP HANDLER ------------------

class EmployeeHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # -------- HOME PAGE (ADD EMPLOYEE) --------
        if self.path == '/':

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px; width: 250px; }
        button { background: green; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>

<h1>Add Employee</h1>

<form method="POST" action="/employees">
    <input type="text" name="employee_name" placeholder="Employee Name" required><br>
    <input type="text" name="department" placeholder="HR / Engineering / Sales / Marketing" required><br>
    <input type="text" name="position" placeholder="Position" required><br>
    <input type="date" name="hire_date" required><br>
    <input type="email" name="email" placeholder="Email" required><br>
    <input type="text" name="mobile_number" placeholder="10 Digit Mobile" required><br>
    <input type="text" name="permanent_address" placeholder="Address" required><br>
    <input type="text" name="nationality" placeholder="Nationality" required><br>
    <input type="text" name="employee_type" placeholder="Full-time / Part-time / Contract" required><br>
    <input type="checkbox" name="isactive" value="1"> Is Active <br><br>
    <button type="submit">Add Employee</button>
</form>

</body>
</html>
"""
            self.wfile.write(html.encode())

        # -------- EMPLOYEES LIST PAGE --------
        elif self.path == '/employees':

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            rows = ""
            for emp in employees:
                rows += f"""
                <tr>
                    <td>{emp['id']}</td>
                    <td>{emp['employee_name']}</td>
                    <td>{emp['department']}</td>
                    <td>{emp['position']}</td>
                    <td>{emp['email']}</td>
                    <td>{'Yes' if emp['isactive'] == '1' else 'No'}</td>
                </tr>
                """

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Employees List</title>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        table {{ border-collapse: collapse; width: 90%; }}
        th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
        th {{ background: #f2f2f2; }}
        a {{ display: inline-block; margin-top: 20px; }}
    </style>
</head>
<body>

<h1>Employees List</h1>

<table>
<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Department</th>
    <th>Position</th>
    <th>Email</th>
    <th>Active</th>
</tr>
{rows}
</table>

<a href="/">⬅ Add New Employee</a>

</body>
</html>
"""
            self.wfile.write(html.encode())

    # -------- SAVE EMPLOYEE --------
    def do_POST(self):
        if self.path == '/employees':

            length = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(self.rfile.read(length).decode())

            employee_name = data.get('employee_name', [''])[0]
            department = data.get('department', [''])[0]
            position = data.get('position', [''])[0]
            hire_date = data.get('hire_date', [''])[0]
            email = data.get('email', [''])[0]
            mobile = data.get('mobile_number', [''])[0]
            address = data.get('permanent_address', [''])[0]
            nationality = data.get('nationality', [''])[0]
            employee_type = data.get('employee_type', [''])[0]
            isactive = data.get('isactive', [''])[0]

            # -------- VALIDATION --------
            if department not in ['HR', 'Engineering', 'Sales', 'Marketing']:
                self.send_error(400, "Invalid Department")
                return

            if '@' not in email:
                self.send_error(400, "Invalid Email")
                return

            if not mobile.isdigit() or len(mobile) != 10:
                self.send_error(400, "Invalid Mobile Number")
                return

            if employee_type not in ['Full-time', 'Part-time', 'Contract']:
                self.send_error(400, "Invalid Employee Type")
                return

            # -------- SAVE DATA --------
            employees.append({
                "id": str(len(employees) + 1),
                "employee_name": employee_name,
                "department": department,
                "position": position,
                "hire_date": hire_date,
                "email": email,
                "mobile_number": mobile,
                "permanent_address": address,
                "nationality": nationality,
                "employee_type": employee_type,
                "isactive": isactive
            })

            save_employees()

            # -------- REDIRECT TO EMPLOYEES PAGE --------
            self.send_response(303)
            self.send_header('Location', '/employees')
            self.end_headers()

# ------------------ RUN SERVER ------------------

def run():
    load_employees()
    server = http.server.HTTPServer(('', PORT), EmployeeHandler)
    print(f"Server running at http://localhost:{PORT}")
    server.serve_forever()

run()
