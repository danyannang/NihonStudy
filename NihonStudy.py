'''
Japanese Study Guide using Flashcard format
Using the SQLite library in Python  

Daniel Yang
'''

#Needs UTF-8 Encoding to display Japanese characters 
import sqlite3

#Dictionary for books and their corresponding .db files
db = { '1':'GenkiI.db' }

#Initial Book Selection Menu 
def MainMenu():
    print("Book Selection")
    print("1. げんき I")
    sel = input()
    return sel 
    
#Opens the .db file for the corresponding selection    
def openBook(book):
    conn = sqlite3.connect(db[int(book)])
    
#Closes the .db file
def closeBook(conn):
    conn.close() 
    
#Creates the base empty vocab table for げんき I
#Chapter(foreign key), Category(foreign key), Hiragana/Katakana, Kanji, Meaning 
def GenkiIVocabTable():
    conn = sqlite3.connect('GenkiI.db')
    cur = conn.cursor()
    
    #Creates new table if it doesn't exist already      
    cur.execute('''CREATE TABLE IF NOT EXISTS VocabDB(             
                       Meaning TEXT NOT NULL PRIMARY KEY,
                       Hiragana TEXT NOT NULL,
                       Kanji TEXT,
                       Chapter INT NOT NULL,
                       Category INT NOT NULL FOREIGN KEY)''')
    
    #Insert values into the table 
    cur.execute('''INSERT INTO VocabDB 
                   VALUES
                   ('Good morning', 'おはよう', '', 1, 1)''')
    
    #Uncomment to clear the table     
    #cur.execute("DROP TABLE IF EXISTS StudentsDB")
    conn.commit()
    conn.close()
    
GenkiIVocabTable()
bookSelection = MainMenu()
conn = openBook(bookSelection)
closeBook(conn)


