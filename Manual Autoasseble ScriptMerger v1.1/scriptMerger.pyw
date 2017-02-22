"""
python Auto Assembler Script Merger for Cheat Engine scripts.

Created by Jack Ackermann
"""


from tkinter import Tk, ttk, Frame, Button, PhotoImage, INSERT, Scrollbar,\
Label, Text, END, FALSE, re, Menu, Toplevel
import webbrowser



class MyApp(Frame):
    
    def centre_window(self):
        w = 1362
        h = 575
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs,  background="black")
        self.root = parent
        self.root.title(' '*140 +'Auto Assemble Script Merger for Cheat Engine Scripts -  by Hawkeye ZAR')
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew',  padx=15,  pady=5)
        
        # create a popup menu, for Copy and Paste functions for aobTextInput        
        self.menu = Menu(self, tearoff=0, relief='sunken')
        self.menu.add_command(label="Cut...")
        self.menu.add_separator()
        self.menu.add_command(label="Copy...")
        self.menu.add_separator()
        self.menu.add_command(label="Paste...")
        
        # Create and add your Buttons
        calc_button = Button(self, text='Merge Scripts', command=self.insert_enable)
        calc_button.grid(column=0, row=9,   sticky='wn', padx=15, pady=24)
        # Resets the Program to start a new merge
        reset_button = Button(self, text='Reset', command=self.on_reset,  width=10) 
        reset_button.grid(column=0, row=9,  sticky='sw',  padx=15)
        # Terminates the Program
        exit_button = Button(self, text='Exit', command=self.onExit,  width=10) 
        exit_button.grid(column=0, row=10,  sticky='sw',  padx=15)
          
        self.script_txt1 = Text(self, borderwidth=1, relief='sunken')
        self.script_txt1.config(font=("consolas", 11), undo=True, wrap='none',
                                height=8, width=80) 
        self.script_txt1.grid(row=1, column=0, sticky="new")
        self.script_scrollb1 = Scrollbar(self, command=self.script_txt1.yview)
        self.script_scrollb1.grid(row=1, column=1, sticky='nse')
        self.script_txt1['yscrollcommand'] = self.script_scrollb1.set
        self.script_scrollba = Scrollbar(self, orient='horizontal',
                                         command=self.script_txt1.xview)
        self.script_scrollba.grid(row=2, column=0, sticky='esw')
        self.script_txt1['xscrollcommand'] = self.script_scrollba.set
        # attach copy/paste popup menu to textbox
        self.script_txt1.bind("<Button-3>", self.popup)

        self.script_txt2 = Text(self, borderwidth=1, relief='sunken')
        self.script_txt2.config(font=("consolas", 11), undo=True,
                                wrap='none', height=8, width=80)
        self.script_txt2.grid(row=4, column=0, sticky="new")
        self.script_scrollb2 = Scrollbar(self, command=self.script_txt2.yview)
        self.script_scrollb2.grid(row=4, column=1, sticky='nse')
        self.script_txt2['yscrollcommand'] = self.script_scrollb2.set
        self.script_scrollbb = Scrollbar(self, orient='horizontal',
                                         command=self.script_txt2.xview)
        self.script_scrollbb.grid(row=6, column=0, sticky='esw')
        self.script_txt2['xscrollcommand'] = self.script_scrollbb.set
        # attach copy/paste popup menu to textbox
        self.script_txt2.bind("<Button-3>", self.popup)
        
        self.script_txt3 = Text(self, borderwidth=1, relief='sunken')
        self.script_txt3.config(font=("consolas", 11), undo=True,
                                wrap='none', height=8, width=80)
        self.script_txt3.grid(row=1, column=2, sticky="new", padx=15)
        self.script_scrollb3 = Scrollbar(self, command=self.script_txt3.yview)
        self.script_scrollb3.grid(row=1, column=2, sticky='nse')
        self.script_txt3['yscrollcommand'] = self.script_scrollb3.set
        self.script_scrollbc = Scrollbar(self, orient='horizontal',
                                         command=self.script_txt3.xview)
        self.script_scrollbc.grid(row=2, column=2, sticky='esw')
        self.script_txt3['xscrollcommand'] = self.script_scrollbc.set
        # attach copy/paste popup menu to textbox
        self.script_txt3.bind("<Button-3>", self.popup)

        # This is were your new merged script will be stored.
        self.script_txt4 = Text(self, borderwidth=1, relief='sunken')
        self.script_txt4.config(font=("consolas", 11), undo=True,
                                wrap='none', height=8, width=80)
        # Code below disabled. Text is now being displayed in separate window
        # self.script_txt4.grid(row=9, column=0, sticky="new")
        # self.script_scrollb4 = Scrollbar(self, command=self.script_txt4.yview)
        # self.script_scrollb4.grid(row=9, column=1, sticky='nse')
        # self.script_txt4['yscrollcommand'] = self.script_scrollb4.set
        # self.script_scrollbd = Scrollbar(self, orient='horizontal',
        #                                 command=self.script_txt4.xview)
        # self.script_scrollbd.grid(row=10, column=0, sticky='esw')
        # self.script_txt4['xscrollcommand'] = self.script_scrollbd.set
        # self.script_txt4.bind("<Button-3>", self.popup)
        
        # create Text Box and ScrollBar for Fourth Script to be merged.
        self.script_txt5 = Text(self, borderwidth=1, relief='sunken')
        self.script_txt5.config(font=("consolas", 11), undo=True,
                                wrap='none', height=8, width=80)
        self.script_txt5.grid(row=4, column=2, sticky="new", padx=15)
        self.script_scrollb5 = Scrollbar(self, command=self.script_txt5.yview)
        self.script_scrollb5.grid(row=4, column=2, sticky='nse')
        self.script_txt5['yscrollcommand'] = self.script_scrollb5.set 
        self.script_scrollbe = Scrollbar(self, orient='horizontal',
                                         command=self.script_txt5.xview)
        self.script_scrollbe.grid(row=6, column=2, sticky='esw')
        self.script_txt5['xscrollcommand'] = self.script_scrollbe.set
        # attach copy/paste popup menu to textbox
        self.script_txt5.bind("<Button-3>", self.popup)  
     
        # Define and setup your labels.
        ttk.Separator(self, orient='horizontal').grid(column=0, row=7,
                                                      columnspan=3,  sticky='esw')
        Label(self, text='1.  First Auto Assemble Script', foreground="yellow",
              background="black",  font=('Arial', 10, 'bold')).grid(column=0, row=0)
        Label(self, text='2.  Second Auto Assemble Script', foreground="yellow",
              background="black", font=('Arial', 10, 'bold')).grid(column=0, row=3)
        Label(self, text='3.  Third Auto Assemble Script', foreground="yellow",
              background="black", font=('Arial', 10, 'bold')).grid(column=2, row=0)
        Label(self, text='4.  Fourth Auto Assemble Script', foreground="yellow",
              background="black", font=('Arial', 10, 'bold')).grid(column=2, row=3, padx=15)
        # Label(self, text='Your New Script', foreground="yellow", background="black",
        #       font=('Arial', 10, 'bold',  'italic')).grid(column=0, row=8)
        
        # Add Image to Promote Cheat The Game
        photo = PhotoImage(file="appImage.gif")
        appImage = Label(self, image=photo, background="black")
        appImage.photo = photo
        appImage.grid(column=0, row=8, sticky='nsw', rowspan=5, columnspan=3, padx=350)
        
        # Add link to Cheat The Game Facebook Page
        def callback(event):
            webbrowser.open_new(r"https://www.facebook.com/groups/CheatTheGame/")
        fbLink = Label(self, text="Go to:  Cheat The Game", cursor="hand2", 
                                    foreground="yellow", background="black",
                                    font=('Arial', 12, 'bold', 'underline'))
        fbLink.grid(column=0, row=9, sticky='sw', padx=550, 
                    pady=10, rowspan=5, columnspan=3)
        fbLink.bind("<Button-1>", callback)  
        Label(self, text="Shout out goes to all the great peeps over at CTG",
              foreground="white", background="black", font=('Arial', 10, 'bold')
              ).grid(column=0, row=8, sticky='nw', padx=460, pady=15,
                     columnspan=3, rowspan=2)
                    
    
    # Create popup menu for cut, copy and paste functions      
    def popup(self, event):                                             
        self.menu.post(event.x_root, event.y_root) 
        w = event.widget 
        self.menu.entryconfigure("Cut...",
                                 command=lambda: w.event_generate("<<Cut>>"))
        self.menu.entryconfigure("Copy...",
                                 command=lambda: w.event_generate("<<Copy>>"))
        self.menu.entryconfigure("Paste...",
                                 command=lambda: w.event_generate("<<Paste>>"))
 

    def insert_enable(self):
        """
        Setup function to copy Script to New location  
        Strip the Enable section of the Script only. 
        Check if any of the text boxes are empty, if empty, go to next text box 
        """
        self.script_txt4.delete(1.0,  END)      
        # nData = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]', 
        #self.script_txt1.get(1.0, END), re.I | re.DOTALL)
        scriptInputText1 = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]',
                                      self.script_txt1.get(1.0, 'end-1c'), re.I | re.DOTALL)
        scriptInputText2 = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]',
                                      self.script_txt2.get(1.0, 'end-1c'), re.I | re.DOTALL)
        scriptInputText3 = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]',
                                      self.script_txt3.get(1.0, 'end-1c'), re.I | re.DOTALL)
        scriptInputText5 = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]',
                                      self.script_txt5.get(1.0, 'end-1c'), re.I | re.DOTALL)
        inputText1 = '// \n' + '// Script 1 ENABLE section Starts Here' + '\n//' + ''.join(scriptInputText1)
        
        # Check if Text Box has Data in it
        if self.script_txt2.get(1.0, 'end-1c') != '':
            inputText2 = '// \n' + '// Script 2 ENABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputText2)
        else:
            inputText2 =''
            
        # Check if Text Box has Data in it    
        if self.script_txt3.get(1.0, 'end-1c') != '':
            inputText3 = '// \n' + '// Script 3 ENABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputText3)
        else:
            inputText3 =''
            
        # Check if Text Box has Data in it    
        if self.script_txt5.get(1.0, 'end-1c') != '':
            inputText5 = '// \n' + '// Script 4 ENABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputText5)
        else:
            inputText5 =''
            
        tempText = inputText1 + inputText2 + inputText3 + inputText5
        newText = re.sub(r'(>\n)\n\n(?!\n\n)|\n{3,}', '', tempText )
        self.script_txt4.insert(INSERT, '[ENABLE] \n' + ''.join(newText))        
        self.insert_disable() # Do Disable portion of the script merge
        self.results_window() # This display's the new script 
      
    def insert_disable(self):
        """
        Setup function to copy Script to New location  
        Strip the Disable section of the Script only
        This adds [DISEND] to the end of the copied scripts. 
        This is needed for the last part of the script merge.         
        Filter for [DISABLED] portion of script is added here, 
        check if any Text Box is empty, if empty skip to next text box
        """        
        self.script_txt1.insert(END, '\n[DISEND]')
        scriptInputT1 = re.findall(r'\[DISABLE\](.*?)\[DISEND\]', self.script_txt1.get(1.0, 'end-1c'), re.I | re.DOTALL)
        inputT1 = '// \n' + '// Script 1 DISABLE section Starts Here' + '\n//' + '\n'.join(scriptInputT1)        
        # Check if Text Box has Data in it
        if self.script_txt2.get(1.0, 'end-1c') != '':
            self.script_txt2.insert(END, '\n[DISEND]')
            scriptInputT2 = re.findall(r'\[DISABLE\](.*?)\[DISEND\]', self.script_txt2.get(1.0, 'end-1c'), re.I | re.DOTALL)
            inputT2 = '// \n' + '// Script 2 DISABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputT2)
        else:
            inputT2 =''        
        # Check if Text Box has Data in it
        if self.script_txt3.get(1.0, 'end-1c') != '':
            self.script_txt3.insert(END, '\n[DISEND]')
            scriptInputT3 = re.findall(r'\[DISABLE\](.*?)\[DISEND\]', self.script_txt3.get(1.0, 'end-1c'), re.I | re.DOTALL)
            inputT3 = '// \n' + '// Script 3 DISABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputT3)
        else:
            inputT3 =''        
        # Check if Text Box has Data in it
        if self.script_txt5.get(1.0, 'end-1c') != '':
            self.script_txt5.insert(END, '\n[DISEND]')
            scriptInputT5 = re.findall(r'\[DISABLE\](.*?)\[DISEND\]', self.script_txt5.get(1.0, 'end-1c'), re.I | re.DOTALL)
            inputT5 = '// \n' + '// Script 4 DISABLE section Starts Here' + '\n//'  + '\n'.join(scriptInputT5)    
        else:
            inputT5 =''          
        tempT = (inputT1 + inputT2 + inputT3 + inputT5)
        #newT = re.sub(r'(>\n)\n\n(?!\n\n)|\n{3,}', '', tempT )      
        self.script_txt4.insert(END, '\n[DISABLE] \n' + ''.join(tempT))
        
    def results_window(self):
        """
        Create a new function to display merged script
        A separate window for the Merged script to be displayed in
        """
        mergeResults = Toplevel(padx=10, pady=10)
        mergeResults.title("Your new Script after the merge process")
        mergeResults.grab_set()
        mergeResults.focus()
        w = 680
        h = 575
        sw = mergeResults.winfo_screenwidth()
        sh = mergeResults.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        mergeResults.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        btnExit = Button(mergeResults, text="Close", command=mergeResults.destroy)
        btnExit.grid(column=0, row=2, sticky='s', pady='5')        
        # This is were your new merged script will be stored.
        result_txt4 = Text(mergeResults, borderwidth=1, relief='sunken')
        result_txt4.config(font=("consolas",  11), undo=True,
                                wrap='none', height=28, width=80)
        result_txt4.grid(row=0, column=0, sticky="new")
        scrollx = Scrollbar(mergeResults, command=result_txt4.yview)
        scrollx.grid(row=0, column=1, sticky='nsw')
        result_txt4['yscrollcommand'] = scrollx.set
        scrolly = Scrollbar(mergeResults, orient='horizontal',
                                         command=result_txt4.xview)
        scrolly.grid(row=1, column=0,  sticky='esw')
        result_txt4['xscrollcommand'] = scrolly.set
        result_txt4.insert(INSERT, self.script_txt4.get(1.0, 'end-1c'))
        # attach copy/paste popup menu to textbox
        result_txt4.bind("<Button-3>", self.popup)
        

    # Resets the program for new merge. Linked to the Reset Button
    def on_reset(self):
        self.script_txt1.delete(1.0,  END)
        self.script_txt2.delete(1.0,  END)
        self.script_txt3.delete(1.0,  END)
        self.script_txt5.delete(1.0,  END)            
    
    # Exit the program. Linked to the Exit Button
    def onExit(self):
        self.root.destroy()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.configure(background="black")
    MyApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
