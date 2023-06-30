import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import MarkType, Experiment
import os, wave, cv2

def create_mark_type(id_experiment):
    if request.method == "POST":
        name = request.form.get("name")

        experiment = Experiment.objects(id=id_experiment).first()
        if not experiment:
            return jsonify({'message': 'Experiment not found'}), 404

        mark_type = MarkType(name=name, experiment=experiment)
        mark_type.save()

        return jsonify({'message': 'MarkType created', 'mark_type_id': str(mark_type.id)}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_mark_type(mark_type_id):
    if request.method == "GET":
        mark_type = MarkType.objects(id=mark_type_id).first()
        if mark_type:
            return mark_type.to_json(), 200
        else:
            return jsonify({'message': 'MarkType not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_mark_types(id_experiment):
    if request.method == "GET":
        experiment = Experiment.objects(id=id_experiment).first()
        if not experiment:
            return jsonify({'message': 'Experiment not found'}), 404
        
        mark_types = MarkType.objects(experiment=experiment)
        return mark_types.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def delete_mark_type(mark_type_id):
    if request.method == "DELETE":
        mark_type = MarkType.objects(id=mark_type_id).first()
        if mark_type:
            mark_type.delete()
            return jsonify({'message': 'MarkType deleted'}), 200
        else:
            return jsonify({'message': 'MarkType not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def edit_mark_type(mark_type_id):
    if request.method == "PUT":
        mark_type = MarkType.objects(id=mark_type_id).first()
        if mark_type:
            name = request.form.get("name")
            experiment_id = request.form.get("experiment_id")

            experiment = Experiment.objects(id=experiment_id).first()
            if not experiment:
                return jsonify({'message': 'Experiment not found'}), 404

            mark_type.name = name
            mark_type.experiment = experiment
            mark_type.save()

            return jsonify({'message': 'MarkType updated'}), 200
        else:
            return jsonify({'message': 'MarkType not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400