"""
Data Parser for Cheat Engine Auto Assemble scripts.

This class does all the file manipluation, temp db creation
and new script generation.

Created by Jack Ackermann

data_parse.py
"""

from tkinter import messagebox
import xml.etree.cElementTree as ET
import sqlite3, re
from pathlib import Path


#  Link ct_temp.db file to the dbName var.
dbName = 'ct_temp.db'


def create_db():
    """
    Create temp DB file to store the read XML data
    
    Check if old db still exists, if found,
    delete and create ct_temp.db
    """

    # dbName = 'ct_temp.db'
    dbFile = Path(dbName)
    
    if dbFile.is_file():
        dbFile.unlink()
        con = sqlite3.connect(dbName)
    else:
        con = sqlite3.connect(dbName)

    cur = con.cursor()  # Create cursor needed for file reading
    
    # Create New table in temp db, with our four new fields
    cur.execute('''CREATE TABLE CheatTable (
                ID TEXT NOT NULL, Description TEXT,
                VariableType TEXT, AssemblerScript TEXT)''')
    
    con.commit()  # update and save changes to DB.

def parse_ct(orig_file):
    """
    Read XML data from the Cheat Table File.
    
    Parse XML data and insert parsed data into Temp DB file
    
    We do this to prevent damage or use of origianl '.ct' file.
    """
  
    # Open Cheat Table so we can access data
    # tree = ET.ElementTree(file='test.ct')
    tree = ET.ElementTree(file=orig_file)
    root = tree.getroot()

    # Create connection to temp db file
    con = sqlite3.connect(dbName)
    cur = con.cursor()  # Create cursor needed for file reading

    # Find elements and store them in a list
    lst1, lst2, lst3, lst4 = [], [], [], []
    id_num, desc, var_type, ass_script = '', '', '', ''

    for elem in list(tree.iter(tag='CheatEntry')):
        try: 
            id_num = elem.find('ID').text          
            desc = elem.find('Description').text
            var_type = elem.find('VariableType').text
            ass_script = elem.find('AssemblerScript').text
        except AttributeError:
            pass
        else:
            lst1.append(id_num)
            lst2.append(desc)
            lst3.append(var_type)
            lst4.append(ass_script + '[DISEND]')
            
    # Loop through the lists, populate temp db with all data from lists        
    for a, b, c, d in zip(lst1, lst2, lst3, lst4):
        cur.execute('INSERT INTO CheatTable VALUES (?, ?, ?, ?)',
                    (str(a), str(b), str(c), str(d)))
        
    con.commit()  # update and save changes to DB.
    con.close()  # close connection to DB.

def delete_db():
    """
    This function deletes the temp_db file
    
    This function is called by the main program's Reset Button
    """
    dbFile = Path(dbName)
    if dbFile.is_file():
        dbFile.unlink()

def upt_listbox(data):
    """
    Create connection to temp db.

    Select the fields content you want to read.

    Then close connection to database when done reading
    """
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute('SELECT ID, Description FROM CheatTable')

    r = cur.fetchall()
    data = []

    # Read DB
    for i in r:
        data.append(i)

    con.close()  # Close the connection to the DB
    return data

def merge_scripts(fName, selText, script_name):
    """
    Create connection to temp db.

    Select the fields for which data you want to read.
    Create regex to find all [ENABLE] portions, enableText
    Create regex to find all [DISABLE] portions, disableText

    Then combine all the enable setions into one.
    Combine all the Disabled sections into one.    
    Finally combine both new sections to form your new script.

    Then close connection to database when done reading
    """
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    args = selText
    sql = "SELECT Description, AssemblerScript FROM CheatTable where \
            Description in ({seq})".format(seq = ','.join(['?']*len(args)))
    cur.execute(sql, args)
    r = cur.fetchall()

    eLabel, eText, enableTXT = '', '', "[ENABLE]\n\n"

    for n, d in r:
        eLabel = str("//\n//" + n + " ENABLE section Starts Here \n//")
        eText = re.findall(r'\[ENABLE\](.*?)\[DISABLE\]',
                                    d, re.I | re.DOTALL)
        enableTXT = enableTXT + (eLabel + ''.join(eText) + '\n')

    dLabel, dText, disableTXT = '', '', "\n\n\n\n[DISABLE]\n\n"

    for n, d in r:
        dLabel = str("//\n//" + n + " DISABLE section Starts Here \n//")
        dText = re.findall(r'\[DISABLE\](.*?)\[DISEND\]',
                                    d, re.I | re.DOTALL)
        disableTXT = disableTXT + (dLabel + ''.join(dText) + '\n')

    new_script = enableTXT + disableTXT
    # Call funct, Add new data to template
    xml_template(fName, new_script, script_name)

def xml_template(fName, new_script, script_name):
    """
    Create all the needed xml headers and body for new Script here
    
    Insert your new script data into this newly created template

    When done, the new script is inserted into the cheat table file.
    """

    idNO = id_counter(fName)
    tree = ET.parse(fName)
    root = tree.getroot()
    a = root.find('CheatEntries')
    b = ET.SubElement(a, 'CheatEntry')
    c = ET.SubElement(b, 'ID')
    d = ET.SubElement(b, 'Description')
    e = ET.SubElement(b, 'LastState')
    f = ET.SubElement(b, 'VariableType')
    g = ET.SubElement(b, 'AssemblerScript')
    c.text = str(idNO)
    d.text = '"' + script_name + '"'
    f.text = 'Auto Assembler Script'
    g.text = new_script
    tree.write(fName, encoding="UTF-8", xml_declaration=True)
    messagebox.showinfo("Insert Success", 'Script Merge Completed')

def id_counter(fName):
    """
    Loop through all ID no's, sort numbers, get last number,
    add 1, this will be your ID number for the new Script
    """
    tree = ET.ElementTree(file=fName)
    root = tree.getroot()
    id_no = []
    for elem in tree.iter():
        if elem.tag == 'ID':
            txt1 = elem.text
            id_no.append(txt1)

    c = sorted(id_no)
    c = c[-1]
    idNO = (int(c) + 1)
    
    return idNO









