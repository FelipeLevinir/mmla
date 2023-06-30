import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import Experiment
import os, wave, cv2

def create_experiment():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        description = request.form.get("description")
        
        if not name or not code:
            return jsonify({'message': 'Name and code are required'}), 400

        experiment = Experiment(name=name, code=code, description=description)
        experiment.save()

        return jsonify({'message': 'Experiment created'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400
    
def get_experiments():
    if request.method == "GET":
        experiments = Experiment.objects()
        return experiments.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_experiment(code):
    if request.method == "GET":
        try:
            experiment = Experiment.objects(code=code).first()
            if experiment:
                return experiment.to_json(), 200
            else:
                return jsonify({'message': 'Experiment not found'}), 404
        except AttributeError:
            return jsonify({'message': 'Bad request'}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400
    
def get_experiment_by_id(id):
    if request.method == "GET":
        try:
            experiment = Experiment.objects.get(pk=id)
            if experiment:
                return experiment.to_json(), 200
            else:
                return jsonify({'message': 'Experiment not found :('}), 404
        except AttributeError:
            return jsonify({'message': 'Bad request'}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400

def delete_experiment(code):
    if request.method == "DELETE":
        experiment = Experiment.objects(code=code).first()
        if experiment:
            experiment.delete()
            return jsonify({'message': 'Experiment deleted'}), 200
        else:
            return jsonify({'message': 'Experiment not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def edit_experiment(code):
    if request.method == "PUT":
        experiment = Experiment.objects(code=code).first()
        if experiment:
            name = request.form.get("name")
            code = request.form.get("code")
            description = request.form.get("description")

            experiment.name = name
            experiment.code = code
            experiment.description = description
            experiment.save()

            return jsonify({'message': 'Experiment updated'}), 200
        else:
            return jsonify({'message': 'Experiment not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400