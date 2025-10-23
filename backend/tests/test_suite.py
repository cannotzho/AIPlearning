from app import app
import requests
import pytest
import os
from src.schemas.video_schema import VideoSchema
from src.services.video_service import MobileNetProcessor
from src.models import db
from marshmallow import ValidationError
import cv2

# Assuming your API is running locally on port 5000
BASE_URL = "http://localhost:5000/api"
TEST_VIDEO = "tests\\CowBalls.mp4"
TEST_IMAGE = "tests\\dog_test.jpg"
UPLOADS = "uploads"

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///processed_videos.db'
# db.init_app(app)
# with app.app_context():
#     db.create_all()

def test_frame_extraction(): #Test frame extraction logic
    #for this implementation, pass in get_framets_keyword_dict from service
    
    expected_result = [1, 2, 2, 3, 4, 5, 9]
    with app.app_context():
        processor = MobileNetProcessor(TEST_VIDEO)
        processor.get_framets_keyword_dict()

        actual_result = processor.ts_detections_dict.keys()

        assert len(actual_result) == len(expected_result)

        for i, frame_ts in enumerate(actual_result):
            assert abs(frame_ts.total_seconds() - expected_result[i]) < 2 #if identified timestamp is more than 2 seconds away from expected result of detected scene change, fail the test

def test_object_detection(): #Test object detection accuracy

    image = cv2.imread(TEST_IMAGE)

    expected_result = "dog"

    with app.app_context():
        processor = MobileNetProcessor(TEST_VIDEO)

        detected_objects = processor.detect_objects_in_frame(image, 0.5)

        assert expected_result in detected_objects

def test_get_videos(): #Testing /videos
    """
    Tests data validity of videos endpoint
    """
    response = requests.get(f"{BASE_URL}/videos")
    assert response.status_code == 200
    video_schema = VideoSchema()

    try:
    # Load and validate the data
        validated_data = video_schema.load(response)
        assert validated_data
    except ValidationError as err:
        assert err.messages

def test_get_video_not_found(): #Testing /videos/<int: id>
    """
    Tests retrieval of a non-existent video.
    """
    response = requests.get(f"{BASE_URL}/videos/1000")
    assert response.status_code == 404

def test_post_video_success(): #Testing /process
    """
    Tests successful upload of video
    """
    file_path = TEST_VIDEO
    with open(file_path, 'rb') as f:
        files = {'video': (os.path.basename(file_path), f, 'video/mp4')}
        response = requests.post(f"{BASE_URL}/process", files=files, data = {})

    assert response.status_code == 200

def test_get_health(): #Test /health
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
