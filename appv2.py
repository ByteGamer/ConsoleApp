#Copyright (c) 2022, BYTE
#All rights reserved.
#
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree. 


from multiprocessing.connection import wait
from time import sleep
from urllib import response
from pyfiglet import Figlet
import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
from getpass import getpass
import traceback

# imports for cli framework






font = Figlet(font='slant')
ByteAuth =  font.renderText("ByteAuth")
clear = lambda: os.system('cls')





#Create a class to store user data

class User:

    type = "client"

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def setUser(self, username):
        self.username = username
    
    
    def setPass(self, password):
        self.password = password

user = User('','')

#loginRequest = requests.post('https://api.byteauth.xyz/Login', data={'Member_Name':name, 'Member_Password':password, 'Platform':'console'})
#loginResponse = json.loads(loginRequest.text)


def postLogin(name,password):
    try: 
        loginRequest = requests.post('https://api.byteauth.xyz/Login', data={'Member_Name':name, 'Member_Password':password, 'Platform':'console'})
        loginResponse = json.loads(loginRequest.text)
    except:
        return('Error connecting to the server')
    try:
        return(loginResponse["error"])
    except:
        return('success')  

def getProjects(name,password):
    try:
        projectsRequest = requests.get('https://api.byteauth.xyz/Projects', data={'Member_Name':name, 'Member_Password':password,'type':'multiple'})
        projectsResponse = json.loads(projectsRequest.text)
        return(projectsResponse)
    except:
        return('Error connecting to the server')
    


def kbInterrupt():
    clear()
    print('\n\nExiting ....')
    sleep(3)
    

def init():
    try:
        clear()
        print(ByteAuth)
        print('\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
        print('Chose your option: \n')
        option = int(input('login [0]\nRegister [1]\n\nInput:'))
        match option:
            case 0:
                login()
            case _:
                print('Not a correct input')
                sleep(3)
                init()

    except KeyboardInterrupt:
        kbInterrupt()
    except ValueError:
        print('Not a correct input')
        sleep(3)
        init()



def login():
    try:
        clear()
        print(ByteAuth)
        print('\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
        print('Enter your information:\n')
        username = input('Username: ')
        password = getpass('Password: ')
        response = postLogin(username,password)
        print(response)
        if response == 'success':
            user.setUser(username)
            user.setPass(password)
            sleep(1)
            mainPage()
        sleep(1)

    except KeyboardInterrupt:
        kbInterrupt()


def mainPage():
    try:
        clear()
        print(ByteAuth)
        print('\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
        projects = getProjects(user.username,user.password)
        print(projects)
        for i in range(len(projects['projects'])):
            print(i, end=" "),print(projects['projects'][i])
        sleep(2)
    except KeyboardInterrupt:
        kbInterrupt()    







#initialization of programm

init()