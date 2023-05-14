import socket
import random
import sqlite3
import os
import time 

os.remove("answers.db")

HOST = 'localhost'
PORT = 12346
conn = sqlite3.connect('answers.db')
cursor = conn.cursor()
conn_question = sqlite3.connect('myDB.db')
cursor_question = conn_question.cursor()

# Créer la table si elle n'existe pas
with open('create_database_answer.sql', 'r') as f:
    cursor.executescript(f.read())

# Obtenir le nombre de joueurs
player_number = int(input("How many players? "))

# Créer une socket pour écouter les connexions des clients
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(player_number)

# Attendre les connexions des clients et les ajouter à la liste des joueurs
players = {}
for i in range(player_number):
    client_socket, address = server_socket.accept()
    print(f"Nouvelle connexion de {address}")
    player_name = client_socket.recv(1024).decode().strip()
    players[player_name] = client_socket
    client_socket.sendall(f"{player_name} joined the game!".encode())

# Obtenir le nombre de questions
nb_question = cursor_question.execute("SELECT COUNT(*) FROM question").fetchone()[0]

# Poser les questions
for i in range(1, nb_question + 1):
    # Récupérer la question depuis la base de données
    cursor_question.execute("SELECT question FROM QUESTION WHERE id = ?;", (i,))
    question = cursor_question.fetchone()[0]

    # Envoyer la question à tous les joueurs
    for player_name, player_socket in players.items():
        player_socket.sendall(f"Question: {question}\n".encode())

    # Attendre les réponses des joueurs
    for player_name, player_socket in players.items():
        answer = player_socket.recv(1024).decode().strip()
        print(f"{player_name} answered: {answer}")
        cursor.execute("INSERT INTO answer(Name, Answer) VALUES (?, ?)", (player_name, answer,))
        conn.commit()

# Fermer la connexion
conn.close()
