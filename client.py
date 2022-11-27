# if message == "NICK":
#                     self.sock.send(self.nickname.encode('utf-8'))


import socket 
import threading
import tkinter 
import tkinter.scrolledtext
from tkinter import *
import sqlite3 

HOST = "127.0.0.2"
# HOST = "172.16.177.213"
PORT = 9000

# We create a client which has a socket , The socket connects to Host and port 
# The client takes nickname fro the dialog box 
# We say gui is still not done and the connection is running 
# The we run two threads on eto build gui and other to deal with the server

class Client:
    
    # self.gui_done, self.running ,  self.win ,  self.sock
    
    def __init__(self , host , port):
        
        # msg = tkinter.Tk()
        # msg.withdraw()
        # self.nickname = simpledialog.askstring("Nickname" , "Please Choose a nickname", parent = msg)
        
        # The entire SignUp Login GUI 
        self.nickname  = " "
        #create an object to create a window
        window = Tk()
        
        #Actions on Pressing Login Button
        def login():
            def login_database():
                conn = sqlite3.connect("1.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM test WHERE email=? AND password=?",(e1.get(),e2.get()))
                row=cur.fetchall()
                conn.close()
                print(row)
                if row!=[]:
                    user_name=row[0][1]
                    l3.config(text="user name found with name: "+user_name)
                    # This is the place from where the user will get logged in and will see the signup window further
                    self.nickname  = user_name
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((host, port))
                    self.afterLogInActivity()
                    
                else:
                    l3.config(text="user not found")

            window.destroy()  #closes the previous window
            login_window = Tk() #creates a new window for loging in
            login_window.title("LogIn")  #set title to the window
            login_window.geometry("800x500")  #set dimensions to the window
            #add 2 Labels to the window
            l1 = Label(login_window,text="email: ",font="times 20")
            l1.place(x = 340,y = 200) 
            l2 = Label(login_window,text="Password: ",font="times 20")
            l2.place(x = 340,y = 260) 
            l3 = Label(login_window,font="times 20") 
            l3.place(x = 340,y = 320)

            #creating 2 adjacent text entries
            email_text = StringVar() #stores string
            e1 = Entry(login_window,textvariable=email_text)
            e1.place(x = 500,y = 200)

            password_text = StringVar()
            e2 = Entry(login_window,textvariable=password_text,show='*')
            e2.place(x = 500,y = 260)

            #create 1 button to login
            b = Button(login_window,text="login",width=20,command=login_database)
            b.grid(row=4,column=1)

            login_window.mainloop()

        #Actions on Pressing Signup button
        def signup():
            #Database action on pressing signup button
            def signup_database():
                conn = sqlite3.connect("1.db") #create an object to call sqlite3 module & connect to a database 1.db
                #once you have a connection, you can create a cursor object and call its execute() method to perform SQL commands
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,name text,email text,password text)")
                cur.execute("INSERT INTO test Values(Null,?,?,?)",(e1.get(),e2.get(),e3.get()))
                
                #execute message after account successfully created
                l4 = Label(signup_window,text="account created",font="times 15")
                l4.place(x = 340,y = 380)
                
                conn.commit()  #save the changes 
                conn.close() #close the connection

            window.destroy()  #closes the previous window
            signup_window = Tk() #creates a new window for signup process
            signup_window.geometry("800x500") #dimensions for new window
            signup_window.title("Sign Up") #title for the window
            #create 3 Labels
            l1 = Label(signup_window,text="User Name: ",font="times 20")
            l1.place(x = 340,y = 200)

            l2 = Label(signup_window,text="User email: ",font="times 20")
            l2.place(x = 340,y = 260)

            l3 = Label(signup_window,text="Password: ",font="times 20")
            l3.place(x = 340,y = 320)
            #create 3 adjacent text entries
            name_text = StringVar() #declaring string variable for storing name and password
            e1 = Entry(signup_window,textvariable=name_text)
            e1.grid(row=1,column=2)

            email_text = StringVar()
            e2 = Entry(signup_window,textvariable=email_text)
            e2.grid(row=2,column=2)

            password_text = StringVar()
            e3 = Entry(signup_window,textvariable=password_text,show='*')
            e3.grid(row=3,column=2)

            #create 1 button to signup
            b1 = Button(signup_window,text="signup",width=20,command=signup_database)
            b1.grid(row=4,column=2)

            signup_window.mainloop()
                    
        #main window code and driver code
        #give dimensions to the window
        window.geometry("800x500")
        #add title to the window
        window.title("Login and Signup system")
        #adding the label "Register Here"
        label1 = Label(window, text="Register Here!",font="times 20").place(x = 340,y = 200) 
        
        #adding two buttons - login and signup
        button1 = Button(window,text="Login",width=20,command=login).place(x = 250,y = 260)

        button2 = Button(window,text="Signup",width=20,command=signup).place(x = 435,y = 260)
        
        #calling mainloop method which is used when your application is ready to run and it tells the code to keep displaying   
        
        # # The below two threads will run simultaneously
        # self.gui_done = False
        # self.running  = True 

        # gui_thread = threading.Thread(target = self.gui_loop )
        # receive_thread = threading.Thread(target = self.receive )
        
        # gui_thread.start()
        # receive_thread.start()
        
        # gui_thread.join()
        # receive_thread.join()
        
        window.mainloop()
     
    def afterLogInActivity(self):
        
        # The below two threads will run simultaneously
        self.gui_done = False
        self.running  = True 

        self.sock.send(self.nickname.encode('utf-8'))
        
        gui_thread = threading.Thread(target = self.gui_loop )
        receive_thread = threading.Thread(target = self.receive )
        
        gui_thread.start()
        receive_thread.start()
        
        gui_thread.join()
        receive_thread.join()
        
    def gui_loop(self):
        # The entire gui of the chat window is written here 
        self.win = tkinter.Tk()  # defined a tkinter window for self here 
        self.win.configure(bg ="lightgray")
        
        
        self.chat_label = tkinter.Label(self.win, text = "Chat: " ,bg = "lightgray")
        self.chat_label.config(font= ("Arial", 12))
        self.chat_label.pack(padx = 20, pady = 5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win )
        self.text_area.pack(padx = 20, pady = 5)
        self.text_area.configure(state ='disabled')
        
        self.msg_label = tkinter.Label(self.win, text = "Message: " ,bg = "lightgray")
        self.msg_label.config(font= ("Arial", 12))
        self.msg_label.pack(padx = 20, pady = 5)
        
        self.input_area = tkinter.Text(self.win , height = 3)  
        self.input_area.pack(padx = 20, pady = 5)
            
        self.send_button = tkinter.Button(self.win, text ="Send" , command = self.write)
        self.send_button.config(font= ("Arial", 12))
        self.send_button.pack(padx = 20, pady = 5)
        
        self.gui_done = True
        
        # what happens if we close the window 
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()  
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)   
    
    def write(self):
        message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
    
    def receive(self):
            while self.running:
                try:
                    message = self.sock.recv(1024).decode('utf-8')
                    # if message == "Spaul":
                    #     self.sock.send(self.nickname.encode('utf-8'))
                    # else:
                    if self.gui_done:
                        self.text_area.config(state = "normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state ='disabled')
                except ConnectionAbortedError:
                    break
                except:
                    print("Error")
                    self.sock.close()
                    break


client = Client(HOST , PORT)

