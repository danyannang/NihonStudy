'''
Japanese Study Guide using Flashcard format
Using the SQLite library in Python  

Daniel Yang
'''

#Needs UTF-8 Encoding to display Japanese characters 
import sqlite3
import re

#Dictionary for books and their corresponding .db files
db = { '1':'GenkiI.db' }

#Initial Book Selection Menu 
def mainMenu():
    print("Book Selection")
    print("1. げんき I")
    sel = input()
    print()
    return sel 
    
#Opens the .db file for the corresponding selection    
def openBook(book):
    conn = sqlite3.connect(db[book])
    return conn 

#Chapter/Section Menu 
def genkiIMenu(): ##Make into a general one 
    print("Lesson Menu")
    print("1. Display All")
    sel = input()
    print()
    
    ##Later change to use a dict or some other method instead of ifs, with each book corresponding to a 
    ## group of choices 
    if sel == '1':
        displayAll() 
    
#Shows all info in the selected table    
##Change so that it doesn't only SELECT from VocabDB (げんき I) 
def displayAll():
    cur.execute('''SELECT * FROM VocabDB''') ##Change so that it does SELECT * from a custom "View"
    for line in cur.fetchall():
        line = re.sub(r'[^\w\s]', '', str(line)) ##Change so that it doesn't get rid of "(polite)"
        print(line)
    print()

    enter = input("Press ENTER to start flashcarding ")
    if enter == '':
        flashCard()
    else:
        return    
        
#Shows one word after another, with the English first and then Japanese after
##Change so that it can flashcard other tables, create a random version 
def flashCard():
    cur.execute('''SELECT Meaning FROM VocabDB ORDER BY Number''') ##Needs ORDER BY so that it does not go out of order
    meaning = tuple(cur.fetchall())
    cur.execute('''SELECT Hiragana FROM VocabDB''') 
    hiragana = cur.fetchall()
    cur.execute('''SELECT Kanji FROM VocabDB''') 
    kanji = cur.fetchall()     
    
    card = list(zip(meaning, hiragana, kanji))
    
    column = 0 #0 for meaning, 1 for hiragana, 2 for kanji
    for term in range(len(card)):
        for category in range(3): #3 columns in total to rotate through 
            next = input()
            if next == '':
                print(*card[term][category], end = '') ##Fix so that it actually prints on same line (needed?)
                column += 1
                if column == 3:
                    print()
                    column = 0
            
    print(card[0][0])
    for term in card:
        term = re.sub(r'[^\w\s]', '', str(term))
    
#Closes the .db file
def closeBook(conn):
    conn.close() 
    
#Creates the base vocab table for げんき I
#Number, Meaning, Hiragana/Katakana, Kanji, Chapter, Category 
def genkiIVocabTable():
    conn = sqlite3.connect('GenkiI.db')
    cur = conn.cursor()
    
    #Uncomment to clear the table     
    cur.execute('''DROP TABLE IF EXISTS VocabDB''')    
    
    #Creates new table if it doesn't exist already      
    cur.execute('''CREATE TABLE IF NOT EXISTS VocabDB(
                       Number INT NOT NULL,
                       Meaning TEXT NOT NULL PRIMARY KEY,
                       Hiragana TEXT NOT NULL,
                       Kanji TEXT,
                       Chapter INT NOT NULL,
                       Category INT NOT NULL)''') ##Turn into a foreign key linking with the Category table
    
    #Insert values into the table 
    ##Turn this and previous execute into try so it won't stop when trying to write onto existing table?
    ##Should be a way to put long lists of values into other .py files 
    cur.execute('''INSERT INTO VocabDB 
                   VALUES
                   (1, 'Good morning', 'おはよう', '', 0, 1),
                   (2, 'Good morning (polite)', 'おはようございます', '', 0, 1),
                   (3, 'Good afternoon', 'こんにちは', '', 0, 1),
                   (4, 'Good evening', 'こんばんは', '', 0, 1),
                   (5, 'Good bye', 'さようなら', '', 0, 1),
                   (6, 'Good night', 'おやすみなさい', '', 0, 1),
                   (7, 'Thank you', 'ありがとう', '', 0, 1),
                   (8, 'Thank you (polite)', 'ありがとうございます', '', 0, 1),
                   (9, 'Excuse me; I am sorry', 'すみません', '', 0, 1),
                   (10, 'No; Not at all', 'いいえ', '', 0, 1),
                   (11, 'I will go and come back', 'いってきます', '', 0, 1),
                   (12, 'Please go and come back', 'いってらっしゃい', '', 0, 1),
                   (13, 'I am home', 'ただいま', '', 0, 1),
                   (14, 'Let us eat', 'いただきます', '', 0, 1),
                   (15, 'Thank you for the meal', 'ごちそさまでした', '', 0, 1),
                   (16, 'How do you do', 'はじめまして', '', 0, 1),
                   (17, 'Nice to meet you', 'どうぞよろしく', '', 0, 1)''')
       
    conn.commit()
    conn.close()
    
def genkiICategoryTable():
    pass
    
genkiIVocabTable()
bookSelection = mainMenu()
conn = openBook(bookSelection)
cur = conn.cursor() ##Move into a function?
genkiIMenu()

closeBook(conn)


