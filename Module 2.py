from tkinter import *
window = Tk()
window.geometry("642x400")
window.resizable(False, False)

window.title("inlogscherm")
# icon =

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

def new_window():

login_button = Button(window,text="Log in", font=("Open Sans", 16, "bold"), bg="#0063D3", fg="white",
                      command=new_window)

window.mainloop()