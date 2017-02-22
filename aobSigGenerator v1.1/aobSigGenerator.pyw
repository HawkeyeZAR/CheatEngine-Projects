"""
PyAOB - AOB Signature Generator for Cheat Engine Scripts

Created by Jack Ackermann
"""


from tkinter import Tk, Frame, Button, PhotoImage, INSERT, Scrollbar,  Label, Text, FALSE, messagebox, Menu, re
import webbrowser



class myAOBSigGen(Frame):
    
    def centreWindow(self):
        w = 690
        h = 585
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs,  background="sky blue")
        self.root = parent
        self.root.title(' '*20 +'PyAOB - AOB Signature Generator for Cheat Engine Scripts -  by Jack Ackermann')
        self.centreWindow()
        self.grid(column=0, row=0, sticky='nsew',  padx=15,  pady=0)
        
        
        # create a popup menu, for Copy and Paste functions for aobTextInput        
        self.menu = Menu(self, tearoff=0, relief='sunken')
        self.menu.add_command(label="Copy...", command=self.copy)
        self.menu.add_separator()
        self.menu.add_command(label="Paste...", command=self.paste)
        
        # create a popup menu, for Copy and Paste functions for aobTextOutput        
        self.menuOut = Menu(self, tearoff=0, relief='sunken')
        self.menuOut.add_command(label="Copy...", command=self.copyA)
        self.menuOut.add_separator()
        self.menuOut.add_command(label="Paste...", command=self.pasteA)

                            
        # Create and add your Buttons
        calc_button = Button(self, text='Generate', background="palegreen1", command=self.getAobText)
        calc_button.grid(column=0, row=6,  sticky='nw', pady=10, padx=15)# sticky='sw', 
        exit_button = Button(self, text='Exit', background="IndianRed1", command=self.onExit, width=7) 
        exit_button.grid(column=0, row=6, sticky='ne', pady=10) #
          
        # create Text Box and ScrollBar for AOB Signature.
        self.aobTextInput = Text(self, borderwidth=0, relief='sunken')
        self.aobTextInput.config(font=("Arial",  11),  undo=True, wrap='none', height=8, width=80)
        self.aobTextInput.grid(row=1, column=0, sticky="new") #, padx=2, pady=2
        self.script_scrollb1 = Scrollbar(self, command=self.aobTextInput.yview)
        self.script_scrollb1.grid(row=1, column=1, sticky='nse')
        self.aobTextInput['yscrollcommand'] = self.script_scrollb1.set
        self.script_scrollba = Scrollbar(self, orient='horizontal',  command=self.aobTextInput.xview)
        self.script_scrollba.grid(row=2, column=0,  sticky='esw')
        self.aobTextInput['xscrollcommand'] = self.script_scrollba.set
        # attach copy/paste popup menu to textbox
        self.aobTextInput.bind("<Button-3>", self.popup)


        # create Text Box and ScrollBar for your AOB Signature pattern.
        self.aobTextOutput = Text(self, borderwidth=1, relief='sunken')
        self.aobTextOutput.config(font=("Arial",  11), undo=True, wrap='none', height=8, width=80)
        self.aobTextOutput.grid(row=4, column=0, sticky="new", columnspan=2)
        #self.script_scrollb4 = Scrollbar(self, command=self.aobTextOutput.yview)
        #self.script_scrollb4.grid(row=4, column=1, sticky='nse')
        #self.aobTextOutput['yscrollcommand'] = self.script_scrollb4.set
        self.script_scrollbd = Scrollbar(self, orient='horizontal',  command=self.aobTextOutput.xview)
        self.script_scrollbd.grid(row=5, column=0,  sticky='esw', columnspan=2)
        self.aobTextOutput['xscrollcommand'] = self.script_scrollbd.set
        # attach copy/paste popup menu to textbox
        self.aobTextOutput.bind("<Button-3>", self.popupOut)
        
        # Define and setup your labels.
        Label(self, text='Paste Your AOB Signatures Here', foreground="purple1", background="sky blue",  font=('Arial', 11, 'bold')).grid(column=0, row=0) # , sticky='sw', columnspan=1,
        Label(self, text='Your New AOB Signature', foreground="purple1", background="sky blue", font=('Arial', 11, 'bold',  'italic')).grid(column=0, row=3) # , sticky='nw'
        
        # Add Image to Promote Cheat The Game
        photo = PhotoImage(file="appImage.gif")
        appImage = Label(self, image=photo,  background="sky blue")
        appImage.photo = photo
        appImage.grid(column=0, row=7, sticky='n', rowspan=3, columnspan=1)
        
        # Add link to Cheat The Game Facebook Page
        def callback(event):
            webbrowser.open_new(r"https://www.facebook.com/groups/CheatTheGame/")
        fbLink = Label(self, text="Go to:  Cheat The Game", cursor="hand2", 
                                    foreground="yellow",  background="black",  font=('Arial', 12, 'bold', 'underline'))
        fbLink.grid(column=0, row=9, padx=190)
        fbLink.bind("<Button-1>", callback)  
        Label(self, text="Shout out to all the great peeps over at CTG", foreground="firebrick1",  
                      background="black",  font=('Arial', 11, 'bold')).grid(column=0, row=7, sticky='ne', pady =2, padx=145)
                      
    
    
    # Create popup menu for aobTextInput copy and paste functions       #####
    def popup(self, event):                                             #####
        self.menu.post(event.x_root, event.y_root)                      #####
    # Create popup menu for aobTextOutput copy and paste functions      #####
    def popupOut(self, event):                                          #####
        self.menuOut.post(event.x_root, event.y_root)                   #####        
    # Copy  to clip board                                               ##### This section here handles the copy and paste functions
    def copy(self, event=None):                                         ##### Since you have to create your own copy and paste menu
        self.clipboard_clear()                                          ##### in python. I had to create a popup for each text box
        text = self.aobTextInput.get("sel.first", "sel.last")           ##### to allow the copying and pasting of the correct data.
        self.clipboard_append(text)                                     #####
    # copy text from clip board                                         #####        
    def paste(self):                                                    #####
        self.aobTextInput.insert(INSERT, self.clipboard_get())          #####
    # Copy to clip board                                                #####        
    def copyA(self, event=None):                                        #####
        self.clipboard_clear()                                          ##### 
        text = self.aobTextOutput.get("sel.first", "sel.last")          #####
        self.clipboard_append(text)                                     #####
    # copy text from clip board                                         #####
    def pasteA(self):                                                   #####
        self.aobTextOutput.insert(INSERT, self.clipboard_get())    
        
        
        
           
    # Get the AOB string signatures entered in the self.aobTextInput textbox, clean the text and pass it to
    # the self.aobTextInput function.
    def getAobText(self):
        # Make sure result aobTextOutput is empty before your function begins
        self.aobTextOutput.delete(1.0,  'end-1c')
        
        # Get the AOB input text from the text box, then split the text so we can compare line by line.
        txtData = self.aobTextInput.get(1.0, 'end-1c').strip().upper()
        txtLine = txtData.split('\n')
        lines = txtLine      
        self.replaceWithQuestionMarks(lines)
        
        
        
    # Loop through the data to find all the aob's that don't match, if found, replace with ?            
    def replaceWithQuestionMarks(self, lines):
        newLine = [] # this will contain the characters/question marks
       
        # loop over each index in a line:
        for i in range(len(lines[0])):
            charactersInAllLines = []
            # Check that each line has the same text length to prevent the script from crashing.
            try:
                # loop over each line, populating charactersInAllLines with the i'th character in the line
                for line in lines:
                    charactersInAllLines.append(line[i])
         
                # convert to a set to get rid of duplicate characters, check if there's only 1 unique character
                if len(set(charactersInAllLines)) == 1:
                    newLine.append(charactersInAllLines[0]) # add the character to the new line
                else:
                    newLine.append('?') # append a question mark
                    
            except IndexError:
                messagebox.showinfo("Invalid AOB Signature Length", "One or more entered AOB signature strings are shorter than your first line." + 
                                    "\nPlease Check that all the lines you entered are of the same length.")
                self.aobTextOutput.delete(1.0,  'end-1c')
                break              
        self.aobTextOutput.insert(INSERT, ''.join(newLine) + '\n')
        self.aobTextOutput.insert(INSERT, '\n' + '________________________________________________________________________\n')
        self.aobTextOutput.insert(INSERT, ' #######################   Double ? Signature Format   ####################### \n')
        self.aobTextOutput.insert(INSERT, '************************************************************************************************\n')
        aobSigType2 = re.sub(r'(\w[?])|([?]\w)', '??',''.join(newLine), re.I | re.DOTALL)
        self.aobTextOutput.insert(INSERT, aobSigType2)     
        return ''.join(newLine) # convert the list of strings into a single string
                



    # Function to exit the program used by the exit button
    def onExit(self):
        self.root.destroy()   




def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.configure(background="sky blue")
    myAOBSigGen(root)
    root.mainloop()

if __name__ == '__main__':
    main()
