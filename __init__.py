from cryptography.fernet import Fernet
import base64
import hashlib
from flask import Flask, render_template_string, request

app = Flask(__name__)

def derive_key(user_password):
    """Transforme une clé en texte brut en une clé Fernet valide"""
    key = hashlib.sha256(user_password.encode()).digest()  # Hash en 32 bytes
    return base64.urlsafe_b64encode(key)  # Encode en base64

@app.route('/encrypt', methods=['GET', 'POST'])
def encryptage():
    if request.method == 'POST':
        user_password = request.form.get('password')  # Clé en texte brut
        valeur = request.form.get('valeur')

        if not user_password or not valeur:
            return "Erreur : clé ou valeur manquante", 400

        try:
            # Transformer la clé en une clé Fernet
            key = derive_key(user_password)
            f = Fernet(key)

            # Convertir la valeur en bytes et la chiffrer
            valeur_bytes = valeur.encode()
            token = f.encrypt(valeur_bytes)
            return f"Valeur encryptée : {token.decode()}"
        except Exception as e:
            return f"Erreur lors de l'encryptage : {str(e)}", 400

    # Affiche le formulaire
    return render_template_string('''
        <form action="/encrypt" method="POST">
            <label for="password">Entrez votre clé de chiffrement :</label>
            <input type="text" id="password" name="password" required><br><br>

            <label for="valeur">Entrez la valeur à chiffrer :</label>
            <input type="text" id="valeur" name="valeur" required><br><br>

            <input type="submit" value="Chiffrer">
        </form>
        <p>🔒 La clé sera transformée automatiquement en clé sécurisée.</p>
    ''')

if __name__ == "__main__":
    app.run(debug=True)
