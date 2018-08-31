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
genkiICategories = { 0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6 }

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
    print("Category Menu")
    print("`. Go By Lesson Number")
    print("0. Display All")
    print("1. Greetings")
    print("2. School/Time")
    print("3. Countries")
    print("4. Majors")
    print("5. Occupations")
    print("6. Countries")
    sel = input()
    print()
    
    ##Later change to use a dict or some other method instead of ifs, with each book corresponding to a 
    ## group of choices 
    if sel == '0':
        displayAll() 
    else:
        cards = gatherCards(sel)
        print("Press ENTER to start flashcarding ")
        flashCard(cards)
    
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
        cards = gatherCards(0)
        flashCard(cards)
    else:
        return    

#SELECTS the words for the selected category and turns the info into a list
#Uses passed number to determine which cards to choose 
##Second parameter so that it can be used with different books?
def gatherCards(sel):
    if sel == 0:
        cur.execute('''SELECT Meaning FROM VocabDB ORDER BY Number''') ##Needs ORDER BY so that it does not go out of order
        meaning = tuple(cur.fetchall())
        cur.execute('''SELECT Hiragana FROM VocabDB''') 
        hiragana = cur.fetchall()
        cur.execute('''SELECT Kanji FROM VocabDB''') 
        kanji = cur.fetchall()     
    else: 
        cur.execute('''SELECT Meaning FROM VocabDB WHERE Category = ? ORDER BY Number''',(sel))
        meaning = tuple(cur.fetchall())
        cur.execute('''SELECT Hiragana FROM VocabDB WHERE Category = ?''',(sel)) 
        hiragana = cur.fetchall()
        cur.execute('''SELECT Kanji FROM VocabDB WHERE Category = ?''',(sel)) 
        kanji = cur.fetchall()          
    
    card = list(zip(meaning, hiragana, kanji))    
    return card
    
#Shows one word after another, with the English first and then Japanese after
##Change so that it can flashcard other tables, create a random version 
def flashCard(card):
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
                       Meaning TEXT NOT NULL,
                       Hiragana TEXT NOT NULL,
                       Kanji TEXT,
                       Chapter INT NOT NULL,
                       Category INT NOT NULL)''') ##Turn into a foreign key linking with the Category table
    
    #Insert values into the table 
    ##Turn this and previous execute into try so it won't stop when trying to write onto existing table?
    ##Should be a way to put long lists of values into other .py files 
    # 1 - Greetings, 2 - School/Time, 3 - Countries, 4 - Majors, 5 - Occupations, 6 - Family    
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
                   (17, 'Nice to meet you', 'どうぞよろしく', '', 0, 1),
                   (18, 'Um...', 'あの', '', 1, 2),
                   (19, 'Now', 'いま', '', 1, 2),
                   (20, 'English (language)', 'えいご', '', 1, 2),
                   (21, 'Yes', 'ええ', '', 1, 2),
                   (22, 'Student', 'がくせい', '', 1, 2),
                   (23, 'Language', '~ご', '', 1, 2),
                   (24, 'Highschool', 'こうこう', '', 1, 2),
                   (25, 'PM', 'ごご', '', 1, 2),
                   (26, 'AM', 'ごぜん', '', 1, 2),
                   (27, '...Years old', '~さい', '', 1, 2),
                   (28, 'Mr/Ms...', '~さん', '', 1, 2),
                   (29, 'Oclock', '~じ', '', 1, 2),
                   (30, 'People', '~じん', '', 1, 2),
                   (31, 'Teacher', 'せんせい', '', 1, 2),
                   (32, 'Major', 'せんもん', '', 1, 2),
                   (33, 'That is right', 'そうです', '', 1, 2),
                   (34, 'College', 'だいがく', '', 1, 2),
                   (35, 'Telephone', 'でんわ', '', 1, 2),
                   (36, 'Friend', 'ともだち', '', 1, 2),
                   (37, 'Name', 'なまえ', '', 1, 2),
                   (38, 'What', 'なん/なに', '', 1, 2),
                   (39, 'Japan', 'にほん', '', 1, 2),
                   (40, '...Year student', '~ねんせい', '', 1, 2),
                   (41, 'Yes', 'はい', '', 1, 2),
                   (42, 'Half', 'はん', '', 1, 2),
                   (43, 'Number', 'ばんごう', '', 1, 2),
                   (44, 'I', 'わたし', '', 1, 2),
                   (45, 'America', 'アメリカ', '', 1, 3),
                   (46, 'Britain', 'イギリス', '', 1, 3), 
                   (47, 'Australia', 'オーストラリア', '', 1, 3), 
                   (48, 'Korea', 'かんこく', '', 1, 3), 
                   (49, 'Sweden', 'スウェーデン', '', 1, 3),
                   (50, 'China', 'ちゅうごく', '', 1, 3),
                   (51, 'Science', 'かがく', '', 1, 4), 
                   (52, 'Asian studies', 'アジアけんきゅう', '', 1, 4), 
                   (53, 'Economics', 'けいざい', '', 1, 4),
                   (54, 'International relations', 'こくさいかんけい', '', 1, 4), 
                   (55, 'Computer', 'コンピューター', '', 1, 4), 
                   (56, 'Anthropology', 'じんるいがく', '', 1, 4), 
                   (57, 'Politics', 'せいじ', '', 1, 4), 
                   (58, 'Business', 'ビジネス', '', 1, 4), 
                   (59, 'Literature', 'ぶんがく', '', 1, 4), 
                   (60, 'History', 'れきし', '', 1, 4), 
                   (61, 'Job; Work', 'しごと', '', 1, 5),
                   (62, 'Doctor', 'いしゃ', '', 1, 5), 
                   (63, 'Office worker', 'かいしゃいん', '', 1, 5), 
                   (64, 'Highschool student', 'こうこうせい', '', 1, 5), 
                   (65, 'Housewife', 'しゅふ', '', 1, 5), 
                   (66, 'Graduate student', 'だいがくいんせい', '', 1, 5), 
                   (67, 'College student', 'だいがくせい', '', 1, 5), 
                   (68, 'Lawyer', 'べんごし', '', 1, 5), 
                   (69, 'Mother', 'おかあさん', '', 1, 6), 
                   (70, 'Father', 'おとうさん', '', 1, 6), 
                   (71, 'Older sister', 'おねえさん', '', 1, 6), 
                   (72, 'Older brother', 'おにいさん', '', 1, 6), 
                   (73, 'Younger sister', 'いもうと', '', 1, 6), 
                   (74, 'Younger brother', 'おとうと', '', 1, 6)''')
     
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


