import tkinter as tk
import threading
import cargame
import client
from multiprocessing import Process
#from Car-Racing-Game-single import cargame_single
#import Car-Racing-Game-single
import sys
 
# adding Folder_2 to the system path
sys.path.insert(0, '/d/semester 8/distributed systems/Car Racing Game using Pygame_01.1/Car-Racing-Game-single')





import sys
sys.path.append("Car-Racing-Game-single")
# adding Folder_2 to the system path
# sys.path.insert(0, '/d/semester 8/distributed systems/Car Racing Game using Pygame_01.1/Car-Racing-Game-single')
import cargame_single

def multiplayer():
    #button.pack_forget()
    cargame.execute_game()
    pass
def single():
    #button.pack_forget()
    cargame_single.execute_single()
    #pass
def startchat():
    client.chatfunc()
def run_multiplayer():
    # create a new thread and run my_function on it
    thread1 = threading.Thread(target=multiplayer)
    thread1.start()
    
    thread2 = threading.Thread(target=startchat)
    thread2.start()
    thread2.join()
    thread1.join()
def run_single():
    # create a new thread and run my_function on it

    thread = threading.Thread(target=single)
    thread.start()
    thread.join()
root = tk.Tk()
root.geometry("800x600")

# create a button that calls run_multiplayer when clicked
button1 = tk.Button(root, text="start multiplayer game window", command=run_multiplayer)
button2 = tk.Button(root, text="start single game", command=run_single)
button1.pack()
button2.pack()

# start the Tkinter event loop
root.mainloop()