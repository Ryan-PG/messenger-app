from os import stat
import socket
import threading
import tkinter
from tkinter import Message, font
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:

  def __init__(self, host, port):
    """ Initialization an instance """
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((host, port))

    msg = tkinter.Tk() # Main window
    msg.withdraw()

    self.nickname = simpledialog.askstring('Nickname', 'Please choose a nickname:', parent=msg)

    self.gui_done = False
    self.running = True # Default is True and means app is running

    gui_thread = threading.Thread(target= self.gui_loop)
    receive_thread = threading.Thread(target= self.receive)

    gui_thread.start()
    receive_thread.start()

  def gui_loop(self):
    """ GUI builder """

    # Main Window
    self.window = tkinter.Tk()
    self.window.wm_title('H.Ryan Chat App')
    self.window.configure(bg='lightgrey')

    # Chat Area Label
    self.chat_label = tkinter.Label(self.window, text='Chat: ', bg='lightgrey')
    self.chat_label.config(font=('Calibri', 12)) # config = configure
    self.chat_label.pack(padx=20, pady=5) # Adding some paddings

    # Chat Area
    self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
    self.text_area.pack(padx=20, pady=5)
    self.text_area.config(state='disabled') # config = configure # Can't change input text area content


    # Message Label
    self.message_label = tkinter.Label(self.window, text='Message: ', bg='blue')
    self.chat_label.config(font=('Calibri', 12))
    self.chat_label.pack(padx=20, pady=5)

    # Message Area
    self.input_area = tkinter.Text(self.window, height=3)
    self.input_area.pack(padx=20, pady=5)

    # Button
    self.send_button = tkinter.Button(self.window, text='Send', command=self.write)
    self.send_button.config(font=('Calibri', 12))
    self.send_button.pack(padx=20, pady=5)

    # Send signal to other functions that UI is up now
    self.gui_done = True

    # if window is closed
    self.window.protocol('WM_DELETE_WINDOW', self.stop)

    self.window.mainloop()
  
  def write(self):
    """ Get the text from message box and send it to the server and then clean the message area """

    message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}" # ('1.0', 'end') ==> get the whole text
    self.socket.send(message.encode('utf-8'))
    self.input_area.delete('1.0', 'end')



  def stop(self):
    """ Stop and Close the Client window """

    self.running = False
    self.window.destroy()
    self.socket.close()
    exit(0)




  def receive(self):
    """ Handle functions for receiving and showing messages """
    
    
    while self.running:
      try:
        message = self.socket.recv(1024).decode('utf-8') # 1024 Bytes

        if message == 'NIC':
          self.socket.send(self.nickname.encode('utf-8'))
        else:
          if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview('end') # Always scroll down to the end with getting messages
            self.text_area.config(stat='disabled')
      except ConnectionAbortedError:
        print('Oh shit... You have no connection :(')
        break
      except:
        print('ERROR')
        self.socket.close()
        break





client = Client(HOST, PORT)









