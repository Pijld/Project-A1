import random
import datetime
import psycopg2

bad_words = ("kut", "fuck", "shit", "hoer", "tering")


def input_name():
    name = input("enter your name: ")
    if name == "":
        name = "anonymous"
    return name


def input_message():
    current_time = datetime.datetime.now()
    real_date = current_time.date()
    real_time = current_time.strftime("%H:" + "%M")
    max_character = 140
    min_character = 1
    while True:
        name = input_name()
        message = input("enter a message (max 140 characters): ")
        if min_character <= len(message) <= max_character:
            with open("output.txt", "a") as f:
                f.write(f"name ; {str(name)} ; message ; {str(message)} ; datetime ; {real_date} ; {real_time}\n")
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


input_message()
connect_database()
