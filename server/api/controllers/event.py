import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import Event, Activity, Experiment
import os, wave, cv2

def create_event(id_activity):
    if request.method == "POST":
        try:
            start_time = float(request.form["start_time"])
            end_time = float(request.form["end_time"])

            activity = Activity.objects(id=id_activity).first()

            event = Event(start_time=start_time, end_time=end_time, activity=activity)
            event.save()

            return jsonify({'message': 'Event created'}), 200
        except AttributeError:
            return jsonify({'message': 'Bad request'}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_events(id_activity):
    if request.method == "GET":
        activity = Activity.objects(id=id_activity).first()
        if not activity:
            return jsonify({'error': 'Experiment not found'}), 404
        
        events = Event.objects(activity=activity)
        
        return events.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_event(event_id):
    if request.method == "GET":
        try:
            event = Event.objects.get(id=event_id)
            return event.to_json(), 200
        except AttributeError:
            return jsonify({'message': 'Event not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def delete_event(event_id):
    if request.method == "DELETE":
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return jsonify({'message': 'Event deleted'}), 200
        except AttributeError:
            return jsonify({'message': 'Event not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def edit_event(event_id):
    if request.method == "PUT":
        try:
            event = Event.objects.get(id=event_id)
            start_time = int(request.form["start_time"])
            end_time = int(request.form["end_time"])
            activity_id = request.form["activity_id"]
            experiment_id = request.form["experiment_id"]

            activity = Activity.objects.get(id=activity_id)
            experiment = Experiment.objects.get(id=experiment_id)

            event.start_time = start_time
            event.end_time = end_time
            event.activity = activity
            event.experiment = experiment
            event.save()

            return jsonify({'message': 'Event updated'}), 200
        except AttributeError:
            return jsonify({'message': 'Bad request'}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400