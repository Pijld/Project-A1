import random
import datetime

current_time = datetime.datetime.now()
print(current_time.strftime("%x " + "%H:" + "%M:"))

bad_words = ("kut", "fuck", "shit", "hoer", "tering")

max_character = 140
min_character = 1

stations = ["Almere", "Amersfoort", "Utrecht"]


name = input("enter your name: ")
if name == "":
    print("anonymous \n")
else:
    print(name + "\n")


while True:
    message = input("enter a message (max 140 characters): ")
    if min_character <= len(message) <= max_character:
        if any(word in message for word in bad_words):
            print("no bad words please.")
        else:
            print(message + "\n")
            with open("output.txt", "w") as outputfile:
                outputfile.write(message + " \nname: " + str(name))
            break
    elif min_character > len(message):
        print("please enter a message, containing at least 1 character.")
    else:
        print("please enter a maximum of 140 characters.")

print(f"printed out on {random.choice(stations)} station")
