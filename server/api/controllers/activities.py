import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import Activity, File, Experiment
import os, wave, cv2

def create_activity(experiment_id):
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        num_participants = int(request.form["num_participants"])
        comment = request.form["comment"]
        
        # Verificar si el experimento existe
        experiment = Experiment.objects(id=experiment_id).first()
        if not experiment:
            return jsonify({'error': 'Experiment not found'}), 404
        
        # Verificar si ya existe una actividad con el mismo nombre
        if Activity.objects(name=name).first():
            return jsonify({'error': 'Activity with the same name already exists'}), 400
        
        # Crear actividad
        activity = Activity(name=name, date=date, num_participants=num_participants, comment=comment, experiment=experiment)
        
        # Guardar archivos de audio y video
        try:
            file_audio = request.files['file_audio']
            file_audio.save(os.path.join(os.getcwd(), "data", str(activity.id), "audio.wav"))
            # Obtener la información del audio
            audio = wave.open(os.path.join(os.getcwd(), "data", str(activity.id), "audio.wav"), 'r')
            frames = audio.getnframes()
            rate = audio.getframerate()
            duration = frames / float(rate)
            audio.close()
            # Crear objeto File y agregarlo a la actividad
            audio_file = File(filename="audio.wav", type="audio", length=duration, frames=frames, rate=rate)
            activity.files.append(audio_file)
        except KeyError:
            pass
        except FileNotFoundError:
            return jsonify({'error': 'Error al subir el archivo de audio'}), 400
        
        try:
            file_video = request.files['file_video']
            file_video.save(os.path.join(os.getcwd(), "data", str(activity.id), "video.mp4"))
            # Obtener la información del video
            cap = cv2.VideoCapture(os.path.join(os.getcwd(), "data", str(activity.id), "video.mp4"))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = total_frames / fps
            cap.release()
            # Crear objeto File y agregarlo a la actividad
            video_file = File(filename="video.mp4", type="video", length=duration, frames=total_frames, fps=fps)
            activity.files.append(video_file)
        except KeyError:
            pass
        except FileNotFoundError:
            return jsonify({'error': 'Error al subir el archivo de video'}), 400
        
        # Guardar la actividad
        activity.save()
        
        return jsonify({'message': 'Activity created'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400


def get_activities(experiment_id):
    if request.method == "GET":
        experiment = Experiment.objects(id=experiment_id).first()
        if not experiment:
            return jsonify({'error': 'Experiment not found'}), 404
        
        activities = Activity.objects(experiment=experiment)
        
        return activities.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activity(name):
    if request.method == "GET":
        # obtener primera actividad que coincida con el nombre
        try:
            activity = Activity.objects(name=name).first().to_json()
        except AttributeError:
            return jsonify({'message': 'Activity not found'}), 404
        return Response(activity, mimetype="application/json", status=200)
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activity_by_id(id):
    if request.method == "GET":
        # obtener primera actividad que coincida con el nombre
        try:
            activity = Activity.objects.get(id=id).to_json()
        except AttributeError:
            return jsonify({'message': 'Activity not found :c'}), 404
        return Response(activity, mimetype="application/json", status=200)
    else:
        return jsonify({'message': 'Bad request'}), 400    

def delete_activity(name):
    if request.method == "DELETE":
        activity = Activity.objects(name=name).first()
        try:
            shutil.rmtree(os.path.join(os.getcwd(),"data", str(activity.id)))
        except FileNotFoundError:
            pass
        activity.delete()
        return jsonify({'message': 'Activity deleted'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_activity_file(name, filename):
    if request.method == "GET":
        activity = Activity.objects(name=name).first()
        if activity:
            for file in activity.files:
                if file.filename == filename:
                    return send_from_directory(os.path.join(os.getcwd(),"data", str(activity.id)), filename, as_attachment=True)
            return jsonify({'message': 'File not found'}), 404
        return jsonify({'message': 'Activity not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def edit_activity(name):
    if request.method == "PUT":
        name = request.form["name"]
        date = request.form["date"]
        num_participants = int(request.form["num_participants"])
        comment = request.form["comment"]
        experiment_id = request.form["experiment_id"]

        # Verificar si la actividad existe
        activity = Activity.objects(name=name).first()
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Verificar si el experimento existe
        experiment = Experiment.objects(id=experiment_id).first()
        if not experiment:
            return jsonify({'error': 'Experiment not found'}), 404

        # Actualizar los campos de la actividad
        activity.name = name
        activity.date = date
        activity.num_participants = num_participants
        activity.comment = comment
        activity.experiment = experiment

        # Guardar los cambios en la actividad
        activity.save()

        return jsonify({'message': 'Activity updated'}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400
