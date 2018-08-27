'''
Japanese Study Guide using Flashcard format
Using the SQLite library in Python  

Daniel Yang
'''

#Needs UTF-8 Encoding to display Japanese characters 
import sqlite3

#Initial Book Selection Menu 
def MainMenu():
    print("Book Selection")
    print("1. げんき I")
    
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
    
MainMenu()
GenkiIVocabTable()

'''
TO-DOs
(げんき I)
Add all of the vocab so far into the げんき I table
Create the table for Category

(Book Selection)

'''
