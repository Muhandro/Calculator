from flask import Flask, request, jsonify, render_template
from calculator import Calculator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_expression():
    data = request.json
    expression = data.get('expression')
    if expression is None:
        return jsonify({"error": "No expression provided"}), 400

    calculator = Calculator()
    try:
        result = calculator.evaluate(expression)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
