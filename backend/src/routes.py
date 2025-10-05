from flask import Blueprint, render_template, redirect, make_response
from flask_restful import Resource, Api, reqparse
from src.models import db, VideoModel, KeywordModel, VideoKeywordMapModel
from src.services.video_service import MobileNetProcessor
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads' # Define your upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Start API server, add endpoints and load the DB
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

video_args = reqparse.RequestParser()
video_args.add_argument('video', location = 'files', type = FileStorage, required = True, help = "File cannot be blank")

@api_bp.route('/')
def index():
    headers = {'Content-Type': 'text/html'}
    response = make_response(render_template("index.html", status = "Unknown"), 200, headers)
    return response

#Setup endpoints as per task

#Returns the status of the service
@api_bp.route('/health', methods = ['GET'])
def health(self, status):
    self.status = status
    #Run service to check on dependencies, database connectivity, and resource availability
    headers = {'Content-Type': 'text/html'}
    response = make_response(render_template("index.html", status = self.status), 200, headers)
    return response

#Accepts video files, performs key frame extraction, object detection, and saves results in database.
#Try to keep endpoints resourceful
class ProcessedVideo(Resource):

    # @marshal_with(video_schema.videoFields)
    def post(self):
        args = video_args.parse_args()

        video_file = args['video']
        # Securely save the file
        filename = secure_filename(video_file.filename)

        if '.' in filename and filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return {'message': 'File type not allowed'}, 400
        
        filename = os.path.join(UPLOAD_FOLDER, filename)
        # if os.path.exists(filename):
        #     return {'message': f'A file already exists at the following path "{filename}"'}, 409
        
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

        return redirect('/api/videos/')

api.add_resource(ProcessedVideo, '/process')

#Retrieves all processed videos from the database.
class Videos(Resource):
    def get(self):
        videos = db.paginate(db.select(VideoModel).order_by(VideoModel.created))
        headers = {'Content-Type': 'text/html'}
        response = make_response(render_template("videos.html", videos = videos), 200, headers)
        return response
    
api.add_resource(Videos, '/videos/')

#Retrieves singular video, for displaying drawn keyframes and detected objects
class Video(Resource):
    def get(self, v_id):
        self.v_id = v_id
        video = db.session.execute(db.select(VideoModel).where(VideoModel.rowid == self.v_id)).scalars().first()
        headers = {'Content-Type': 'text/html'}
        response = make_response(render_template("video.html", video = video), 200, headers)
        return response
    
api.add_resource(Video, '/videos/<int:v_id>')

#Performs a full-text search on video summaries based on detected objects or video file name.
@api_bp.route('/search', methods = ['GET'])
def search(self):
    pass