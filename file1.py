import random
import datetime
import psycopg2

current_time = datetime.datetime.now()
real_time = current_time.strftime("%x " + "%H:" + "%M")

bad_words = ("kut", "fuck", "shit", "hoer", "tering")


def input_name():
    name = input("enter your name: ")
    if name == "":
        name = "anonymous"
    return name


def input_message():
    max_character = 140
    min_character = 1
    while True:
        name = input_name()
        message = input("enter a message (max 140 characters): ")
        if min_character <= len(message) <= max_character:
            with open("output.txt", "a") as f:
                f.write(f"name ; {str(name)} ; message ; {str(message)} ; datetime ; {str(real_time)} \n")
            return message
        elif min_character > len(message):
            print("please enter a message, containing at least 1 character.")
        else:
            print("please enter a maximum of 140 characters.")


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


def conn_database():
    goedgekeurd = True
    gekozen_station = kies_station()
    lijn = read_message()
    if any(word in lijn[3] for word in bad_words):
        goedgekeurd = False

    conn = psycopg2.connect(host="20.229.131.82", dbname="Data messages", user="postgres", password="postgres")
    cur = conn.cursor()

    create_table = """CREATE TABLE IF NOT EXISTS berichten(
    id SERIAL PRIMARY KEY,
    naam VARCHAR(255),
    bericht VARCHAR(141), 
    station VARCHAR(255),
    datum VARCHAR(255),
    status VARCHAR(255))"""

    if goedgekeurd:
        insert_table = """INSERT INTO berichten(naam, bericht, station, datum, status) VALUES(%s, %s, %s, %s, %s)"""
        insert_value = (lijn[1], lijn[3], gekozen_station, lijn[5], "goedgekeurd")
    else:
        insert_table = """INSERT INTO berichten(naam, bericht, station, datum, status) VALUES(%s, %s, %s, %s, %s)"""
        insert_value = (lijn[1], lijn[3], gekozen_station, lijn[5], "afgekeurd")

    cur.execute(create_table)
    cur.execute(insert_table, insert_value)
    conn.commit()

    cur.close()
    conn.close()


input_message()
kies_station()
conn_database()
