from flask import Flask, jsonify
from traitement import run_traitement
import os

app = Flask(__name__)

@app.route('/data')
def data():
    result = run_traitement("debug.html")
    return jsonify(result)

@app.route('/')
def home():
    return "✅ Eurofos API en ligne. Accédez aux données via /data"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
