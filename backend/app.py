from flask import Flask, render_template, redirect
from sqlalchemy_utils import database_exists
from src.routes import api_bp
from src.models import db, KeywordModel, VideoModel, VideoKeywordMapModel
import os

UPLOADS_FOLDER = 'uploads'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///processed_videos.db'

db.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')

if not database_exists('sqlite:///instance/processed_videos.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/reset_all', methods = ['POST', 'GET'])
def reset_all():
    #delete all video entries and video files in uploads folder
    #Route currently used for testing only
    db.session.query(VideoModel).delete()
    db.session.query(KeywordModel).delete()
    db.session.query(VideoKeywordMapModel).delete()
    db.session.commit()
    try:
        for filename in os.listdir(UPLOADS_FOLDER):
            file_path = os.path.join(UPLOADS_FOLDER, filename)
            if os.path.isfile(file_path):  # Check if it's a file, not a subdirectory
                os.remove(file_path)
        print(f"All files in '{UPLOADS_FOLDER}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting files in '{UPLOADS_FOLDER}': {e}")
    return redirect('/api/videos/')

if __name__ == "__main__":
    app.run(debug = True)