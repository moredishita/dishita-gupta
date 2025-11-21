from pathlib import Path
import json
import random
import string
class Bank:
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("sorry we are facing some issues")

    except Exception as err:
        print("an error occured" , err) 
    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters,k = 5)
        digits = random.choices(string.digits,k = 4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)
            

    def createaccount(self):
        d = {
            "name" : input("enter the name:"),
            "email" : input("enter the email"),
            "phoneno" : input("enter your phone number"),
            "pin" : int(input("please tell your pin(4 digits)")),
            "account no." : Bank.__accountno(),
            "balance" : 0
        }
        print("please note down your acc number" , d["account no."])
        if len(str(d['pin'])) != 4:
            print("please review your pin")

        elif len(str(d["phoneno"])) != 10:
            print("please review your phone number")

        else:
            Bank.data.append(d)
            Bank.__update()

    def deposite_money(self):
        accno = input("enter the acc number:")
        pin = int(input("enter your pin:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        print(user_data)
        
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter the amount to be deposited:"))
            if amount <= 0:
                print("invalid amount")
            elif amount > 10000:
                print("greater then 10000")
            else:
                user_data[0]["balance"] += amount    
                Bank.__update()
                print("amount credited")    



    def withdraw_money(self):
        accno = input("enter the acc number:")
        pin = int(input("enter your pin:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        print(user_data)
        
        if not user_data:
            print("user not found")
        else:
            amount = int(input("enter the amount to be withdrwal:"))
            if amount <= 0:
                print("invalid amount")
            elif amount > 10000:
                print("greater then 10000")
            else:
                if user_data[0]["balance"] < amount:
                    print("insufficient balance")
                else:
                    user_data[0]['balance'] -= amount
                    Bank.__update()
                    print("amount debited")    

    def details(self):
        accno = input("enter the acc number:")
        pin = int(input("enter your pin:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        
        if not user_data:
            print("user not found")
        else:
            for i in user_data[0]:
                print(i,user_data[0][i])

    def update_details(self):
        accno = input("enter the acc number:")
        pin = int(input("enter your pin:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        if not user_data:
            print("user not found")
        else:
            print("you cannot change account number")
            print("now update your details and skip if you don't want to update ")
            # name,email,phone,pin 
            new_data = {
                'name': input("enter your new name:"),
                'email':input("enter your new email"),
                'phoneno':input("enter your new phone number"),
                'pin':input("enter your new pin"),
            }
            new_data["account no."] = user_data[0]["account no."]
            new_data["balance"] = user_data[0]["balance"]

            #Handle the skipped values:

            for i in new_data:
                if new_data[i] == "":
                    new_data[i] = user_data[0][i]
            print(new_data)

            #We have to update new data to database:

            for i in user_data[0]:
                if user_data[0][i] == new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i] = int(new_data[i])

                    else:
                        user_data[0][i] = new_data[i]
            print(user_data)  
            Bank.__update()  
            print("Details updated!")


    def delete_account(self):
        accno = input("enter the acc number:")
        pin = int(input("enter your pin:"))
        user_data = [i for i in Bank.data if i["account no."] == accno and i["pin"] == pin]
        
        if not user_data:
            print("user not found")
        else:
            for i in Bank.data:
                if i["account no."] == accno and i["pin"] == pin:
                    Bank.data.remove(i)
            Bank.__update()
            print("data deleted")


print(Bank.data)


user = Bank()
print("press 1 for creating an account")
print("press 2 to deposit money")
print("press 3 to withdraw money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting the account")

check = int(input("enter your choice:"))

if check == 1:
    user.createaccount()

if check == 2:
    user.deposite_money()

if check == 3:
    user.withdraw_money()    

if check == 4:
    user.details()

if check == 5:
    user.update_details()

if check == 6:
    user.delete_account()

