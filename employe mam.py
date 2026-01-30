import http.server
import urllib.parse
import json
import os

PORT = 8000
DATA_FILE = 'employees.json'
employees = []


#n ------------------ DATA HANDLING ------------------

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
        if self.path == '/':

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management System</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px; width: 250px; }
        button { background: green; color: white; border: none; cursor: pointer; }
        pre { background: #f4f4f4; padding: 15px; }
    </style>
</head>
<body>

<h1>Employee Management System</h1>

<form method="POST" action="/employees">
    <input type="text" name="employee_name" placeholder="Employee Name" required><br>
    <input type="text" name="department" placeholder="Department (HR, Engineering)" required><br>
    <input type="text" name="position" placeholder="Position" required><br>
    <input type="date" name="hire_date" required><br>
    <input type="email" name="email" placeholder="Email" required><br>
    <input type="text" name="mobile_number" placeholder="Mobile Number" required><br>
    <input type="text" name="permanent_address" placeholder="Permanent Address" required><br>
    <input type="text" name="nationality" placeholder="Nationality" required><br>
    <input type="text" name="employee_type" placeholder="Full-time / Part-time / Contract" required><br>
    <input type="checkbox" name="isactive" value="1" > IsActive <br>
    <input type="text" name="empLastworkingdate" placeholder="Last Working Date"><br>
    <button type="submit">Add Employee</button>
</form>

<h2>Employees Data</h2>
<pre id="data"></pre>

<script>
fetch('/employees')
  .then(res => res.json())
  .then(data => {
    document.getElementById('data').innerText =
      JSON.stringify(data, null, 2);
  });
</script>

</body>
</html>
"""
            self.wfile.write(html.encode())

        elif self.path == '/employees':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(employees).encode())

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
            empLastworkingdate = data.get('empLastworkingdate', [''])[0]

            # ---------- VALIDATIONS ----------

            if department not in ['HR', 'Engineering', 'Sales', 'Marketing']:
                self.send_error(400, "Invalid department")
                return

            if '@' not in email or '.' not in email:
                self.send_error(400, "Invalid email address")
                return

            if not mobile.isdigit() or len(mobile) != 10:
                self.send_error(400, "Invalid mobile number")
                return

            if employee_type not in ['Full-time', 'Part-time', 'Contract']:
                self.send_error(400, "Invalid employee type")
                return

            if isactive not in ['1','']:   # Checkbox can be '1' or not present
                     
                self.send_error(400, "Invalid isactive value")
                return
            if empLastworkingdate:
                try:
                    from datetime import datetime
                    datetime.strptime(empLastworkingdate, '%Y-%m-%d')
                except ValueError:
                    self.send_error(400, "Invalid last working date format")
                    return

            # ---------- SAVE DATA ----------

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
                "isactive": isactive,
                "empLastworkingdate" : empLastworkingdate
            })

            save_employees()

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()




def run():
    load_employees()
    server = http.server.HTTPServer(('', PORT), EmployeeHandler)
    print(f"Server running at http://localhost:{PORT}")
    server.serve_forever()


run()
