"""
python Auto Assembler Script Merger for Cheat Engine scripts.

Created by Jack Ackermann
"""

from tkinter import Tk, ttk, Frame, Button, PhotoImage, INSERT, Scrollbar,\
     Label, Text, FALSE, filedialog, END, Listbox, MULTIPLE, messagebox
import webbrowser, shutil, os
from data_parse import create_db, parse_ct, delete_db, upt_listbox, \
     merge_scripts



class AutoInsert(Frame):
    

    def centre_window(self):
        w = 700
        h = 440
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs,  background="black")
        self.root = parent
        centre_title = (' '*20)  # Use spaces to center Title
        self.root.title(centre_title + 'Auto Assemble Script Merger for Cheat'+
                            ' Engine Scripts -  by Hawkeye ZAR')
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew',  padx=15,  pady=5)
        
        # Create Openfile Dialog
        open_file = Button(self, text='Open Script', command=self.load_file)
        open_file.grid(column=0, row=0, sticky='wn', padx=5, pady=5)

        # Create a Text Field to Display file Name
        self.fname = Text(self, borderwidth=1, relief='sunken')
        self.fname.config(font=('consolas', 10), wrap='none',
                                height=1, width=80)
        self.fname.grid(row=0, column=0, sticky='w', padx='85', columnspan=2)
        self.fname.insert(INSERT, (' '*25 + '...No file opened...'))

        # Create List Box, selection for scripts to be merged
        self.listbox = Listbox(self, selectmode=MULTIPLE,
                               relief='sunken', width=70, height=8)
        self.listbox.grid(row=1, column=0, padx=85, pady=5, sticky='w')
        self.listbox.insert(END, 'Select all Assembler scripts ' \
                            'that you want merged')
        self.scrollb = Scrollbar(self, command=self.listbox.yview)
        self.scrollb.grid(row=1, column=0, pady=5, padx=500, sticky='ns')
        self.listbox['yscrollcommand'] = self.scrollb.set

        # Clear Contents of Script Name TextBox when user clicks inside it.
        def callback(event):
            self.focus_set()
            self.script_name.delete(1.0, END)
        # Create text widget for new Script Name
        self.script_name = Text(self, relief='sunken')
        self.script_name.config(height=1, width=53)
        self.script_name.grid(row=2, column=0, padx=85, pady=2, sticky='w')
        self.script_name.insert(INSERT, 'Type in a name for your new script')
        self.script_name.bind("<Button-1>", callback)
        
        # Create Merge Script Button
        merge_btn = Button(self, text='Merge Scripts', command=self.onMerge)
        merge_btn.grid(column=0, row=3, sticky='w', pady=6, padx=180)
        
        # Resets the Program to start a new merge
        reset_btn = Button(self, text='Reset', command=self.onReset, width=10) 
        reset_btn.grid(column=0, row=3,  sticky='w', pady=6, padx=85)
        
        # Terminates the Program
        exit_btn = Button(self, text='Exit', command=self.onExit, width=10) 
        exit_btn.grid(column=0, row=3, sticky='w', pady=6, padx=435)
          
        # Add Image to Promote Cheat The Game
        photo = PhotoImage(file="appImage.gif")
        appImage = Label(self, image=photo, background='black')
        appImage.photo = photo
        appImage.grid(column=0, row=8, sticky='nsw', rowspan=3,
                      columnspan=3, padx=50)

        # Create function to open link in browser
        def callback(event):
            weblink = (r"https://www.facebook.com/groups/CheatTheGame/")
            webbrowser.open_new(weblink)
        # Add link to Cheat The Game Facebook Page    
        fbLink = Label(self, text="Go to:  Cheat The Game", cursor="hand2", 
                        foreground="yellow", background="black",
                        font=('Arial', 12, 'bold', 'underline'))
        fbLink.grid(column=0, row=9, sticky='sw', padx=240, 
                    pady=10, rowspan=3, columnspan=3)
        fbLink.bind("<Button-1>", callback)  
        Label(self, text="Shout out goes to all the great peeps over at CTG",
              foreground="white", background="black", font=('Arial', 10, 'bold')
              ).grid(column=0, row=8, sticky='nw', padx=180, pady=15,
                     columnspan=3, rowspan=2)

        self.orig_file = ''
    def load_file(self):
        """
        Load the Cheat Table File you want to use.

        Then call the create_db() function to create tempory db
        to save the contents of the cheat table so that
        the original files stays untouched.
        
        After temp db is created, call the parse_ct() and parse the
        data to the db file called, temp_db.db

        Call the upt_listbox() function to update fields in
        self.listbox with available scripts that can
        be merged.
        """
        create_db()  # call func to create temp db

        # Create the file selection dialog
        self.orig_file = filedialog.askopenfilename(filetypes=[
                                                ("CheatEngine CT File","*.ct")])

        # Update Name field text box with file name.
        self.fname.delete(1.0, END)
        self.fname.insert(INSERT, self.orig_file)
        
        parse_ct(self.orig_file)  # call function parse_ct()

        # call function upt_listbox(), update self.listbox
        self.listbox.delete(0, END)
        for i, d in upt_listbox(self):
            self.listbox.insert(END, d)

    def onReset(self):
        """
        Resets the Program to begin a new merge

        Function delete_db() gets called to delete the temp_db.db
        """
        # Clear all required fields
        self.fname.delete(1.0, END)
        self.listbox.delete(0, END)
        self.script_name.delete(1.0, END)

        # Enter new Data into required fields
        self.fname.insert(INSERT, (' '*25 + '...No file opened...'))
        self.listbox.insert(END, 'Select all Assembler scripts ' \
                            'that you want merged')
        self.script_name.insert(INSERT, 'Type in a name for your new script')

        delete_db()  # Delete the Temp DB File.

        messagebox.showinfo("Reset Program", 'The Program has been Reset \
                            \n\nAll data has been deleted')

    def onMerge(self):
        """
        Create copy of opened cheat table to insert our new script into.
        This will prevent any corruption or damage to the original file.

        Update fname path with the newly copied file.

        Get scripts to be merged, only the scripts that have been selected.

        Call the "merge_scripts(fName)" function to do merge and update
        the cheat table file copy with our new script.
        """

        index = self.listbox.curselection()
        if len(index) >= 2:
            fName = 'New Script ' + os.path.basename(self.orig_file)
            shutil.copy2(self.orig_file, fName)  # Make Copy of file to modify
            self.fname.delete(1.0, END)
            self.fname.insert(INSERT, fName) 

            selText = []
            for i in index:  # Get list of selected scripts to be merged.
                selText.append(self.listbox.get(i))

            # Call the function to merge the selected scripts
            script_name = self.script_name.get(1.0, END)
            merge_scripts(fName, selText, script_name)
                
        else:
            messagebox.showinfo("Error: Selection is too short!",\
                                'Select at least two scripts to merge.')

      
    # Exit the program. Linked to the Exit Button
    def onExit(self):
        delete_db()
        self.root.destroy()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.configure(background="black")
    AutoInsert(root)
    root.mainloop()

if __name__ == '__main__':
    main()
