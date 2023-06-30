import shutil, json
from flask import request, jsonify, Response, send_from_directory
from database.models import MarkLevel, MarkType
import os, wave, cv2

def create_mark_level(id_marktype):
    if request.method == "POST":
        name = request.form.get("name")
        value = request.form.get("value")

        mark_type = MarkType.objects(id=id_marktype).first()
        if not mark_type:
            return jsonify({'message': 'MarkType not found'}), 404

        mark_level = MarkLevel(name=name,value=value ,marktype=mark_type)
        mark_level.save()

        mark_type.update(push__marklevel=mark_level.id)

        return jsonify({'message': 'MarkLevel created', 'mark_level_id': str(mark_level.id)}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400
    
def get_mark_level(mark_level_id):
    if request.method == "GET":
        mark_level = MarkLevel.objects(id=mark_level_id).first()
        if mark_level:
            return mark_level.to_json(), 200
        else:
            return jsonify({'message': 'MarkLevel not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400

def get_mark_levels(id_marktype):
    if request.method == "GET":
        mark_type = MarkType.objects(id=id_marktype).first()
        if not mark_type:
            return jsonify({'message': 'MarkType not found'}), 404
        
        mark_levels = MarkLevel.objects(marktype=mark_type)
        return mark_levels.to_json(), 200
    else:
        return jsonify({'message': 'Bad request'}), 400
    
def delete_mark_level(mark_level_id):
    if request.method == "DELETE":
        mark_level = MarkLevel.objects(id=mark_level_id).first()
        if mark_level:
            mark_level.delete()
            return jsonify({'message': 'MarkLevel deleted'}), 200
        else:
            return jsonify({'message': 'MarkLevel not found'}), 404
    else:
        return jsonify({'message': 'Bad request'}), 400
    
# def edit_mark_level(mark_level_id):
#     if request.method == "PUT":
#         mark_level = MarkLevel.objects(id=mark_level_id).first()
#         if mark_level:
#             name = request.form.get("name")
#             mark_type_id = request.form.get("mark_type_id")

#             mark_type = MarkType.objects(id=mark_type_id).first()
#             if not mark_type:
#                 return jsonify({'message': 'MarkType not found'}), 404

#             mark_level.name = name
#             mark_level.marktype = mark_type
#             mark_level.save()

#             return jsonify({'message': 'MarkLevel updated'}), 200
#         else:
#             return jsonify({'message': 'MarkLevel not found'}), 404
#     else:
#         return jsonify({'message': 'Bad request'}), 400