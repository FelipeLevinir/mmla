import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import Mark, MarkType, Experiment, Event
import os, wave, cv2

def create_mark(experiment_id, event_id):
    if request.method == "POST":
        try:
            # print(request.form)

            # Intentar recuperar datos de la solicitud
            try:
                comment = request.form["comment"]
                time_in_video = request.form["time_in_video"]
                mark_type_ids = json.loads(request.form["mark_type"])
            except Exception as e:
                return jsonify({'message': 'Error retrieving form data', 'error': str(e)}), 400

            # Buscar objetos en la base de datos
            try:
                experiment = Experiment.objects.get(id=experiment_id)
                event = Event.objects.get(id=event_id)
            except Exception as e:
                return jsonify({'message': 'Error fetching experiment or event', 'error': str(e)}), 400

            # Buscar y agregar MarkTypes
            # mark_type_refs = []  # Lista para almacenar las referencias de MarkType
            # for mark_type_id in mark_type_ids:
            #     try:
            #         mark_type = MarkType.objects.get(id=mark_type_id)
            #         mark_type_refs.append(mark_type.to_dbref())  # Obtener la referencia de MarkType y agregarla a la lista
            #     except Exception as e:
            #         return jsonify({'message': f'Error fetching MarkType with id {mark_type_id}', 'error': str(e)}), 400

            # Crear y guardar la marca
            try:
                mark = Mark(comment=comment,
                            time_in_video=time_in_video,
                            experiment=experiment,
                            event=event,
                            mark_type=mark_type_ids)  # Asignar la lista de referencias de MarkType
                mark.save()
            except Exception as e:
                return jsonify({'message': 'Error saving the mark', 'error': str(e)}), 400

            return jsonify({'message': 'Mark created'}), 200
        except Exception as e:
            return jsonify({'message': 'Bad request', 'error': str(e)}), 400
        
    else:
        return jsonify({'message': 'Bad request'}), 400


def get_mark(mark_id):
    if request.method == "GET":
        try:
            mark = Mark.objects.get(id=mark_id)
            return mark.to_json(), 200
        except AttributeError:
            return jsonify({'message': 'Mark not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400


def get_marks(experiment_id,event_id):
    if request.method == "GET":
        try:
            # Filtrar las marcas por experiment_id y event_id
            marks = Mark.objects.filter(experiment=experiment_id, event=event_id)
            
            # Convertir los resultados a JSON y devolverlos
            return marks.to_json(), 200
        except Exception as e:
            return jsonify({'message': 'Bad request', 'error': str(e)}), 400
    else:
        return jsonify({'message': 'Bad request'}), 400

def delete_mark(mark_id):
    if request.method == "DELETE":
        try:
            mark = Mark.objects.get(id=mark_id)
            mark.delete()
            return jsonify({'message': 'Mark deleted'}), 200
        except AttributeError:
            return jsonify({'message': 'Mark not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400
    
