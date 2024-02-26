from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import os
import yaml

app = Flask(__name__, template_folder='/app/frontend/templates')
CORS(app, origins="*")   # Activation de CORS pour toutes les routes

# Prénom récupéré depuis la variable d'environnement CONFIGMAP_NAME
configmap_name = os.environ.get('CONFIGMAP_NAME', 'Benjamin')
DATA_FILE_PATH = '/app/data/todolists.yaml'

def load_todolists():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            todolists = yaml.safe_load(file) or []
        return todolists
    return []

def save_todolists(todolists):
    with open(DATA_FILE_PATH, 'w') as file:
        yaml.dump(todolists, file)

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html', configmap_name=configmap_name, todo_lists=load_todolists())

@app.route('/add')
@cross_origin()
def add():
    return render_template('add.html')

@app.route('/new', methods=['POST'])
@cross_origin()
def new_todolist():
    data = request.get_json()
    if data and 'name' in data and 'tasks' in data:
        todolists = load_todolists()
        todolist = {'name': data['name'], 'tasks': data['tasks']}
        todolists.append(todolist)
        save_todolists(todolists)
        return jsonify({'message': 'TodoList ajoutée avec succès!'}), 200
    else:
        return jsonify({'error': 'Données incomplètes'}), 400

@app.route('/done', methods=['POST'])
@cross_origin()
def mark_as_done():
    data = request.get_json()
    if data and 'name' in data and 'content' in data:
        todolists = load_todolists()
        for todolist in todolists:
            if todolist['name'] == data['name']:
                for task in todolist['tasks']:
                    if task['content'] == data['content']:
                        task['status'] = 'DONE'
                        save_todolists(todolists)
                        return jsonify({'message': 'Tâche marquée comme DONE!'}), 200
        return jsonify({'error': 'Todo ou tâche non trouvée!'}), 404
    else:
        return jsonify({'error': 'Données incomplètes'}), 400

@app.route('/getall', methods=['GET'])
@cross_origin()
def get_all_todolists():
    todolists = load_todolists()
    return jsonify({'todolists': todolists}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
