from pathlib import Path
import json
import random
import string

class Bank:
    database = "database.json"
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = database.loads(fs.read())

        else:
            print("sorry we are facing some issues") 

    except Exception as err:
        print("an error ocurred" , err)

    @classmethod
    def __update(cls):
        with open(cls.database , "w") as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters , k = 5) 
        digits = random.choices(string.digits , k = 4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)


    def createaccount(self):
        d = {
            "name" : input("enter the name:"),
            "email" : input("enter your email:"),
            "phoneno" : input("entre the phone number"),
            "pin" : int(input("enter the pin:")),
            "account no." : Bank.__accountno(),
            "balance" : 1000
        }
    
        print("please note your accout number" , d["account no."])
        
        if len(str(d["pin"])) != 4:
            print("please review your pin it shoul be of 4 digits")

        elif len(str(d["phoneno"])) != 10:
            print("please review your phone number it should be of 10 digits")

        else:
            Bank.data.append(d)
            Bank.__update()

    def deposite_money(self):
        accno = input("enter the account number:")
        pin = int(input("enter the pin number:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        print(user_data)

        if not user_data:
            print("user not found...please check")
        else:
            amount = int(input("enter the amount to be deposited"))

            if amount <= 0:
                print("invalid amount")
            elif amount >= 10000:
                print("amount greater than 10000 cannot be deposited")
            else:
                user_data[0]["balance"] += amount
                Bank.__update()
                print("amount deposited")

    def withdrwa_money(self):
        accno = input("enter your account number:")
        pin = input("enter the pin number:")
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        print(user_data)

        if not user_data:
            print("user not found....please check again")

        else:
            amount = int(input("enter the amount you want to withdraw"))

            if amount <= 0:
                print("invalid amount")
            elif amount > 10000:
                print("amount greater than 10000 cannot be withdrawn")
            else:
                if user_data[0]["balance"] < amount:
                    print("insufficent balance")
                else:
                    user_data[0]["balance"] -= amount
                    Bank.__update()
                    print("amount debited")

    def details(self):
        accno = input("enter your account number:")
        pin = input("enter your pin number:")
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin] 
        print(user_data) 

        if not user_data:
            print("user not found...please check")
        else:
            for i in user_data:
                print(i,user_data[0][i])


    def update_details(self):
        accno = input("enter the account number:")
        pin = input("enter the pin number:")
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]

        if not user_data:
            print("user not found....please check")
        else:
            print("you accnot change the account number")
            print("now update your details and skip if you dont want to update your details")
            #name,email,phone number,pin

            new_data = {
                "name":input("enter your new name"),
                "email":input("enter your new email"),
                "phoneno":input("enter your new phone number"),
                "pin":input("enter your new pin"),
            }
            new_data["account no."]

user = Bank()
print("press 1 for creating an account")
print("press 2 for depositing the money")
print("press 3 to withdraw the money")
print("press 4 for the details")
print("press 5 for updating the detaila")
print("press 6 for deleting the account")


check = int(input("enter the number of option you want to perform"))

if check == 1:
    user.createaccount()

if check == 2:
    user.deposite_money()
    