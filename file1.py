import random
import datetime
import psycopg2

bad_words = ("kut", "fuck", "shit", "hoer", "tering")

from tkinter import *


window = Tk()
window.title('voer uw bericht in')

icon = PhotoImage(file="nslogo.png")
window.iconphoto(True, icon)

window.geometry('960x470')
window.resizable(False, False)

canvas = Canvas(window, bg='#FFFFFF', width=960, height=460)
canvas.pack()
all_images = []
all_images.append(PhotoImage(file="achtergrond.png"))  # 0
canvas.create_image(0, 0, image=all_images[0], anchor=NW)


deel_ervaring = Label(window, height=1, width=22, text="Deel uw ervaring",
                      font=("Open Sans", 22, "bold"), bg="#FFC917")
deel_ervaring.place(x=295,y=41)

vraag_naam = Label(window, height=1, width=22, text="Laat hier uw naam achter:",
                   font=("Open Sans", 16, "bold"), bg="#FFC917")
vraag_naam.place(x=220,y=133)

schrijf_bericht = Label(window, height=1, width=34, text="Schrijf hier het bericht dat u wilt achterlaten:",
                   font=("Open Sans", 16, "bold"), bg="#FFC917")
schrijf_bericht.place(x=152,y=259)

entry_naam = Entry(window, bg="#dedbde", font=("Arial", 15))
entry_naam.place(x=109,y=167,height=57,width=530)

text_message = Text(window, bg="#dedbde", font=("Arial", 13))
text_message.place(x=109, y=293, height=142, width=530)


def anoniemfunction():
    if(x.get()==1):
        entry_naam.delete(0,END)
        entry_naam.config(state=DISABLED)
    elif(x.get()==0):
        entry_naam.config(state=NORMAL)
x = IntVar()

checkbutton=Checkbutton(window,text="Anoniem", font=("Open Sans",13,"bold"),height=2,width=15,
                        bg="#0063D3", fg="black", selectcolor="white", activebackground="#0063D3",
                        activeforeground="black", variable=x, onvalue=1, offvalue=0, command=anoniemfunction)
checkbutton.place(x=700,y=171)


def verstuur_message():
    current_time = datetime.datetime.now()
    real_date = current_time.date()
    real_time = current_time.strftime("%H:" + "%M")
    max_character = 140
    min_character = 1
    while True:
        name = entry_naam.get()
        if name == "":
            name = "Anoniem"
        message = text_message.get(1.0,END).strip()
        if min_character <= len(str(message)) <= max_character:
            with open("output.txt", "a") as f:
                f.write(f"name ; {str(name)} ; message ; {str(message)} ; datetime ; {real_date} ; {real_time}\n")
                entry_naam.delete(0, END)
                text_message.delete(1.0, END)
            return message
        elif min_character > len(str(message)):
            print("please enter a message, containing at least 1 character.")
        else:
            print("please enter a maximum of 140 characters.")

verstuur_button = Button(window,text="Verstuur", font=("Open Sans",13,"bold"),
                         bg="#0063D3", fg="black", activeforeground="black", activebackground="#0063D3",
                         command=verstuur_message)
verstuur_button.place(x=700,y=320, height=70, width=179.5)

window.mainloop()

# def input_name():
#     name = input("enter your name: ")
#     if name == "":
#         name = "anonymous"
#     return name



def read_message():
    with (open("output.txt", "r") as f):
        lines = f.readlines()
        line = lines[-1] if lines else None
        words = line.split(";")
        return words


def kies_station():
    with open("stations.txt", "r") as f:
        lines = f.readlines()
        random_station = random.choice(lines)
        return random_station


def connect_database():
    goedgekeurd = True

    gekozen_station = kies_station()
    lijn = read_message()
    if any(word in lijn[3] for word in bad_words):
        goedgekeurd = False

    gekozen_mod = random.randint(1, 4)

    conn = psycopg2.connect(host="20.229.131.82", dbname="stationszuil", user="postgres", password="postgres")
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS moderators')

    create_mod = """CREATE TABLE IF NOT EXISTS moderators(
    id INT PRIMARY KEY, 
    naam VARCHAR(255),
    email VARCHAR(255)) """

    create_table = """CREATE TABLE IF NOT EXISTS berichten(
    id SERIAL PRIMARY KEY,
    naam VARCHAR(255),
    bericht VARCHAR(141), 
    station VARCHAR(255),
    datum VARCHAR(255),
    status VARCHAR(255),
    tijd VARCHAR(255),
    moderator INT) """

    # fk_mod = """"ALTER TABLE berichten ADD CONSTRAINT fk_mod
    # FOREIGN KEY REFERENCES(moderator) REFERENCES moderators.id"""

    insert_mod = """INSERT INTO moderators(naam, email, id)
    VALUES(%s, %s, %s)"""
    mod_values = [("Jan Versteeg", "Janversteeg@moderator.com", 1), ("Henk de Jong", "HenkdeJong@moderator.com", 2),
                  ("Pam de Haan", "PamdeHaan@moderator.com", 3), ("Youri Lang", "YouriLang@moderator.com", 4)]

    if goedgekeurd:
        insert_table = """INSERT INTO berichten(naam, bericht, station, datum, tijd, status, moderator) 
        VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        insert_value = (lijn[1], lijn[3], gekozen_station, lijn[5], lijn[6], "goedgekeurd", gekozen_mod)
    else:
        insert_table = """INSERT INTO berichten(naam, bericht, station, datum, tijd, status, moderator) 
        VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        insert_value = (lijn[1], lijn[3], gekozen_station, lijn[5], lijn[6], "afgekeurd", gekozen_mod)

    cur.execute(create_mod)
    cur.execute(create_table)
    # cur.execute(fk_mod)
    cur.executemany(insert_mod, mod_values)
    cur.execute(insert_table, insert_value)
    conn.commit()
    cur.close()
    conn.close()


connect_database()
