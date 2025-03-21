from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request
from flask import render_template
from flask import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil

@app.route('/encrypt', methods=['POST'])
def encryptage():
    user_key = request.form.get('key')  # Récupère la clé de l'utilisateur
    valeur = request.form.get('valeur')  # Récupère la valeur à chiffrer

    if not user_key or not valeur:
        return "Erreur : clé ou valeur manquante", 400

    try:
        f = Fernet(user_key)  # Crée un objet Fernet avec la clé fournie
        valeur_bytes = valeur.encode()  # Conversion str -> bytes
        token = f.encrypt(valeur_bytes)  # Encrypt la valeur
        return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
    except Exception as e:
        return f"Erreur lors de l'encryptage : {str(e)}", 400  # Si la clé est invalide

@app.route('/decrypt', methods=['POST'])
def decryptage():
    user_key = request.form.get('key')  # Récupère la clé de l'utilisateur
    token = request.form.get('token')  # Récupère le token à déchiffrer

    if not user_key or not token:
        return "Erreur : clé ou token manquants", 400

    try:
        f = Fernet(user_key)  # Crée un objet Fernet avec la clé fournie
        token_bytes = token.encode()  # Conversion str -> bytes
        decrypted_value = f.decrypt(token_bytes)  # Déchiffre la valeur
        return f"Valeur décryptée : {decrypted_value.decode()}"  # Retourne la valeur décryptée
    except Exception as e:
        return f"Erreur de décryptage : {str(e)}", 400  # Si la clé ou le token est invalide

if __name__ == "__main__":
    app.run(debug=True)
