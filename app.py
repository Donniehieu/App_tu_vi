from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from convert_solar_to_lunar import convert_solar_to_lunar


app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)