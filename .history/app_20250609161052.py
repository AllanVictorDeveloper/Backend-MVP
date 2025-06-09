from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Bem-vindo à sua API Flask!"

if __name__ == '__main__': # <-- Importante!
    app.run(debug=True)