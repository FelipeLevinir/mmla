from flask import Flask
import utils.config as config
from flask_cors import CORS
from flasgger import Swagger
from database.db import initialize_db
from flask_cors import cross_origin

from controllers.activities import create_activity, get_activities, get_activity_by_id, get_activity, delete_activity, get_activity_file
from controllers.analysis import create_analysis, get_analysis, get_analysis_by_id, delete_analysis
from controllers.results import get_results
from controllers.indicator import create_indicator_measure, get_indicator_measure, download_indicator_measure_csv
from controllers.experiments import create_experiment, get_experiment_by_id ,get_experiments, get_experiment, delete_experiment, edit_experiment
from controllers.marktype import create_mark_type, get_mark_type, get_mark_types, delete_mark_type
from controllers.marklevel import create_mark_level, get_mark_levels, get_mark_level, delete_mark_level
from controllers.event import create_event, get_events, get_event
from controllers.marks import create_mark, get_marks
# config
data = config.CONFIG

#async_mode = 'eventlet'
app = Flask(__name__)
swagger = Swagger(app)
cors = CORS(app)
print('mongodb://' + data["mongo_host"] + ':' + str(data["mongo_port"]) + '/' + data["mongo_db"])
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + data["mongo_host"] + ':' + str(data["mongo_port"]) + '/' + data["mongo_db"]
}

app.config['CORS_HEADERS'] = 'Content-Type'

initialize_db(app)

# create a new activity
@app.route('/experiment/<string:experiment_id>/activities', methods=['POST'])
@cross_origin()
def add_activity_route(experiment_id):
    """
    Create a new activity
    This endpoint will create a new activity
    ---
    tags:
      - activities
    parameters:
      - name: experiment_id
        in: path
        type: string
        required: true
        description: The ID of the associated experiment
      - name: name
        in: formData
        type: string
        required: true
        description: The name of the activity
      - name: date
        in: formData
        type: string
        required: true
        description: The date of the activity
      - name: num_participants
        in: formData
        type: integer
        required: true
        description: The number of participants in the activity
      - name: comment
        in: formData
        type: string
        description: Optional comment for the activity
      - name: file_audio
        in: formData
        type: file
        required: false
        description: The audio file of the activity
      - name: file_video
        in: formData
        type: file
        required: false
        description: The video file of the activity
    responses:
      200:
        description: Activity created
      400:
        description: Error
    """
    return create_activity(experiment_id)

#get all activities
@app.route('/experiment/<string:experiment_id>/activities', methods=['GET'])
@cross_origin()
def get_activities_route(experiment_id):
    """
    Get all activities for a specific experiment
    This endpoint will return all activities associated with a given experiment
    ---
    tags:
      - activities
    parameters:
      - name: experiment_id
        in: path
        type: string
        required: true
        description: The ID of the experiment for which to get the activities
    responses:
      200:
        description: Activities
      404:
        description: Experiment not found
      400:
        description: Error
    """
    return get_activities(experiment_id)

#get an activity
@app.route('/activities/<string:name>', methods=['GET'])
@cross_origin()
def get_activity_route(name):
    """
    Get an activity
    This endpoint will return an activity
    ---
    tags:
      - activities
    responses:
      200:
        description: Activity
      400:
        description: Error
    """
    return get_activity(name)

@app.route('/activitiesById/<string:id_activity>', methods=['GET'])
@cross_origin()
def get_activity_by_id_route(id_activity):
    """
    Get an activity
    This endpoint will return an activity
    ---
    tags:
      - activities
    responses:
      200:
        description: Activity
      400:
        description: Error
    """
    return get_activity_by_id(id_activity)

#delete an activity
@app.route('/activities/<string:name>', methods=['DELETE'])
@cross_origin()
def delete_activity_route(name):
    """
    Delete an activity
    This endpoint will delete an activity
    ---
    tags:
      - activities
    responses:
        200:
            description: Activity deleted
        400:
            description: Error
        505:
            description: Error
        """
    return delete_activity(name)

#get an activity file
@app.route('/activities/<string:name>/<string:filename>', methods=['GET'])
@cross_origin()
def get_activity_file_route(name, filename):
    """
    Get an activity file
    This endpoint will return an activity file
    ---
    tags:
      - activities
    responses:
      200:
        description: Activity file
      400:
        description: Error
    """
    return get_activity_file(name, filename)

#create a new analysis
@app.route('/analysis', methods=['POST'])
@cross_origin()
def add_analysis_route():
    """
    Create a new analysis
    This endpoint will create a new analysis
    ---
    tags:

        - analysis
    parameters:
        - name: name    
            in: formData    
            type: string                            
            required: true
            description: The name of the analysis
    """
    return create_analysis()

#get all analysis
@app.route('/analysis', methods=['GET'])
@cross_origin()
def get_analysis_route():
    """
    Get all analysis
    This endpoint will return all analysis
    ---
    tags:
      - analysis
    responses:
      200:
        description: Analysis
      400:
        description: Error
    """
    return get_analysis()

#get an analysis
@app.route('/analysis/<string:id_analysis>', methods=['GET'])
@cross_origin()
def get_analysis_name_route(id_analysis):
    """
    Get an analysis
    This endpoint will return an analysis
    ---
    tags:
      - analysis
    parameters:
      - id_analysis: id of the analysis
    responses:
      200:
        description: Analysis
      400:
        description: Error
    """
    return get_analysis_by_id(id_analysis)

#delete an analysis
@app.route('/analysis/<string:name>', methods=['DELETE'])
@cross_origin()
def delete_analysis_route(name):
    """
    Delete an analysis
    This endpoint will delete an analysis
    ---
    tags:
      - analysis
    responses:
        200:
            description: Analysis deleted
        400:
            description: Error
        505:
            description: Error
        """
    return delete_analysis(name)

# get results
@app.route('/results', methods=['GET'])
@cross_origin()
def get_results_route():
    """
    Get results
    This endpoint will return results
    ---
    tags:
      - results
    responses:
      200:
        description: Results
      400:
        description: Error
    """
    return get_results()

# create a new indicator measure
@app.route('/indicator-measure/<string:indicator_name>', methods=['POST'])
@cross_origin()
def add_indicator_measure_route(indicator_name):
    """
    Create a new indicator measure
    This endpoint will create a new indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
    responses:
      200:
        description: Indicator measure created
      400:
        description: Error
    """
    return create_indicator_measure(indicator_name)

# get indicator measure by id analysis
@app.route('/indicator-measure/<string:indicator_name>/<string:id_analysis>', methods=['GET'])
@cross_origin()
def get_indicator_measure_route(indicator_name, id_analysis):
    """
    Get indicator measure
    This endpoint will return indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
      - id_analysis: id of the analysis
    responses:
      200:
        description: Indicator measure
      400:
        description: Error
    """
    return get_indicator_measure(indicator_name, id_analysis)

# download csv indicator measure by id analysis 
@app.route('/indicator-measure/<string:indicator_name>/<string:id_analysis>/csv', methods=['GET'])
@cross_origin()
def download_indicator_measure_csv_route(indicator_name, id_analysis):
    """
    Download csv indicator measure
    This endpoint will download csv indicator measure
    ---
    tags:
      - indicator-measure
    parameters:
      - indicator_name: name of the indicator
      - id_analysis: id of the analysis
    responses:
      200:
        description: Indicator measure csv
      400:
        description: Error
    """
    return download_indicator_measure_csv(indicator_name, id_analysis)

#Metedos HTTP para gestionar Experimentos
@app.route('/experiments', methods=['POST'])
@cross_origin()
def add_experiment_route():
    return create_experiment()

@app.route('/experiments', methods=['GET'])
@cross_origin()
def get_experiments_route():
    return get_experiments()

@app.route('/experiment/<string:code>', methods=['GET'])
@cross_origin()
def get_experiment_route(code):
    return get_experiment(code)

@app.route('/experimentID/<string:id_experiment>', methods=['GET'])
@cross_origin()
def get_experiment_by_id_route(id_experiment):
    return get_experiment_by_id(id_experiment)

@app.route('/experiment/<string:code>', methods=['DELETE'])
@cross_origin()
def delete_experiment_route(code):
    return delete_experiment(code)

@app.route('/experiment/<string:code>', methods=['PUT'])
@cross_origin()
def edit_experiment_route(code):
    return edit_experiment(code)

#Metedos HTTP para gestionar Tipos de Marcas
@app.route('/experiment/<string:id_experiment>/marktype', methods=['POST'])
@cross_origin()
def add_marktype_route(id_experiment):
    return create_mark_type(id_experiment)

@app.route('/marktype/<string:mark_type_id>', methods=['GET'])
@cross_origin()
def get_marktype_route(mark_type_id):
    return get_mark_type(mark_type_id)

@app.route('/experiment/<string:id_experiment>/marktypes', methods=['GET'])
@cross_origin()
def get_marktypes_route(id_experiment):
    return get_mark_types(id_experiment)

@app.route('/marktype/<string:mark_type_id>', methods=['DELETE'])
@cross_origin()
def delete_mark_type_route(mark_type_id):
    return delete_mark_type(mark_type_id)

#Metedos HTTP para gestionar Niveles de Marcas
@app.route('/marktype/<string:mark_type_id>/marklevel', methods=['POST'])
@cross_origin()
def add_marklevel_route(mark_type_id):
    return create_mark_level(mark_type_id)

@app.route('/marktype/<string:mark_type_id>/marklevel', methods=['GET'])
@cross_origin()
def get_marklevels_route(mark_type_id):
    return get_mark_levels(mark_type_id)

@app.route('/marklevel/<string:mark_level_id>', methods=['GET'])
@cross_origin()
def get_marklevel_route(mark_level_id):
    return get_mark_level(mark_level_id)

@app.route('/marklevel/<string:mark_level_id>', methods=['DELETE'])
@cross_origin()
def delete_mark_level_route(mark_level_id):
    return delete_mark_level(mark_level_id)

#Metedos HTTP para gestionar Eventos
@app.route('/activities/<string:activities_id>/event', methods=['POST'])
@cross_origin()
def add_event_route(activities_id):
    return create_event(activities_id)

@app.route('/activities/<string:activities_id>/events', methods=['GET'])
@cross_origin()
def get_events_route(activities_id):
    return get_events(activities_id)

@app.route('/event/<string:event_id>', methods=['GET'])
@cross_origin()
def get_event_route(event_id):
    return get_event(event_id)

#Metedos HTTP para gestionar Marcas
@app.route('/create_mark/<experiment_id>/<event_id>', methods=['POST'])
@cross_origin()
def add_mark_route(experiment_id,event_id):
    return create_mark(experiment_id,event_id)

@app.route('/get_marks/<experiment_id>/<event_id>', methods=['GET'])
@cross_origin()
def get_marks_route(experiment_id,event_id):
    return get_marks(experiment_id,event_id)

# run server
@app.route('/')
def hello():
    return 'server is running :)'

if __name__ == '__main__':
    app.run(debug=data["api_debug"], host=data["api_host"], port=data["api_port"])