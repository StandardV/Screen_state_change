import win32con
import win32gui
import time
import win32api
import os
from multiprocessing import Process

auto_turn= False
path1 = os.path.join(os.path.dirname(__file__), "listrack.txt")
with open(path1, 'w') as fp:
    fp.write('True')
p_change = 'True'

def screen_off():
    """turn off screen"""
    #with open(path1, 'w') as fp:
    #    fp.write('False')
    return win32gui.SendMessage(win32con.HWND_BROADCAST,
                        win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)

def screen_on():
    """turn on screen from movement"""
    #with open(path1, 'w') as fp:
    #    fp.write('True')
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1)
    #return win32gui.SendMessage(win32con.HWND_BROADCAST,
    #                    win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
    

def perform_change(val): 
    """check if duplicate, if not perform screen off or on"""
    if p_change != val:
        print(val , p_change)
        if 'False'  in val:
            screen_off()
        elif 'True' in val:
            screen_on()
        else:
            print("houston we have a problem")

def auto_turnoff():
    """count down time to turn off screen"""
    global auto_turn
    while True:
        time.sleep(2)
        nexttime = time.time() + 600
        if nexttime < time.time():
            auto_turn = True
    #after a period of time, auto invoke screen of functionality

def actively_monitor(): #actively check if state changed
    """monitor file if it's true or false"""
    global auto_turn
    while True:
        time.sleep(2) #open file, (read), then wait and do it again
        #open...read
        # if state the same as it is from before, skip, else, trigger function
        if auto_turn == True:
            with open(path1, 'w') as fp:
                fp.write('False')
            auto_turn = False
        else:
            with open(path1, 'r') as fp:
                line = fp.readline()
            
            perform_change(line)
        
        


if __name__ == '__main__':
    p1 = Process(target=actively_monitor)
    p2 = Process(target=auto_turnoff)
    p1.start()
    p2.start()