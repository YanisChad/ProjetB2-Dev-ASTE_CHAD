import tkinter
import socket
import sqlite3

# connect to the database
# conn = sqlite3.connect('myDB.db')
# cur = conn.cursor()

conn_answer = sqlite3.connect('answers.db')
cur_answer = conn_answer.cursor()

# conn.commit()

# create a socket to communicate with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12346))

def create_profile(name, quizz):
    client_socket.send(f"{name}".encode())
    response = client_socket.recv(1024).decode()
    button_start.destroy()
    button_create.destroy()
    name_entry.destroy()
    profile_label.destroy()
    quizz_entry.destroy()
    quizz_label.destroy()
    name_label.destroy()
    game(0, quizz)
    return response == "PROFILE_CREATED"

def create_question(question, point, name):

    question_entry.delete(0, tkinter.END)
    point_entry.delete(0, tkinter.END)

    print("create_question : " + question)

    conn = sqlite3.connect(name + '.db')
    cur = conn.cursor()

    # insert the question into the database
    cur.execute("CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, question TEXT, point INTEGER)")
    cur.execute("INSERT INTO question (question, point) VALUES (?, ?)", (question, point))
    conn.commit()

    # send a message to the server to create the question
    client_socket.send(f"CREATE_QUESTION::{question}::{point}".encode())
    response = client_socket.recv(1024).decode()
    return response == "QUESTION_CREATED"

def get_questions(quizz):

    conn = sqlite3.connect(quizz + '.db')
    cur = conn.cursor()
    # retrieve all questions from the database
    cur.execute("SELECT question FROM QUESTION")
    questions = [row[0] for row in cur.fetchall()]
    return questions

def count_question(quizz):
    conn = sqlite3.connect(quizz + '.db')
    cur = conn.cursor()
    # retrieve the number of questions from the database
    cur.execute("SELECT COUNT(*) FROM QUESTION")
    count = cur.fetchone()[0]
    return count

# Interface Tkinter
app = tkinter.Tk()
app.title("ZepQuizz")
app.geometry("800x600")
app['background']='#252525'


global button_start
global button_quit
global button_create
global name_entry
global profile_label

name = tkinter.StringVar()
answer = tkinter.StringVar()
quizz = tkinter.StringVar()
button_start = tkinter.Button(app, text="Start", bg="#252525", fg="#ffffff", command= lambda: create_profile(name.get(), quizz.get()), height=2, width=10, font=("Arial", 20))
button_quit = tkinter.Button(app, text="Quit", bg="#252525", fg="#ffffff", command= lambda: app.destroy(), height=2, width=10, font=("Arial", 20))
button_create = tkinter.Button(app, text="Create Quizz", bg="#252525", fg="#ffffff", command= lambda: name_quizz(), height=2, width=10, font=("Arial", 20))

profile = tkinter.PhotoImage(file="images/profile.png")
profile = profile.subsample(5, 5)
profile_label = tkinter.Label(app, image=profile)
profile_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

name_entry = tkinter.Entry(app, width=20, textvariable=name, font=("Arial", 20))
name_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
name_label = tkinter.Label(app, text="Your name : ", bg="#252525", fg="#ffffff", font=("Arial", 20))
name_label.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)

quizz_entry = tkinter.Entry(app, width=20, textvariable=quizz, font=("Arial", 20))
quizz_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
quizz_label = tkinter.Label(app, text="Choose your quizz : ", bg="#252525", fg="#ffffff", font=("Arial", 20))
quizz_label.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

button_start.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
button_quit.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
button_create.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

def name_quizz():
    global title_entry
    global label_title
    global button_valid

    button_start.destroy()
    button_create.destroy()
    name_entry.destroy()
    profile_label.destroy()
    quizz_entry.destroy()
    quizz_label.destroy()
    name_label.destroy()

    name = tkinter.StringVar()
    title_entry = tkinter.Entry(app, width=20, textvariable=name, font=("Arial", 20))
    title_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    label_title = tkinter.Label(app, text="Titre du Quizz", bg="#252525", fg="#ffffff", font=("Arial", 20))
    label_title.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    print("name_quizz : " + name.get())
    button_valid = tkinter.Button(app, text="Valider", bg="#252525", fg="#ffffff", command= lambda: new_question(name.get()), height=2, width=10, font=("Arial", 20))
    button_valid.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

def new_question(name_quizz):

    global question_entry
    global point_entry

    button_start.destroy()
    button_create.destroy()
    name_entry.destroy()
    profile_label.destroy()
    title_entry.destroy()
    label_title.destroy()
    button_valid.destroy()
    quizz_entry.destroy()
    quizz_label.destroy()
    name_label.destroy()

    question = tkinter.StringVar()
    point = tkinter.StringVar()
    question_entry = tkinter.Entry(app, width=20, textvariable=question, font=("Arial", 20))
    question_entry.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)
    point_entry = tkinter.Entry(app, width=20, textvariable=point, font=("Arial", 20))
    point_entry.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)
    label_question = tkinter.Label(app, text="ecris une question", bg="#252525", fg="#ffffff", font=("Arial", 20))
    label_question.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)
    label_point = tkinter.Label(app, text="combien de point vaut la question", bg="#252525", fg="#ffffff", font=("Arial", 20))
    label_point.place(relx=0.7, rely=0.3, anchor=tkinter.CENTER)
    button_question = tkinter.Button(app, text="Envoyer", bg="#252525", fg="#ffffff", command= lambda: create_question(question.get(), point.get(), name_quizz), height=2, width=10, font=("Arial", 20))
    button_question.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

def game(i, quizz):
    questions = get_questions(quizz)
    question_label = tkinter.Label(app, text=questions[i+1], bg="#252525", fg="#ffffff", font=("Arial", 20))
    question_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    answer = tkinter.StringVar()
    answer_entry = tkinter.Entry(app, width=20, textvariable=answer, font=("Arial", 20))
    answer_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    button_answer = tkinter.Button(app, text="Envoyer", bg="#252525", fg="#ffffff", command= lambda: get_answer(answer.get(), i, question_label, answer_entry, button_answer, quizz), height=2, width=10, font=("Arial", 20))
    button_answer.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


def get_answer(answer, question_index, question_label, answer_entry, button_answer, quizz):
    client_socket.send(f"{answer}".encode())
    question_label.destroy()
    if question_index == count_question(quizz) - 2:
        for widget in app.winfo_children():
            widget.destroy()
        label_end = tkinter.Label(app, text="Fin du Quizz", bg="#252525", fg="#ffffff", font=("Arial", 20))
        label_end.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        button_verify = tkinter.Button(app, text="Verifier les réponses", bg="#252525", fg="#ffffff", command= lambda: verify(), height=2, width=10, font=("Arial", 20))
        button_verify.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        button_quit = tkinter.Button(app, text="Quit", bg="#252525", fg="#ffffff", command= lambda: app.destroy(), height=2, width=10, font=("Arial", 20))
        button_quit.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        
    else:
        answer_entry.delete(0, tkinter.END)
        question_label.after(200, lambda: game(question_index + 1, quizz))

scores = {}

def verify():
    global scores

    for widget in app.winfo_children():
        widget.destroy()

    conn_answer = sqlite3.connect('answers.db')
    cursor_answer = conn_answer.cursor()
    cursor_name = conn_answer.cursor()

    # Récupération des réponses des joueurs
    cursor_answer.execute("SELECT answer FROM answer")
    cursor_name.execute("SELECT name FROM answer")
    answers = cursor_answer.fetchall()
    name = cursor_name.fetchall()

    # Initialisation du score
    for player_name in name:
        if player_name[0] not in scores:
            scores[player_name[0]] = 0

    # Création de la fenêtre pour afficher les réponses
    window = tkinter.Toplevel(app)
    window.title("Vérification des réponses")

    # Affichage de la première réponse
    index = 0
    label = tkinter.Label(window, text=answers[index][0])
    label.pack()
    label_name = tkinter.Label(window, text=name[index][0])
    label_name.pack()

    # Fonction pour faire défiler les réponses
    def next_answer():
        nonlocal index
        index += 1
        if index < len(answers):
            label.config(text=answers[index][0])
            label_name.config(text=name[index][0])
        else:
            window.destroy()
            announce_winner()


    # Création du bouton "Valider"
    def validate_answer():
        global scores
        player_name = name[index][0]
        scores[player_name] += 1
        next_answer()

    validate_button = tkinter.Button(window, text="Valider", command=validate_answer)
    validate_button.pack()

    # Création du bouton "Refuser"
    def refuse_answer():
        next_answer()

    refuse_button = tkinter.Button(window, text="Refuser", command=refuse_answer)
    refuse_button.pack()

    def announce_winner():
        global scores
        winner = max(scores, key=scores.get)
        winner_score = scores[winner]

        # Création de la fenêtre pour annoncer le vainqueur
        winner_window = tkinter.Toplevel(app)
        winner_window.title("Le vainqueur est...")

        # Affichage du nom du vainqueur et de son score
        winner_label = tkinter.Label(winner_window, text="Le vainqueur est : " + winner + " avec un score de " + str(winner_score))
        winner_label.pack()

        # Affichage de la fenêtre
        winner_window.grab_set()
        app.wait_window(winner_window)

    # Affichage de la fenêtre
    window.grab_set()
    app.wait_window(window)

    cursor_answer.close()
    conn_answer.close()

app.mainloop()
