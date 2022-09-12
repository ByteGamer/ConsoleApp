#Copyright (c) 2022, BYTE
#All rights reserved.
#
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree. 

from time import sleep
from pyfiglet import Figlet
import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
from getpass import getpass
import traceback





console = Console()
font = Figlet(font='slant')
ByteAuth =  font.renderText("ByteAuth")

clear = lambda: os.system('cls')




try:
    def start():
        clear()
        print(ByteAuth)
        

    #-----------------------------------------------------------------------------------------------------------------------
    #login system


    def projectData():
        try:
            start()

            console.print('\nWelcome to ByteAuth', style='bold blue')
            console.print('\n1. Login')
            console.print('\n2. Register')

            choice = input('\nEnter your choice: ')
            if choice == '1':
                start()
                console.print('\nLogin',style='bold blue')
                name = input('\nUsername: ')
                password = getpass('\nPassword: ')
                try: 
                    loginRequest = requests.post('https://api.byteauth.xyz/Login', data={'Member_Name':name, 'Member_Password':password, 'Platform':'console'})
                    loginResponse = json.loads(loginRequest.text)
                except:
                    console.print("Error Connecting to Server",style="bold red")
                    sleep(1)
                    start()
                    projectData()
                try:
                    console.print(loginResponse["error"], style="bold red")
                    sleep(1)
                    projectData()
                except:
                    #print(loginResponse["projects"])
                    projectsScreen(name,password)
                    sleep(1)    
            elif choice == '2':
                start()
                console.print('\nRegister',style='bold blue')
                name = input('\nUsername: ')
                email = input('\nEmail: ')
                password = input('\nPassword: ')
                try:
                    registerRequest = requests.post('https://api.byteauth.xyz/register',data={"Member_Name":name,"Member_Email":email,"Member_Password":password})
                    loginresponse = json.loads(registerRequest.text)
                
                    try:
                        console.print(loginresponse["error"], style="bold red")
                        sleep(1)
                        projectData()
                    except:
                        start()
                        console.print('\n Your account has been created', style='bold green')
                        console.print('\n Your username is: ' + name)
                        console.print('\n Your password is: ' + password)
                        console.print('\n YOUR RECOVERY TOKEN IS: ' + loginresponse["Member_RecoveryToken"] + ' KEEP THIS TOKEN SAFE!\n', style='bold red')
                        input(' Press enter to continue')
                        projectData()
                except Exception:
                    console.print("Error Connecting to Server",style="bold red")
                    sleep(1)
                    start()
                    projectData()
            else:
                console.print('Invalid Choice', style='bold red')
                sleep(1)
                projectData()
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            projectData()

    #-----------------------------------------------------------------------------------------------------------------------
    #projects screen
    def projectsScreen(name,password):
        try:
            start()
            console.print("Welcome Back",end=" ",style="bold" ),console.print(name,style="bold blue")
            console.print("\nProjects:",style="bold")

            projectsRequest = requests.get('https://api.byteauth.xyz/Projects', data={'Member_Name':name, 'Member_Password':password,'type':'multiple'})
            projectsResponse = json.loads(projectsRequest.text)

            for i in range(len(projectsResponse['projects'])):
                print(i, end=" "),console.print(projectsResponse['projects'][i],style="italic blue")
            console.print("\nSelect a project to view its details:",style="bold")   
            console.print('\nType "New" to create a new project\n',style="dim") 


            project = input()
            
            if project == 'New':
                newProject(name,password)  
            else:
                intproject = int(project)
            try:
                if intproject in range(len(projectsResponse)):
                    projectRequest = requests.get('https://api.byteauth.xyz/Projects', data={'Project_Name':projectsResponse['projects'][intproject],'Member_Name':name, 'Member_Password':password,'type':'single'})
                    ProjectRespons = json.loads(projectRequest.text)
                    ProjectDataScreen(ProjectRespons,name,password)
                    sleep(1)
                else:
                    console.print("Invalid Input",style="bold red")
                    sleep(1)
                    projectsScreen(name,password)
            except IndexError:
                console.print("Invalid Input",style="bold red")
                sleep(1)
                projectsScreen(name,password)
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            projectsScreen(name,password)

    def newProject(name,password):
        try:
            start()
            console.print("Create New Project",style="bold")
            projectName = input("\nProject Name: ")
            projectDescription = input("\nProject Description: ")
            projectRequest = requests.post('https://api.byteauth.xyz/Projects', data={'Project_Name':projectName,'Project_Description':projectDescription,'Member_Name':name, 'Member_Password':password})
            projectResponse = json.loads(projectRequest.text)
            try:
                console.print(projectResponse["error"], style="bold red")
                sleep(1)
                projectsScreen(name,password)
            except:
                console.print("Project Created",style="bold green")
                sleep(1)
                projectsScreen(name,password)
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            newProject(name,password)


    #-----------------------------------------------------------------------------------------------------------------------
    #project data screen
    def ProjectDataScreen(projectdata , name, password):
        try:
            start()

            #loop true users
            table = Table(show_header=True, header_style="bold blue", box=box.SIMPLE_HEAD)
            table.add_column("Nr.", style="bold blue")
            table.add_column("User Id")
            table.add_column("User Key")
            table.add_column("IP Address")
            table.add_column("HWID")
            table.add_column("user Note")
            table.add_column("key note")
            table.add_column("user Claimed")

            console.print("Project:",end=" "),console.print(projectdata["Project_Name"],style="bold blue")
            console.print("\nProject Description:",end=" "),console.print(projectdata["Project_Description"],style="bold blue")
            console.print("\nID",end=" "),console.print(projectdata["_id"],style="bold blue")
            console.print("\nProject Users:",end="\n")


            for i in range(len(projectdata["Project_Users"])):  
                try:
                    ip = projectdata["Project_Users"][i]["User_Identifiers"]["IP"]
                except:
                    ip = "N/A"

                try:
                    hwid = projectdata["Project_Users"][i]["User_Identifiers"]["HWID"]
                except:
                    hwid = "N/A"

                table.add_row(
                    str(i),projectdata["Project_Users"][i]["User_Id"],projectdata["Project_Users"][i]["User_Key"],ip,hwid,projectdata["Project_Users"][i]["User_Note"],projectdata["Project_Users"][i]["Key_Note"],str(projectdata["Project_Users"][i]["User_Claimed"])
                )

            console.print("\n",table)

            console.print("\nSelect a user to view and edit its details:",style="bold")
            console.print('\nType "New" to create a new keys\n',style="dim") 

            select = input()
            
            if select == 'New':
                newKey(name,password,projectdata)
            else:
                intselect = int(select)
            try:
                if intselect in range(len(projectdata["Project_Users"])):
                    detailScreen(projectdata , name, password , projectdata["Project_Users"][intselect])
                else:
                    console.print("Invalid Input",style="bold red")
                    sleep(1)
                    ProjectDataScreen(projectdata , name, password)
            except IndexError:
                console.print("Invalid Input",style="bold red")
                sleep(1)
                ProjectDataScreen(projectdata , name, password)
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            ProjectDataScreen(projectdata , name, password)

    def newKey(name,password,projectdata):
        try:
            start()
            console.print("Create New Keys",style="bold")
            keyAmmount = int(input("\nAmount of keys: "))
            Key_Note = input("\nKey Note: ")

            projectRequest = requests.post('https://api.byteauth.xyz/Keys', data={'Project_Name':projectdata["Project_Name"],"Member_Name":name, "Member_Password":password,"amount":keyAmmount,"Key_Note":Key_Note})    
            projectResponse = json.loads(projectRequest.text)
            try:
                console.print(projectResponse["error"], style="bold red")
                sleep(1)
                projectsScreen(name,password)
            except:
                console.print("Keys Created",style="bold green")
                sleep(1)
                projectsScreen(name,password)
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            newKey(name,password,projectdata)


    #-----------------------------------------------------------------------------------------------------------------------
    #detail screen
    def detailScreen(projectdata, data, name, password , detaildata):
        try:
            start()
            console.print("Project:",end=" "),console.print(projectdata["Project_Name"],style="bold blue")
            console.print("\nProject Description:",end=" "),console.print(projectdata["Project_Description"],style="bold blue")
            console.print("\nID",end=" "),console.print(projectdata["_id"],style="bold blue")
            console.print("\nUser Id:",end=" "),console.print(detaildata["User_Id"],style="bold blue")
    

            sleep(1)    
        except ValueError:
            console.print("Invalid Input",style="bold red")
            sleep(1)
            detailScreen(projectdata, data , name, password , detaildata)

    projectData()

except KeyboardInterrupt:
    print("\nExiting...")
    sleep(1)
    clear()
    exit()