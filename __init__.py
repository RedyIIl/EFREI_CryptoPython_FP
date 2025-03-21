from cryptography.fernet import Fernet
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Affiche un formulaire pour saisir la clé et la valeur à chiffrer
    return render_template_string('''
        <form action="/encrypt" method="POST">
            <label for="key">Entrez votre clé de chiffrement :</label>
            <input type="text" id="key" name="key" required><br><br>

            <label for="valeur">Entrez la valeur à chiffrer :</label>
            <input type="text" id="valeur" name="valeur" required><br><br>

            <input type="submit" value="Chiffrer">
        </form>
    ''')

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

if __name__ == "__main__":
    app.run(debug=True)
