from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "employees.json"

# ------------------ HELPERS ------------------

def load_employees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_employees(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ ROUTES ------------------

# ✅ GET ALL EMPLOYEES
@app.route("/api/employees", methods=["GET"])
def get_employees():
    employees = load_employees()
    return jsonify(employees), 200

# ✅ GET EMPLOYEE BY ID
@app.route("/api/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    employees = load_employees()
    for emp in employees:
        if int(emp["id"]) == emp_id:
            return jsonify(emp), 200
    return jsonify({"message": "Employee not found"}), 404

# ✅ ADD EMPLOYEE
@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.json

    required_fields = [
        "employee_name", "department", "position",
        "hire_date", "email", "mobile_number",
        "permanent_address", "nationality",
        "employee_type"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    if data["department"] not in ["HR", "Engineering", "Sales", "Marketing"]:
        return jsonify({"message": "Invalid department"}), 400

    if data["employee_type"] not in ["Full-time", "Part-time", "Contract"]:
        return jsonify({"message": "Invalid employee type"}), 400

    if not data["mobile_number"].isdigit() or len(data["mobile_number"]) != 10:
        return jsonify({"message": "Invalid mobile number"}), 400

    employees = load_employees()

    new_employee = {
        "id": len(employees) + 1,
        "employee_name": data["employee_name"],
        "department": data["department"],
        "position": data["position"],
        "hire_date": data["hire_date"],
        "email": data["email"],
        "mobile_number": data["mobile_number"],
        "permanent_address": data["permanent_address"],
        "nationality": data["nationality"],
        "employee_type": data["employee_type"],
        "isactive": data.get("isactive", True)
    }

    employees.append(new_employee)
    save_employees(employees)

    return jsonify(new_employee), 201

# ✅ UPDATE EMPLOYEE
@app.route("/api/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.json
    employees = load_employees()

    for emp in employees:
        if int(emp["id"]) == emp_id:
            emp.update(data)
            save_employees(employees)
            return jsonify(emp), 200

    return jsonify({"message": "Employee not found"}), 404

# ✅ DELETE EMPLOYEE
@app.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    employees = load_employees()
    updated = [emp for emp in employees if int(emp["id"]) != emp_id]

    if len(updated) == len(employees):
        return jsonify({"message": "Employee not found"}), 404

    save_employees(updated)
    return jsonify({"message": "Employee deleted successfully"}), 200

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
