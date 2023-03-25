from pydantic import BaseModel
#Class which describes input
class input(BaseModel):
    emp_title: str
    emp_length: float
    homeownership: str
    annual_income: float
    debt_to_income: float
    delinq_2y: float
    earliest_credit_line: float
    total_credit_lines: float
    open_credit_lines: float
    total_debit_limit: float
    loan_purpose: str
    loan_amount: float
    balance: float