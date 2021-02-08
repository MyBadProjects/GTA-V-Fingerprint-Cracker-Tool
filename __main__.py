import os
import pyautogui as pyauto
import wx
import keyboard as kb
import time
from tkinter import Tk, Button, Label, Frame, END

"""
Not Hotbar Style
style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.FRAME_SHAPED  )
"""

class _Interface():
    def __init__(self,window):
        frame = Frame(master=window)
        window.winfo_toplevel().title("Fingerprint Tool")
        button = Button(master=frame,text='Start',command=loop,width=75,height=10)
        button.pack()
        label = Label(master=frame,text='To exit loop mode press "Esc"\nTo scan and highlight press "`"\nMade by MyBadProjects / backspace',width=75,height=6)
        label.pack()
        frame.pack()
        window.mainloop()
        
    def enable():
        enabled = True
        button2["state"] = "disabled"
        button3["state"] = "enabled"

    def disable():
        enabled = False
        button2["state"] = "enabled"
        button3["state"] = "disabled"

class _Frame(wx.Frame):
        def __init__(self,posX,posY,sizeX,sizeY,colour,opacity,close_mode):
            print('Frame started') # Log that the frame has started
            style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | 
                wx.NO_BORDER | wx.FRAME_SHAPED  )
            wx.Frame.__init__(self, None, title='Highlight', style = style)
            self.SetTransparent( 220 ) # Set the transparancy
            self.SetSize(wx.Size(sizeX, sizeY)) # Size the frame to the position mentioned
            self.Move(wx.Point(posX, posY)) # Move the frame to the position mentioned

            # Close frame depending on close_mode
            if close_mode==None:
                self.Bind(wx.EVT_LEFT_DOWN, self.Exit)
            elif close_mode.lower()=="keydown":
                self.Bind(wx.EVT_KEY_DOWN, self.Exit)
            elif close_mode.lower()=="leftclick":
                self.Bind(wx.EVT_LEFT_DOWN, self.Exit)
            elif close_mode.lower()=="rightclick":
                self.Bind(wx.EVT_RIGHT_DOWN, self.Exit)
            elif close_mode.lower()=="anymouse":
                self.Bind(wx.EVT_MOSE_EVENTS, self.Exit)
            elif close_mode.lower()=="any":
                self.Bind(wx.EVT_KEY_DOWN, self.Exit)
                self.Bind(wx.EVT_MOSE_EVENTS, self.Exit)
            else:
                print("No close method.\nClicking on the box will make it disappear.")
                self.Bind(wx.EVT_LEFT_DOWN, self.Exit)

            # Set the frame colour to be the colour mentioned
            if colour!=None:
                try:
                    self.SetBackgroundColour(colour)
                except:
                    print('The colour was not valid.')
            
            self.Show() # This shows the frame

        def Exit(self, event=None):
            self.Close() # Close the frame
            print("Frame closed") # Log that the frame has been closed
 
class HighlightImage():
    def __init__ (self,image):
        image_detect = pyauto.locateOnScreen(image) # Locate the image
        if image_detect: # Check for if it detected the image
            print(image_detect) # This logs the output

            app = wx.App()
            frame = _Frame(
                image_detect.left, # This gets the X position
                image_detect.top, # This gets the Y position
                image_detect.width, # This gets the Width
                image_detect.height, # This gets the Height
                "blue",
                220,
                "leftclick"
            )
            app.MainLoop()

dir_path = os.path.dirname(os.path.realpath(__file__))

def run():
    for filename in os.listdir(dir_path): # This goes through all the files of the local directory
        if filename.startswith("print_"): # Prevent the script from highlighting all fingerprints
            print(filename) # Logs file name
            if filename.endswith(".png"): # This only lists the files which are a .png and checks if they match
                fingerprint = pyauto.locateOnScreen(os.path.join(dir_path, filename))
                if fingerprint:
                    print(fingerprint) # Logs pyautogui.locateOnScreen output
                    print(filename)

                    filenumber = filename[:-4][-1:]
                    print(filenumber) # Logs file number
                    
                    for partfilename in os.listdir(dir_path): # This goes through all the files of the local directory
                        if partfilename.startswith(filenumber): # Prevent the script from highlighting all fingerprints and it checks if the file contains the correct part
                            print(partfilename)
                            highlightcheck = pyauto.locateOnScreen(partfilename)
                            if highlightcheck:
                                Highlight = HighlightImage(partfilename)
                            else:
                                print("A fingerprint part could not be found!")





#HighlightImage = HighlightImage("test.png")

pressed = False
enabled = True

def loop():
    while True: # This loops so it can detect the keypress
        try: # This prevents any erros
            if kb.is_pressed('`'): # This detects the keypress
                if pressed == False:
                    if enabled == True:
                        print('Key pressed!')
                        run()
                        time.sleep(1)
                        pressed = True
            else:
                pressed = False
            if kb.is_pressed('Esc'):
                print('Stopping Loop')
                break
        except:
            loop() # This calls the loop
            break # This stops the loop
        
window = Tk()
interface = _Interface(window)
