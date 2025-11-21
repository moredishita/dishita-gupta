import streamlit as st
from pathlib import Path
import json
import random
import string

# ---------------- BANK CLASS -------------------

class Bank:
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("Database file missing!")
    except Exception as err:
        print("Error:", err)

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        acc = alpha + digits
        random.shuffle(acc)
        return "".join(acc)

    def createaccount(self, name, email, phoneno, pin):
        d = {
            "name": name,
            "email": email,
            "phoneno": phoneno,
            "pin": pin,
            "account no.": Bank.__accountno(),
            "balance": 0
        }

        Bank.data.append(d)
        Bank.__update()
        return d["account no."]

    def find_user(self, accno, pin):
        return [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]

    def deposit(self, accno, pin, amount):
        user = self.find_user(accno, pin)
        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"

        user[0]["balance"] += amount
        Bank.__update()
        return "Amount deposited successfully"

    def withdraw(self, accno, pin, amount):
        user = self.find_user(accno, pin)
        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"

        if user[0]["balance"] < amount:
            return "Insufficient balance"

        user[0]["balance"] -= amount
        Bank.__update()
        return "Amount withdrawn successfully"

    def details(self, accno, pin):
        user = self.find_user(accno, pin)
        if not user:
            return None
        return user[0]

    def update(self, accno, pin, name, email, phoneno, new_pin):
        user = self.find_user(accno, pin)
        if not user:
            return "User not found"

        u = user[0]

        if name:
            u["name"] = name
        if email:
            u["email"] = email
        if phoneno:
            u["phoneno"] = phoneno
        if new_pin:
            u["pin"] = new_pin

        Bank.__update()
        return "Details updated successfully"

    def delete(self, accno, pin):
        user = self.find_user(accno, pin)

        if not user:
            return "User not found"

        Bank.data.remove(user[0])
        Bank.__update()
        return "Account deleted successfully"


# ---------------- STREAMLIT UI -------------------

bank = Bank()

st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Account", "Deposit Money", "Withdraw Money",
     "View Details", "Update Details", "Delete Account"]
)

# CREATE ACCOUNT
if menu == "Create Account":
    st.header("Create New Bank Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    pin = st.text_input("4-digit PIN")

    if st.button("Create"):
        if len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("Phone number must be 10 digits")
        else:
            acc = bank.createaccount(name, email, phone, int(pin))
            st.success(f"Account created successfully! Your Account Number is: **{acc}**")


# DEPOSIT MONEY
if menu == "Deposit Money":
    st.header("Deposit Money")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        result = bank.deposit(accno, int(pin), amount)
        st.success(result)


# WITHDRAW MONEY
if menu == "Withdraw Money":
    st.header("Withdraw Money")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        result = bank.withdraw(accno, int(pin), amount)
        st.success(result)


# VIEW DETAILS
if menu == "View Details":
    st.header("View Account Details")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Show Details"):
        info = bank.details(accno, int(pin))
        if info:
            st.json(info)
        else:
            st.error("User not found")


# UPDATE DETAILS
if menu == "Update Details":
    st.header("Update Account Details")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN")

    st.write("Leave fields empty if you don't want to change.")

    name = st.text_input("New Name")
    email = st.text_input("New Email")
    phone = st.text_input("New Phone")
    new_pin = st.text_input("New PIN")

    if st.button("Update"):
        result = bank.update(accno, int(pin), name, email, phone, new_pin)
        st.success(result)


# DELETE ACCOUNT
if menu == "Delete Account":
    st.header("Delete Account")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Delete"):
        result = bank.delete(accno, int(pin))
        st.success(result)
