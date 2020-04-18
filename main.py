
#------------------------------------------------------------------

# Things to implement
# - 1st appearance -  Login , create new accnt
# if login :
#   withdraw, add money ,accnt summary, change details or password, transfer money delete,
# else
#     give details.

#  find a way to store the objects

#-------------------------------------------------------------------

import bcrypt      # help to develop costfactor thus useful to protect from rainbow attacks
import pickle
import os
import sys

# start
CRED = '\033[32m'
CEND = '\033[0m'
detdict = {'users': [], 'objects': {}}


class Account:

    def __init__(self, **kwargs):
        self.fname = kwargs['fname']
        self.age = kwargs['age']
        self.place = kwargs['place']
        self.job = kwargs['job']
        self.usrname = kwargs['usrname']
        self.password = kwargs['password']
        self.balance = kwargs['balance']

        self.allDict = kwargs

    def getVal(self, value):
        return self.allDict[value]

    def setVal(self, value, nature, mode):
        # print(str(value) + nature + mode)
        if(nature == 'balance' and mode == 'add'):
            self.balance = self.balance + value
        if(nature == 'balance' and mode == 'sub'):
            if(value > self.balance):
                amt = int(
                    input("Current balance insufficient, please give appropriate amount"))

                self.setVal(amt, nature, mode)
            else:

                self.balance = self.balance - value

        self.allDict[nature] = self.balance

    @classmethod
    def retClass(cls, **kwargs):
        for x, y in kwargs.items():
            print(' {}  -->  {}'.format(x, y))
        return Account(**kwargs)

    def hashfunc(self):
        # print(self.password)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.password, salt)
        self.hashed = hashed

    def checkpass(self, newpass):
        return bcrypt.checkpw(newpass, self.hashed)


def getAlldetails(lst):
        # global detdict
    fname = raw_input("Enter your full name :")
    age = input("Enter age :")
    place = raw_input("Enter place :")
    job = raw_input("Enter job :")
    # usrname = raw_input("Enter desired username :")
    while True:
        usrname = raw_input("Enter desired username :")
        if(usrname in lst):
            print('Username exists, plesse enter new one :')
        else:
            break

    password = raw_input("Enter pin :")
    balance = 500
    details = {}
    details.update({'fname': fname, 'age': age, 'place': place,
                    'job': job, 'usrname': usrname, 'password': password, 'balance': balance})
    return details


def updatedict(user, **objects):
    global detdict
    if(user != None):
        detdict.get('users').append(user)
       # print(detdict)
    if(len(objects) > 0):

        detdict.get('objects').update(objects)

        # print(detdict.get('objects').get('amina').getVal('balance'))


def savedict(savedict):
    with open('object_data.pkl', 'w') as file:

        pickle.dump(savedict, file, pickle.HIGHEST_PROTOCOL)


def loadOption(val):
    global detdict

    if(val == 2):
       # print(detdict)
        print("---- Create Account ----")
        det = getAlldetails(detdict.get('users'))
       # a = Account(**det)
        accnt = Account.retClass(**det)
        accnt.hashfunc()
        udict = {accnt.getVal('usrname'): accnt}
        updatedict(accnt.getVal('usrname'), **udict)
        print(CRED + 'Details enterd successfully' + CEND)
        print('Your current balance is Rs. 500')
        print('Logging out....')

    else:
        # global detdict

        print("---- Login with your credentials ----")

        val = False
        while not val:

            usr = raw_input('Enter username :')
            password = raw_input('Enter password : ')
            val = verifyUsrnamepass(usr, password, **detdict)
            if(not val):
                print("Wrong inputs : Enter valid credentials")

        print("Login succes:")
        print("Welcome : " + CRED + usr + CEND)
        showdet(usr)


def showdet(usr):

    print(CRED + "1. Show summary" + CEND + "  " +
          CRED + "2. Add money" + CEND + "  " + CRED + "3. Retrieve Money" +
          CEND + "  " + CRED + "4.Transfer money" +
          CEND + "  " + CRED + "5. Update pin" + CEND
          + "  " + CRED + "6. Delete your account" + CEND)
    opt = input("Enter your option :")
    usroptions(opt, usr)


def usroptions(opt, usr):

    global detdict
    currobj = detdict.get('objects').get(usr)
    # print("det are", detdict.get('objects').get(usr))
    if(opt == 1):
        print("------- " + CRED + "Summary of your account" + CEND + " --------")
        print("Full Name " + "-----> " + currobj.getVal('fname'))

        print("Age " + "-----> " + str(currobj.getVal('age')))
        print("Current balance " + "-----> " +
              "{}".format(currobj.getVal('balance')))
        showdet(usr)
    if(opt == 2):
        # global detdict
        print("Your current balance is  " + CRED +
              "{}".format(currobj.getVal('balance')) + CEND)
        mon = int(raw_input("Enter the amount to add"))
        currobj.setVal(mon, 'balance', 'add')
        print("Your updated balance is  " + CRED +
              "{}".format(currobj.getVal('balance')) + CEND)
        up = {usr: currobj}
        updatedict(None, **up)
        showdet(usr)

    if(opt == 3):

        amt = int(input('Enter the amount to be withdrawed : '))
        currobj.setVal(amt, 'balance', 'sub')
        print(CRED + 'Successfull' + CEND)
        print("Your updated balance is  " + CRED +
              "{}".format(currobj.getVal('balance')) + CEND)
        showdet(usr)
    if(opt == 4):

        tr = int(input("Enter the amount ot be tranfered : "))
        while True:

            name = raw_input("Enter the user you needs to transfer money : ")
            if(name not in detdict.get('users')):
                print("Sorry user doesnt exists")
                # name = raw_input("Enter the correct user")
            else:
                detdict.get('objects').get(name).balance = detdict.get(
                    'objects').get(name).balance + tr
                detdict.get('objects').get(name).allDict['balance'] = detdict.get(
                    'objects').get(name).balance
                detdict.get('objects').get(usr).balance = detdict.get(
                    'objects').get(usr).balance - tr
                detdict.get('objects').get(usr).allDict['balance'] = detdict.get(
                    'objects').get(usr).balance
                print("Suucessfully tranfered")
                break

        # print(detdict.get('objects').get(name).balance)

        up = {name: detdict.get('objects').get(
            name), usr: detdict.get('objects').get(usr)}
        updatedict(None, **up)
        showdet(usr)

    if(opt == 5):
        while True:
            pin = raw_input("Enter your current pin : ")
            if(not detdict.get('objects').get(usr).checkpass(pin)):
                print("Wrong pin")
            else:
                new_pin = raw_input("Enter your new pin : ")
                detdict.get('objects').get(usr).password = new_pin
                detdict.get('objects').get(usr).hashfunc()
                print("Changed pin successfully, please login again")
                break
    if(opt == 6):
        choice = raw_input("Do you want remove the account?,  yes | no :")
        if(choice == 'yes'):
            detdict.get('objects').pop(usr)

            detdict.get('users').remove(usr)
        else:
            showdet(usr)


def verifyUsrnamepass(usr, password, **kwargs):

    if (usr in kwargs.get('users')):

        if(kwargs.get('objects').get(usr).checkpass(password)):
            return True

        # print(sys.exc_info())

    return False


def initailLoad():

    try:
        global detdict
        if(os.path.exists('object_data.pkl')):
            with open('object_data.pkl', 'r') as file:

                detdict = pickle.load(file)
        print(CRED + "1: Login using your Account" + CEND + "         " +
              CRED + "2: Create Account" + CEND)

        val = input("Enter your option " + CRED + "1" +
                    CEND + " or " + CRED + "2" + CEND + " :")

        det = loadOption(val)
    except:
        # if(exception.__class__.__name__ == 'No')
        print('something went wrong')
        sys.exit()
    finally:

        if('val' in locals()):
            savedict(detdict)

        sys.exit()


if(__name__ == '__main__'):

    initailLoad()
