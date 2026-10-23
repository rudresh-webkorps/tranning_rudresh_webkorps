import os
import csv
from datetime import datetime

File = "expense.csv"
Fields = ["date", "category", "amount"]
def add_expense():
    categoryy =input("add category ")
    ammount = Float(input("add amount:"))
    new_file = not os.path.exists(File)
    with open (File, "a",newline="") as f:
        w=CSV.DictWriter(f, fieldnames =Fields)
        if new_file:
            w.writeheader()
        w.writerow({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "category": categoryy, "amount": ammount})



def load_expenses():
    if not os.path.exists(File):
        return []
    with open(File, "r",newline="")as f:
        return list(CSV.DictReader(f))

def view_expense():
    for e in load_expenses():
        print(f"{e['date']} - {e['category']} - {e['amount']}")

def total_expense():
    print("Total expense :", sum(float(e['amount']) for e in load_expenses()))

while True:
    choice =int(input ("enter what you eant to do 1. add expense 2.View expense 3. total expense 4. exit"))
    if choice == 1 :
        try:
            add_expense()
        except ValueError:
            print("Enter a valid number")
    elif choice == 2 : view_expense()
    elif choice == 3 : total_expense()
    elif choice == 4 : break    
            

