from flask import Flask, jsonify
from traitement import run_traitement

app = Flask(__name__)

@app.route('/data')
def data():
    result = run_traitement("debug.html")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
