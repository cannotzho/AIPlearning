from flask import Blueprint, render_template, redirect, make_response, request, jsonify, send_file
from flask_restful import Resource, Api, reqparse
from src.models import db, VideoModel, KeywordModel, VideoKeywordMapModel
from src.schemas.video_schema import VideoSchema
from src.services.video_service import MobileNetProcessor
from src.services.search_service import SearchHandler
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads' # Define your upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

KEYFRAMES_FOLDER = 'keyframes'
if not os.path.exists(KEYFRAMES_FOLDER):
    os.makedirs(KEYFRAMES_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Start API server, add endpoints and load the DB
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


@api_bp.route('/')
def index():
    headers = {'Content-Type': 'text/html'}
    response = make_response(render_template("index.html", status = "Unknown"), 200, headers)
    return response

#Setup endpoints as per task

#Returns the status of the service
@api_bp.route('/health', methods = ['GET'])
def health():
    #Run service to check on dependencies, database connectivity, and resource availability
    #nvm, it doesn't need to be so complicated
    headers = {'Content-Type': 'text/html'}
    response = make_response(jsonify("Backend is live"), 200, headers)
    return response

#Accepts video files, performs key frame extraction, object detection, and saves results in database.
#Try to keep endpoints resourceful
class ProcessedVideo(Resource):

    def post(self):
        args = reqparse.RequestParser()
        args.add_argument('video', location = 'files', type = FileStorage, required = True, help = "File cannot be blank")

        video_args = args.parse_args()

        video_file = video_args['video']
        # Securely save the file
        filename = secure_filename(video_file.filename)

        if '.' in filename and filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return redirect('/', 415, {'message': 'File type not allowed'})
        
        filename = os.path.join(UPLOAD_FOLDER, filename)
        counter = 0
        while os.path.exists(filename):
            counter += 1
            filename = filename.rsplit('.', 1)[0] + f" ({counter})." + filename.rsplit('.', 1)[1].lower()
        
        video_file.save(filename)
        
        #Create VideoProcessor object to perform processing functions
        #Subclass determines object detection implementation
        processor = MobileNetProcessor(filename)

        #Immediately try adding video to the video table in database
        processor.add_video()

        #Generate frame_ts to detected objects dictionary with default threshold values for histogram
        #This also runs object detection and automatically adds new keywords
        processor.get_framets_keyword_dict()

        #add video-keyword mappings

        processor.process()

        return redirect('/')

api.add_resource(ProcessedVideo, '/process')

#Retrieves all processed videos from the database.
class Videos(Resource):
    def get(self):
        videos = db.session.execute(db.select(VideoModel).order_by(VideoModel.created)).scalars()
        
        video_schema = VideoSchema()
        serialized_list = []
        for video in videos:
            serialized_list.append(video_schema.dump(video))
        
        headers = {'Content-Type': 'application/json'}
        response = make_response(jsonify(serialized_list), 200, headers)
        
        return response
    
api.add_resource(Videos, '/videos/')

#Retrieves singular video, for displaying drawn keyframes and detected objects
class Video(Resource):
    def get(self, v_id):
        self.v_id = v_id
        video : VideoModel = db.session.execute(db.select(VideoModel).where(VideoModel.rowid == self.v_id)).scalars().first()
        if video == None:
            return "Video not found in database", 404
        file_path = os.path.join(UPLOAD_FOLDER, f'{video.uri}.mp4')

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({"detail": "Video not found in uploads",}), 404
        
    def delete(self, v_id):
        self.v_id = v_id
        video : VideoModel = db.session.execute(db.select(VideoModel).where(VideoModel.rowid == self.v_id)).scalars().first()
        file_path = os.path.join(UPLOAD_FOLDER, f'{video.uri}.mp4')
        if os.path.exists(file_path):
            db.session.delete(video)
            associations : VideoKeywordMapModel = db.session.execute(db.select(VideoKeywordMapModel).where(VideoKeywordMapModel.video_id == self.v_id)).scalars()
            db.session.delete(associations)
            db.session.commit()
            os.remove(file_path)
            return redirect('/',"Video deleted", 204)
        
        else:
            return redirect('/', 404)
 
api.add_resource(Video, '/videos/<int:v_id>')

#Retrieve list of keyframe timestamps with video id
class Keyframes(Resource):
    def get(self, v_id):
        self.v_id = v_id
        datarows : list[VideoKeywordMapModel] = db.session.execute(db.select(VideoKeywordMapModel).where(VideoKeywordMapModel.video_id == self.v_id)).scalars()

        serialized_list = []
        for row in datarows:
            serialized_list.append(row.frame_ts)

        serialized_list = list(set(serialized_list))
        headers = {'Content-Type': 'application/json'}
        response = make_response(jsonify(serialized_list), 200, headers)
        
        return response
    
api.add_resource(Keyframes, '/keyframes/<int:v_id>')    

#Retrieve keyframe image from video
class Keyframe(Resource):
    def get(self, filename, frame_number):
        try:
            return send_file(os.path.join(KEYFRAMES_FOLDER, f'{filename}/{frame_number}.jpg'))
        except:
            return "File not found", 404
    
api.add_resource(Keyframe, '/keyframes/<string:filename>/<int:frame_number>')

#Test endpoint for viewing keyword-vector tables
class Keywords(Resource):
    def get(self):
        keywords = db.paginate(db.select(KeywordModel).order_by(KeywordModel.id))
        headers = {'Content-Type': 'text/html'}
        response = make_response(render_template("keywords.html", keywords = keywords), 200, headers)
        return response
    
api.add_resource(Keywords, '/keywords/')

#Performs a full-text search on video summaries based on detected objects or video file name.
class SearchResult(Resource):
    def get(self):
        search_query, search_type = request.args.get('query'), request.args.get('search_type')
        search_handler = SearchHandler()
        if search_query == "":
            videos = db.session.execute(db.select(VideoModel).order_by(VideoModel.created)).scalars()
            
            video_schema = VideoSchema()
            serialized_list = []
            for video in videos:
                serialized_list.append(video_schema.dump(video))
            
            headers = {'Content-Type': 'application/json'}
            response = make_response(jsonify(serialized_list), 200, headers)
            
            return response
        
        result = search_handler.process_search_results(query=search_query, search_type=search_type)
        video_schema = VideoSchema()
        serialized_list = []
        for video in result:
            serialized_list.append(video_schema.dump(video))
        headers = {'Content-Type': 'application/json'}
        response = make_response(serialized_list, 200, headers)
        return response
    
api.add_resource(SearchResult, '/search/')
