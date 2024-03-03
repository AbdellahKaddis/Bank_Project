
from asyncio.windows_events import NULL
from datetime import date
import time
import os
from enum import Enum
class enService(Enum):
    PeopleList=1
    FindPerson=2
    AddNewPerson=3
    UpdatePerson=4
    DeletePerson=5
    Transactions=6
    ManageUsers=7
    Logout=8
 

class enTransactionsService(Enum):
    Deposit=1
    Withdraw=2
    Transfer=3
    MainMenue=4
    
class enPermissions(Enum):
    All=-1
    PeopleList=1
    FindPerson=2
    AddNewPerson=4
    UpdatePerson=8
    DeletePerson=16
    Transactions=32
    AddNewUser=64
    UpdateUser=128
    DeleteUser=256 
    ManageUsers=512
    
class enManageUsersMenue(Enum):
    UsersList=1
    FindUser=2
    AddNewUser=3
    UpdateUser=4
    DeleteUser=5
    ChangePassword=6
    MainMenue=7
    
class clsValidation:
    def CheckIfTheNumberIsInt():
        try:
            val = int(input("\n                             -Enter the number of the service that you want to perform? "))
            return val
        except ValueError:
             print("\n                             -this service is not exist.") 
             return clsValidation.CheckIfTheNumberIsInt()
             
    def IsNumber(Message):
        try:
            val = int(input(Message))
            return val
        except ValueError:
             print("\nEnter a number!!.") 
             clsValidation.IsNumber()
             
    def IsNumberInRange(Number,MinNumber,MaxNumber,Service):
        
        while Number < MinNumber or Number > MaxNumber:
            print("\n                              -this service is not exist.")
            Number=int(input("\n                             -Enter the number of the service that you want to perform? "))
        return  Service(Number)
    
    def IsUserHasPermission(UserPermission,ScreenPermission:enPermissions):
     if UserPermission == enPermissions.All.value:
         return True
     
     if(ScreenPermission.value & UserPermission != ScreenPermission.value):
          return False
     else:
         return True

class Person:
    def __init__(self,AccountNumber,FirstName,LastName,Age,Gender,AccountBalance:int):
        self.AccountNumber=AccountNumber
        self.FirstName=FirstName
        self.LastName=LastName
        self.Age=Age
        self.Gender=Gender
        self.AccountBalance=AccountBalance
        
    def AddNewPerson():
        AccountNumber=input("Enter Account Number? ")
        FirstName=input("Enter FirstName? ")
        LastName=input("Enter LastName? ")
        Age=input("Enter Age? ")
        Gender=input("Enter your Gender? ")
        AccountBalance=clsValidation.IsNumber("\nEnter AccountBalance?")
        
        Person.SavePersonInformationToTextFile(Person(AccountNumber,FirstName,LastName,Age,Gender,AccountBalance))
    
    def UpdatePerson(self,AccountNumber,Gender,AccountBalance):
         FirstName=input("Enter FirstName? ")
         LastName=input("Enter LastName? ")
         Age=input("Enter Age? ")
         Person.UpdatePersonInformationInTextFile(Person(AccountNumber,FirstName,LastName,Age,Gender,AccountBalance))

    def Find(AccountNumber):
        AllPersons=Person.LoadPersonsDataToList()
        for person in AllPersons:
            if person.AccountNumber == AccountNumber:
                return person
            
        return NULL
    
    def Delete(self,AccountNumber):
        AllPersons=Person.LoadPersonsDataToList()
        file=open('PersonsData.txt','w')
        for person in AllPersons:
            if person.AccountNumber != AccountNumber:
                DataToSave=str(person.AccountNumber)+"#//#"+person.FirstName+"#//#"+person.LastName+"#//#"+ str(person.Age)+"#//#"+person.Gender+"#//#"+ str(person.AccountBalance)+"\n"
                file.write(DataToSave)
        file.close()                    
        
    def PrintPersonInformation(self):
        print("Person Information:")
        print("--------------------------------")
        print("Account Number :",self.AccountNumber)
        print("FirstName      :",self.FirstName)
        print("LastName       :",self.LastName)
        print("Age            :",self.Age)
        print("Gender         :",self.Gender)
        print("AccountBalance :",self.AccountBalance)
        print("--------------------------------")
        
    def SavePersonInformationToTextFile(self):
        DataToSave=str(self.AccountNumber)+"#//#"+self.FirstName+"#//#"+self.LastName+"#//#"+ str(self.Age)+"#//#"+self.Gender+"#//#"+ str(self.AccountBalance)+"\n"
        file=open('PersonsData.txt','a')
        file.write(DataToSave)
        file.close()
    
    def LoadPersonsDataToList():
        file=open('PersonsData.txt','r')
        lines=file.readlines()
        AllPersons=[]
       
        for line in lines:    
            Data=line.split("#//#")
            if Data[0] != "\n":
                person1=Person(Data[0],Data[1],Data[2],Data[3],Data[4],Data[5])
                AllPersons.append(person1)

        file.close()
        return AllPersons
        
    def UpdatePersonInformationInTextFile(self):
        
        AllPersons=Person.LoadPersonsDataToList()
       
        file=open('PersonsData.txt','w')
        
        for person in AllPersons:
            if person.AccountNumber != self.AccountNumber:
                DataToSave=str(person.AccountNumber)+"#//#"+person.FirstName+"#//#"+person.LastName+"#//#"+ str(person.Age)+"#//#"+person.Gender+"#//#"+ str(person.AccountBalance)+"\n"
                file.write(DataToSave)
            else:
                DataToSave=str(self.AccountNumber)+"#//#"+self.FirstName+"#//#"+self.LastName+"#//#"+ str(self.Age)+"#//#"+self.Gender+"#//#"+ str(self.AccountBalance)+"\n"
                file.write(DataToSave)
           
        file.close()
       
    def ShowPeopleList():
        AllPersons=Person.LoadPersonsDataToList()
        print("\n\n__________________________________________________________________________________________________________________")
        print("|  Account Number   |     FirstName     |     LastName     |   Age   |    Gender    |        AccountBalance       |")
        print("|-----------------------------------------------------------------------------------------------------------------|")
        for person in AllPersons:
            print("|"+str(person.AccountNumber).center(14)+"     |"+person.FirstName.center(19)+"|"+person.LastName.center(18)+"|"+ str(person.Age).center(9)+"|"+person.Gender.center(14)+"|"+ str(person.AccountBalance).replace("\n","").center(29)+"|")
        print("|_________________________________________________________________________________________________________________|")   
        
    def Deposit(self,AccountNumber,FirstName,LastName,Age,Gender,AccountBalance:int,Amount:int):
         AccountBalance=AccountBalance + Amount 
         Person.UpdatePersonInformationInTextFile(Person(AccountNumber,FirstName,LastName,Age,Gender,AccountBalance))
         
    def Withdraw(self,AccountNumber,FirstName,LastName,Age,Gender,AccountBalance:int,Amount:int):
         AccountBalance=AccountBalance - Amount 
         Person.UpdatePersonInformationInTextFile(Person(AccountNumber,FirstName,LastName,Age,Gender,AccountBalance))
    
 
class User:
    def __init__(self,UserName:str,Password:str,FirstName:str,LastName:str,Age:int,Gender:str,Permissions:int):
        self.UserName=UserName
        self.Password=Password
        self.FirstName=FirstName
        self.LastName=LastName
        self.Age=Age
        self.Gender=Gender
        self.Permissions=Permissions
    
    def SetPermissions():
        Permissions=0
        Answer=input("\nDo you want to give this person all permissions?y/n  ")
        if Answer.lower() == "y":
            Permissions=enPermissions.All.value
            return Permissions 
        else:
             Answer=input("\nDo you want to allow this user show People Lists?y/n  ")
             if Answer.lower() == "y":
                  Permissions+=enPermissions.PeopleList.value
                   
             Answer=input("\nDo you want to allow this user Find Persons?y/n  ")
             if Answer.lower() == "y":
                    Permissions+=enPermissions.FindPerson.value 
         
             Answer=input("\nDo you want to allow this user Add New Persons?y/n  ")
             if Answer.lower() == "y":
                      Permissions+=enPermissions.AddNewPerson.value
        
             Answer=input("\nDo you want to allow this user Update Persons?y/n  ")
             if Answer.lower() == "y":
                  Permissions+=enPermissions.UpdatePerson.value 
                
             Answer=input("\nDo you want to allow this user Delete Persons?y/n  ")
             if Answer.lower() == "y":
                 Permissions+=enPermissions.DeletePerson.value 
              
             Answer=input("\nDo you want to allow this user manage Transactions?y/n  ")
             if Answer.lower() == "y":
                     Permissions+=enPermissions.Transactions.value
       
             Answer=input("\nDo you want to allow this user Add New Users?y/n  ")
             if Answer.lower() == "y":
                 Permissions+=enPermissions.AddNewUser.value 
              
             Answer=input("\nDo you want to allow this user update Users?y/n  ")
             if Answer.lower() == "y":
                     Permissions+=enPermissions.UpdateUser.value
         
             Answer=input("\nDo you want to allow this user to delete users?y/n  ")
             if Answer.lower() == "y":
                  Permissions+=enPermissions.DeleteUser.value 
                  
             Answer=input("\nDo you want to allow this user to manage users?y/n  ")
             if Answer.lower() == "y":
                  Permissions+=enPermissions.ManageUsers.value      
             
             return Permissions   
        
    def AddNewUser():
        UserName=input("Enter UserName? ")
        Password=input("Enter Password? ")
        FirstName=input("Enter FirstName? ")
        LastName=input("Enter LastName? ")
        Age=input("Enter Age? ")
        Gender=input("Enter your Gender? ")
        Permissions=User.SetPermissions()
        
        User.SaveUserInformationToTextFile(User(UserName,Password,FirstName,LastName,Age,Gender,Permissions))
    
    def UpdateUser(self,UserName,Password,Gender): 
         FirstName=input("Enter FirstName? ")
         LastName=input("Enter LastName? ")
         Age=input("Enter Age? ")
         Permissions=User.SetPermissions()
         User.UpdateUserInformationInTextFile(User(UserName,Password,FirstName,LastName,Age,Gender,Permissions))

    def FindUserByUserNameAndPassword(UserName:str,Password:str):
        AllUsers=User.LoadUserDataToList()
        for user in AllUsers:
            if user.UserName == UserName and user.Password == Password:
                return user
            
        return NULL
    
    def FindUserByUserName(UserName:str):
        AllUsers=User.LoadUserDataToList()
        for user in AllUsers:
            if user.UserName == UserName:
                return user
            
        return NULL

    def DeleteUser(self,UserName):
        AllUsers=User.LoadUserDataToList()
        file=open('UserData.txt','w')
        for user in AllUsers:
            if user.UserName != UserName:
                DataToSave=user.UserName+"#//#"+user.Password+"#//#"+user.FirstName+"#//#"+user.LastName+"#//#"+ str(user.Age)+"#//#"+user.Gender+"#//#"+ str(user.Permissions)+"\n"
                file.write(DataToSave)
        file.close()           
        
    def PrintUserInformation(self):
        print("Person Information:")
        print("--------------------------------")
        print("UserName       :",self.UserName)
        print("Password       :",self.Password)
        print("FirstName      :",self.FirstName)
        print("LastName       :",self.LastName)
        print("Age            :",self.Age)
        print("Gender         :",self.Gender)
        print("Permissions    :",self.Permissions)
        print("--------------------------------")
        
    def SaveUserInformationToTextFile(self):
        DataToSave=self.UserName+"#//#"+self.Password+"#//#" +self.FirstName+"#//#"+self.LastName+"#//#"+ str(self.Age)+"#//#"+self.Gender+"#//#"+ str(self.Permissions)+"\n"
        file=open('UserData.txt','a')
        file.write(DataToSave)
        file.close()
    
    def LoadUserDataToList():
        file=open('UserData.txt','r')
        lines=file.readlines()
        AllUsers=[]
       
        for line in lines:    
            Data=line.split("#//#")
            if Data[0] != "\n":
                user1=User(Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6])
                AllUsers.append(user1)

        file.close()
        return AllUsers
        
    def UpdateUserInformationInTextFile(self):
        
        AllUsers=User.LoadUserDataToList()
       
        file=open('UserData.txt','w')
        
        for user in AllUsers:
            if user.UserName != self.UserName:
                DataToSave=user.UserName+"#//#"+user.Password+"#//#"+user.FirstName+"#//#"+user.LastName+"#//#"+ str(user.Age)+"#//#"+user.Gender+"#//#"+ str(user.Permissions)+"\n"
                file.write(DataToSave)
            else:
                DataToSave=self.UserName+"#//#"+self.Password +"#//#"+self.FirstName+"#//#"+self.LastName+"#//#"+ str(self.Age)+"#//#"+self.Gender+"#//#"+ str(self.Permissions)+"\n"
                file.write(DataToSave)
           
        file.close()
       
    def ChangePassword(self,UserName,FirstName,LastName,Age,Gender,Permissions):
        NewPassword=input("Enter New Password? ")
        User.UpdateUserInformationInTextFile(User(UserName,NewPassword,FirstName,LastName,Age,Gender,Permissions)) 
        
    def ShowUsersList():
        AllUsers=User.LoadUserDataToList()
        print("\n\n_______________________________________________________________________________________________")
        print("|   UserName   |   FirstName     |     LastName    |   Age   |    Gender    |   Permissions   |")
        print("|---------------------------------------------------------------------------------------------|")
        for user in AllUsers:
            print("|"+user.UserName.center(14)+"|"+user.FirstName.center(17)+"|"+user.LastName.center(17)+"|"+ str(user.Age).center(9)+"|"+user.Gender.center(14)+"|"+str(user.Permissions).replace("\n","").center(17)+"|")
        print("|_____________________________________________________________________________________________|")   
          
        
class TransactionsMenue:
        
    def ReadNumberOfService():
        Number=clsValidation.CheckIfTheNumberIsInt()
      
        return clsValidation.IsNumberInRange(Number,1,4,enTransactionsService)
    
    def GoBackToTransactionsMenueScreen():
        Continue=input("\nIf you want to go back to Transactions Menue Screen Enter Yes? ")
        if(Continue.lower() == "yes"):
            TransactionsMenue.ShowTransactionsMenueScreen()
            return
        else:
            return  
     
    def ShowDepositScreen():
        os.system("cls")
        Draw.Draw_Header("Deposit Screen")
        AccountNumber=input("\n\nEnter Account Number? ")
        person=Person.Find(AccountNumber)
        if person != NULL:
            person.PrintPersonInformation()
            Amount=clsValidation.IsNumber(f"\nyour Account Balance is {person.AccountBalance} How much do you want to Deposit? ")
            person.Deposit(AccountNumber,person.FirstName,person.LastName,person.Age,person.Gender,int(person.AccountBalance),Amount)
            print("operation done.")
        else:
            print("Person does not exist.")
        
    def ShowWithdrawScreen():
        os.system("cls")
        Draw.Draw_Header("Withdraw Screen")
        
        AccountNumber=input("\n\nEnter Account Number? ")
        person=Person.Find(AccountNumber)
        
        if person != NULL:
            person.PrintPersonInformation()
            
            Amount=clsValidation.IsNumber(f"\nyour Account Balance is {person.AccountBalance} How much do you want to withdraw? ")
            if Amount > int(person.AccountBalance):
                while True:
                    print(f"you can't withdraw more than your balance: {person.AccountBalance}")
                    Amount=clsValidation.IsNumber(f"\nyour balance is {person.AccountBalance} How much do you want to withdraw? ")
                    if Amount <= int(person.AccountBalance):
                        break
                
            
            person.Withdraw(AccountNumber,person.FirstName,person.LastName,person.Age,person.Gender,int(person.AccountBalance),Amount)
            print("operation done.")
        else:
            print("Person does not exist.")     

    def ShowTransferScreen():
         os.system("cls")
         Draw.Draw_Header("Transfer Screen")
         
         AccountNumber=input("\n\nTransfer Balance From Account.Enter AcountNumber? ")
         person1=Person.Find(AccountNumber)
         
         while person1 == NULL:
              print("Person does not exist.") 
              AccountNumber=input("\n\nTransfer Balance From Account.Enter AcountNumber? ")
              person1=Person.Find(AccountNumber)
              

         AccountNumber=input("\n\nTransfer Balance To Account.Enter AcountNumber? ")
         person2=Person.Find(AccountNumber)
         
         while person2 == NULL:
              print("Person does not exist.") 
              AccountNumber=input("\n\nTransfer Balance From Account.Enter AcountNumber? ")
              person2=Person.Find(AccountNumber)
              
         Amount=clsValidation.IsNumber(f"\nyour Account Balance is {person1.AccountBalance} How much do you want to Transfer? ")

         while Amount > int(person1.AccountBalance):
             print(f"you can't Transfer more than your balance: {person1.AccountBalance}")
             Amount=clsValidation.IsNumber(f"\nyour Account Balance is {person1.AccountBalance} How much do you want to Transfer? ")
                 
 
         person1.Withdraw(person1.AccountNumber,person1.FirstName,person1.LastName,person1.Age,person1.Gender,int(person1.AccountBalance),Amount)
         person2.Deposit(person2.AccountNumber,person2.FirstName,person2.LastName,person2.Age,person2.Gender,int(person2.AccountBalance),Amount)
         
         print(f"{Amount} Transfered From Account [{person1.AccountNumber}] To Account [{person2.AccountNumber}] Successfully.")
            
    def ShowTheChosenScreen(Service):
        if Service == enTransactionsService.Deposit:
            TransactionsMenue.ShowDepositScreen()
            TransactionsMenue.GoBackToTransactionsMenueScreen()
        elif Service == enTransactionsService.Withdraw:
            TransactionsMenue.ShowWithdrawScreen()
            TransactionsMenue.GoBackToTransactionsMenueScreen()
        elif Service == enTransactionsService.Transfer:
            TransactionsMenue.ShowTransferScreen()
            TransactionsMenue.GoBackToTransactionsMenueScreen()     
        elif Service == enTransactionsService.MainMenue:
            MainMenue.ShowMainMenueScreen()

    def ShowTransactionsMenueScreen():
        os.system("cls")
        Draw.Draw_Header("Transactions Menue Screen")
        print("\n                             1=>Deposit.")
        print("\n                             2=>Withdraw.")
        print("\n                             3=>Transfer.")
        print("\n                             4=>Main Menue.")
        print("\n________________________________________________________________________________________________________________________")
        Service=TransactionsMenue.ReadNumberOfService()
        TransactionsMenue.ShowTheChosenScreen(Service)


class Login():
    def ShowLoginScreen():
        global CurrentUser
        CurrentUser=NULL
        
        Draw.Draw_Header("Login Screen")
        
        UserName=input("\nEnter UserName? ")
        Password=input("\nEnter Password? ")
        CurrentUser=User.FindUserByUserNameAndPassword(UserName,Password)
        
        Trials=3
        
        while CurrentUser == NULL:
            Trials-=1
            
            if Trials == 0:
                print("The system is bolcked becuase you entered wrong password three times.")
                break
            
            print(f"Wrong Password you still have {Trials} Trials.")
            UserName=input("\nEnter UserName? ")
            Password=input("\nEnter Password? ")
            CurrentUser=User.FindUserByUserNameAndPassword(UserName,Password)

        if  CurrentUser != NULL:
            MainMenue.ShowMainMenueScreen()
            

class Draw:
    def Draw_Header(Title):
        os.system("color f0")
        Date=str(date.today())+"  "+str(time.strftime("%H:%M:%S", time.localtime()))
        if CurrentUser != NULL:
           print("------------------".rjust(120))
           print(("| UserName: "+CurrentUser.UserName+"|").rjust(120))
           print("------------------".rjust(120))
        print("\n ***Developed By ABDELLAH KADDIS***                "+str(Date))  
        print("________________________________________________________________________________________________________________________")
        print("                                         "+Title)
        print("________________________________________________________________________________________________________________________\n")
       

class ManageUsersMenue:
        def ReadNumberOfService():
             Number=clsValidation.CheckIfTheNumberIsInt()
        
             return clsValidation.IsNumberInRange(Number,1,7,enManageUsersMenue)

        def GoBackToManageUsersMenueScreen():
            Continue=input("\n\n\n\nIf you want to go back to Manage Users Menue Screen Enter Yes? ")
            if(Continue.lower() == "yes"):
                 ManageUsersMenue.ShowManageUsersMenueScreen()
                 return
            else:
                return 
            
        def ShowUsersListScreen():
            os.system("cls")
            Draw.Draw_Header("Users List Screen")
            User.ShowUsersList()
            
        def ShowFindUserScreen():
            os.system("cls")
            Draw.Draw_Header("Find User Screen")
            UserName=input("\n\nEnter UserName? ")
            user=User.FindUserByUserName(UserName)
            if user != NULL:
                  user.PrintUserInformation()
            else:
                 print("User Does Not Found.")
                 
        def ShowAddNewUserScreen():
             if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.AddNewUser):
                  os.system("cls")
                  Draw.Draw_Header("Denied Access Screen")
                  print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.AddNewUser.name)
             else:
                os.system("cls")
                Draw.Draw_Header("Add New User Screen")
                User.AddNewUser()
                print("User added successfully.")
            
        def ShowUpdateUserScreen():
             if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.UpdateUser):
                os.system("cls")
                Draw.Draw_Header("Denied Access Screen")
                print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.UpdateUser.name)
             else:
                 os.system("cls")
                 Draw.Draw_Header("Update User Screen")
                 UserName=input("\n\nEnter UserName? ")
                 user=User.FindUserByUserName(UserName)
                 if user != NULL:
                     user.PrintUserInformation()
                     user.UpdateUser(user.UserName,user.Password,user.Gender)
                     print("User updated successfully.")
                 else:
                     print("User does not exist.")
                
        def ShowDeleteUserScreen():
             if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.DeleteUser):
                 os.system("cls")
                 Draw.Draw_Header("Denied Access Screen")
                 print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.DeleteUser.name)
             else:
                os.system("cls")
                Draw.Draw_Header("Delete User Screen")
                UserName=input("\n\nEnter UserName? ")
                user=User.FindUserByUserName(UserName)
                if user != NULL:
                    user.PrintUserInformation()
                    Continue=input("\nAre you sure do you want to delete this person?y/n  ")
                    if(Continue.lower() == "y" ):
                        user.DeleteUser(UserName)
                        print("user deleted successfully.") 
                else:
                    print("User does not exist.")
                        
        def ShowChangePasswordScreen():
             os.system("cls") 
             Draw.Draw_Header("Change Password Screen")
             UserName=input("\n\nEnter UserName? ")
             user=User.FindUserByUserName(UserName)
             if user != NULL:
                 CurrentPassword=input("\n\nEnter your current Password? ")
                
                 while CurrentPassword != user.Password:
                      print("Wrong Password!!!")
                      CurrentPassword=input("\nEnter your current Password? ")
                      
                 user.ChangePassword(UserName,user.FirstName,user.LastName,user.Age,user.Gender,user.Permissions)
                 print("Password Changed successfully.")     
             else:
                 print("User does not exist.")
            
        def ShowTheChosenScreen(Service):
             if Service == enManageUsersMenue.UsersList:
                     ManageUsersMenue.ShowUsersListScreen()
                     ManageUsersMenue.GoBackToManageUsersMenueScreen()
             elif Service == enManageUsersMenue.FindUser:
                   ManageUsersMenue.ShowFindUserScreen()
                   ManageUsersMenue.GoBackToManageUsersMenueScreen()
             elif Service == enManageUsersMenue.AddNewUser:
                 ManageUsersMenue.ShowAddNewUserScreen()
                 ManageUsersMenue.GoBackToManageUsersMenueScreen()
             elif Service == enManageUsersMenue.UpdateUser:
                      ManageUsersMenue.ShowUpdateUserScreen()
                      ManageUsersMenue.GoBackToManageUsersMenueScreen()
             elif Service == enManageUsersMenue.DeleteUser:
                      ManageUsersMenue.ShowDeleteUserScreen()   
                      ManageUsersMenue.GoBackToManageUsersMenueScreen()
             elif Service == enManageUsersMenue.ChangePassword:
                      ManageUsersMenue.ShowChangePasswordScreen()   
                      ManageUsersMenue.GoBackToManageUsersMenueScreen()         
             elif Service == enManageUsersMenue.MainMenue:
                  MainMenue.ShowMainMenueScreen()
            
        def ShowManageUsersMenueScreen():
             os.system("cls")
             Draw.Draw_Header("Manage Users Menue Screen")
             print("\n                             1=>Users List.")
             print("\n                             2=>Find User.")
             print("\n                             3=>Add New User.")
             print("\n                             4=>Update User.")
             print("\n                             5=>Delete User.")
             print("\n                             6=>Change Password.")
             print("\n                             7=>Main Menue.")
             print("\n________________________________________________________________________________________________________________________")
             Service=ManageUsersMenue.ReadNumberOfService()
             ManageUsersMenue.ShowTheChosenScreen(Service)
               
             
class MainMenue:
    
    def ReadNumberOfService():
        Number=clsValidation.CheckIfTheNumberIsInt()
        
        return clsValidation.IsNumberInRange(Number,1,8,enService)

    def GoBackToMainMenue():
        Continue=input("\n\n\nIf you want to go back to Main Menue Enter Yes? ")
        if(Continue.lower() == "yes"):
            MainMenue.ShowMainMenueScreen()
            return
        else:
            return  
           
    def ShowPeopleListScreen():
        
        if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.PeopleList):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.PeopleList.name)
        else:
            os.system("cls")
            Draw.Draw_Header("People List Screen")
            Person.ShowPeopleList()
  
    def ShowFindPersonScreen():
        if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.FindPerson):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.FindPerson.name)
        else:
            os.system("cls")
            Draw.Draw_Header("Find Person Screen")
            AccountNumber=input("\n\nEnter Account Number? ")
            person=Person.Find(AccountNumber)
            if person != NULL:
                person.PrintPersonInformation()
            else:
                print("Person does not exist.")
            
    def ShowAddNewPersonScreen():
          if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.AddNewPerson):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.AddNewPerson.name)
          else:
               os.system("cls")
               Draw.Draw_Header("Add New Person Screen")
               Person.AddNewPerson()
               print("person added successfully.")         
     
    def ShowUpdatePersonScreen():
         if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.UpdatePerson):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.UpdatePerson.name)
         else:
              os.system("cls")
              Draw.Draw_Header("Update Person Screen")
              AccountNumber=input("\n\nEnter Account Number? ")
              person=Person.Find(AccountNumber)
              if person != NULL:
                  person.PrintPersonInformation()
                  person.UpdatePerson(AccountNumber,person.Gender,person.AccountBalance)
                  print("person updated successfully.")
              else:
                  print("Person does not exist.")
          
    def ShowDeletePersonScreen():
        if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.DeletePerson):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.DeletePerson.name)
        else:
            os.system("cls")
            Draw.Draw_Header("Delete Person Screen")
            AccountNumber=input("\n\nEnter Account Number? ")
            person=Person.Find(AccountNumber)
            if person != NULL:
                person.PrintPersonInformation()
                Continue=input("\nAre you sure do you want to delete this person?y/n  ")
                if(Continue == "y" or Continue == "Y"):
                    person.Delete(AccountNumber)
                    print("person deleted successfully.") 
            else:
                print("Person does not exist.")       
        
    def ShowTransactionsMenueScreen():
        if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.Transactions):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.Transactions.name)
        else:
            os.system("cls")
            TransactionsMenue.ShowTransactionsMenueScreen()
            
    def ShowManageUserMenueScreen():
        if not clsValidation.IsUserHasPermission(int(CurrentUser.Permissions),enPermissions.ManageUsers):
            os.system("cls")
            Draw.Draw_Header("Denied Access Screen")
            print("\n\n\n\n                       You Don't Have Permissions For: "+enPermissions.ManageUsers.name)
        else:
            ManageUsersMenue.ShowManageUsersMenueScreen() 
  
    def ShowTheChosenScreen(Service):
        if Service == enService.PeopleList:
            MainMenue.ShowPeopleListScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.FindPerson:
            MainMenue.ShowFindPersonScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.AddNewPerson:
            MainMenue.ShowAddNewPersonScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.UpdatePerson:
            MainMenue.ShowUpdatePersonScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.DeletePerson:
            MainMenue.ShowDeletePersonScreen()   
            MainMenue.GoBackToMainMenue()
        elif Service == enService.Transactions:
            MainMenue.ShowTransactionsMenueScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.ManageUsers:
            MainMenue.ShowManageUserMenueScreen()
            MainMenue.GoBackToMainMenue()
        elif Service == enService.Logout:
             os.system("cls")
             Login.ShowLoginScreen()
     
    def ShowMainMenueScreen():
        os.system("cls")
        Draw.Draw_Header("Main Menue Screen")
        print("\n                             1=>People List.")
        print("\n                             2=>Find Person.")
        print("\n                             3=>Add New Person.")
        print("\n                             4=>Update Person.")
        print("\n                             5=>Delete Person.")
        print("\n                             6=>Transactions.")
        print("\n                             7=>Manage Users Menue.")
        print("\n                             8=>Logout.")
        print("\n________________________________________________________________________________________________________________________")
        Service=MainMenue.ReadNumberOfService()
        MainMenue.ShowTheChosenScreen(Service)
        

Login.ShowLoginScreen()

#Login Information
#UseName:user1
#Password:0000
