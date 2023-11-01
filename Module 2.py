from tkinter import *

window = Tk()
window.geometry("642x400")
window.resizable(False, False)

window.title("inlogscherm")
icon = PhotoImage(file="nslogo.png")
window.iconphoto(True, icon)

canvas = Canvas(window, bg='#FFFFFF', width=642, height=400)
canvas.pack()
photo=PhotoImage(file="inlogscherm.png")
canvas.create_image(0, 0, image=photo, anchor=NW)

inloggen_text = Label(window, text="inloggen", font=("Open Sans", 25, "bold"), bg="#FFC917")
inloggen_text.place(x=40, y=82, height=60, width=145)

email_text = Label(window, text="Emailadres", font=("Open Sans", 16, "bold"), bg="#FFC917")
email_text.place(x=32, y=200, height=20, width=142)

wachtwoord_test = Label(window, text="Wachtwoord", font=("Open Sans", 16, "bold"), bg="#FFC917")
wachtwoord_test.place(x=40,y=270, height=20, width=142)

email_input = Text(window, bg="#dedbde", font=("Arial", 12))
email_input.place(x=210, y=200, height=25, width=410)

wachtwoord_input = Entry(window, bg="#dedbde", font=("Arial", 12), show="*")
wachtwoord_input.place(x=210, y=270, height=25, width=410)

foutmelding_text = Label(window, text="", font=("Arial, 10"), bg="#FFC917", fg="red")
foutmelding_text.place(x=210,y=300,height=20,width=400)

def new_window():
    email = email_input.get(1.0, "end-1c")
    wachtwoord = wachtwoord_input.get()
    with open("moderators.txt", "r") as f:
        for line in f:
            words = line.strip().split(";")  # remove newline and split into words
            if words[1].strip() == email and words[2].strip() == wachtwoord:
                open_window = Tk()
                window.destroy()
            # else:
            #     if window.winfo_exists():
            #         foutmelding_text.config(text="onjuist emailadres of wachtwoord.")


login_button = Button(window,text="Log in", font=("Open Sans", 16, "bold"), bg="#0063D3", fg="white",
                      activebackground="#0063D3", activeforeground="white",command=new_window)
login_button.place(x=332,y=350, height=40,width=200)

window.mainloop()

#bron end-1c chat gpt. betekent, end -1 character, om nieuwe line weg te halen.