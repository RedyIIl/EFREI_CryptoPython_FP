from cryptography.fernet import Fernet
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Bienvenue sur la page d'accueil. Allez sur /encrypt pour chiffrer des données."

@app.route('/encrypt', methods=['GET', 'POST'])
def encryptage():
    if request.method == 'POST':
        # Récupère la clé de l'utilisateur et la valeur à chiffrer
        user_key = request.form.get('key')
        valeur = request.form.get('valeur')

        if not user_key or not valeur:
            return "Erreur : clé ou valeur manquante", 400

        try:
            # Crée un objet Fernet avec la clé fournie
            f = Fernet(user_key)
            # Convertir la valeur en bytes et la chiffrer
            valeur_bytes = valeur.encode()
            token = f.encrypt(valeur_bytes)
            return f"Valeur encryptée : {token.decode()}"
        except Exception as e:
            return f"Erreur lors de l'encryptage : {str(e)}", 400

    # Si la méthode est GET, affiche le formulaire
    return render_template_string('''
        <form action="/encrypt" method="POST">
            <label for="key">Entrez votre clé de chiffrement (base64) :</label>
            <input type="text" id="key" name="key" required><br><br>

            <label for="valeur">Entrez la valeur à chiffrer :</label>
            <input type="text" id="valeur" name="valeur" required><br><br>

            <input type="submit" value="Chiffrer">
        </form>
    ''')

if __name__ == "__main__":
    app.run(debug=True)
