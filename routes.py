# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session  # Ensure this import is correct
from models import Employee

employee_router = APIRouter(prefix="/employees", tags=["Employees"])


@employee_router.post("/", response_model=Employee)
async def create_employee(employee: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@employee_router.get("/", response_model=list[Employee])
async def get_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()
    return employees


@employee_router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="No Employee found with this id")
    return employee


@employee_router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    updated_employee: Employee,
    session: Session = Depends(get_session),
):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="No Employee found with this id")

    # Update employee fields
    employee.name = updated_employee.name
    employee.age = updated_employee.age
    employee.department = updated_employee.department
    employee.salary = updated_employee.salary

    session.commit()
    session.refresh(employee)
    return employee


@employee_router.delete("/{employee_id}")
async def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="No Employee found with this id")

    session.delete(employee)
    session.commit()
    return {"message": f"Employee {employee_id} deleted successfully"}
