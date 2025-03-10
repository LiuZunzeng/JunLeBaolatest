from flask import Flask, request, jsonify, send_from_directory
from main import Solver
import json
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)


app = Flask(__name__)


@app.route('/process', methods=['POST'])
def submit():
    data = request.json
    fetch_result = Solver(data).start()

    return jsonify(fetch_result)

    #except Exception as e:
        #fetch_result = {'code': 2, 'result': None}
        #return jsonify(fetch_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)

