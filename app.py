from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Video(db.Model):
    #video file name, detected objects, frame timestamps, and created timestamp
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(60), nullable = False)
    #detected_objects = db.Column(db.list of strings)
    #frame_ts = db.Column(db.float?)
    #created_ts = db.Column(db.DateTime, default = datetime.utcnow) <-- assuming this is the date the db entry was made
    def __repr__(self):
        return '<%r>' % self.id

#Setup index
@app.route('/', methods = ['POST','GET'])
def index(self):
    return "Hi"
#Setup endpoints as per task

#Returns the status of the service
@app.route('/health', methods = ['GET'])
def health(self):
    return ''

#Accepts video files, performs key frame extraction, object detection, and saves results in database.
@app.route('/process', methods = ['POST'])
def process(self):
    pass

#Retrieves all processed videos from the database.
@app.route('/videos', methods = ['GET'])
def videos(self):
    pass

#Performs a full-text search on video summaries based on detected objects or video file name.
@app.route('/search', methods = ['GET'])
def search(self):
    pass

if __name__ == "__main__":
    app.run(Debug = True)