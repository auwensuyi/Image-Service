from flask import Flask, jsonify, request

app = Flask(__name__)

items = [3,4,5]

@app.route('/', methods=['GET'])
def get_items():
    return jsonify({'/': items})

if __name__ == '__main__':
    app.run(debug=True)