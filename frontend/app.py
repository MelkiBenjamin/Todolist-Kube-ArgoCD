from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

# Liste de todo list (initialisée avec quelques exemples)
todo_lists = [
    {"id": 1, "name": "Liste 1", "tasks": [
        {"id": 1, "content": "Faire les courses", "status": "TODO"},
        {"id": 2, "content": "Apprendre Flask", "status": "TODO"},
    ]},
    {"id": 2, "name": "Liste 2", "tasks": [
        {"id": 3, "content": "Créer une todo list", "status": "TODO"},
    ]}
]

# Prénom récupéré depuis la variable d'environnement CONFIGMAP_NAME
configmap_name = os.environ.get('CONFIGMAP_NAME', 'Benjamin')

@app.route('/')
def index():
    return render_template('index.html', todo_lists=todo_lists, configmap_name=configmap_name)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_list_name = request.form['list_name']
        new_task_content = request.form['task_content']
        new_task_status = "TODO"

        new_list = {"id": len(todo_lists) + 1, "name": new_list_name, "tasks": [
            {"id": len(todo_lists) + 1, "content": new_task_content, "status": new_task_status}
        ]}
        todo_lists.append(new_list)

        return jsonify({"message": "Todo ajoutée avec succès!"})

    return render_template('add.html', configmap_name=configmap_name)

@app.route('/done/<int:todo_id>/<int:task_id>')
def mark_as_done(todo_id, task_id):
    for todo_list in todo_lists:
        if todo_list['id'] == todo_id:
            for task in todo_list['tasks']:
                if task['id'] == task_id:
                    task['status'] = 'DONE'
                    return jsonify({"message": "Tâche marquée comme DONE!"})

    return jsonify({"error": "Todo ou tâche non trouvée!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
