from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "haii"}

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    return {"employee_id": employee_id, "name": "Sample Employee"}

@app.get("/employee/{employee_id}/details")
def get_employee_details(employee_id: int):
    return {
        "employee_id": employee_id,
        "name": "Sample Employee",
        "department": "IT",
        "salary": 25000
    }

@app.get("/employees")
def get_employees(department: str = None):
    return {"filtered_department": department, "message": "Showing employees"}

@app.get("/employees/search")
def search_employees(name: str = None, min_salary: float = None):
    return {"search_name": name, "min_salary_filter": min_salary}