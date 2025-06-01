import subprocess
from flask import Flask, jsonify, request
from traitement import run_traitement
import os

app = Flask(__name__)

@app.route('/data')
def data():
    result = run_traitement("debug.html")
    return jsonify(result)

@app.route('/refresh', methods=['POST'])
def refresh_data():
    try:
        subprocess.run(["python3", "main.py"], check=True)
        return jsonify({"status": "success", "message": "Données mises à jour"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/debug')
def debug_html():
    try:
        with open("debug.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Fichier debug.html non trouvé.", 404
    except Exception as e:
        return f"Erreur lors de la lecture du fichier : {str(e)}", 500

@app.route('/')
def home():
    return '''
    <h1>Eurofos API</h1>
    <button onclick="refreshData()">Refresh Data</button>
    <script>
    function refreshData() {
        fetch('/refresh', { method: 'POST' })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(err => alert('Erreur: ' + err));
    }
    </script>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Démarrage du serveur Flask sur le port", port)
    app.run(host='0.0.0.0', port=port)
