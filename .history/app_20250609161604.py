from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Bem-vindo à sua API Flask!"

if __name__ == '__main__':
    app.run(debug=True)