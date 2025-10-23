#Contains functions to process video and generate list of detected objects and frame timestamps

import cv2
import numpy as np
from datetime import datetime, timedelta, timezone
from sentence_transformers import SentenceTransformer
from src.models import db, VideoModel, KeywordModel, VideoKeywordMapModel, keyword_does_not_exist
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import os

KEYFRAMES_FOLDER = 'keyframes'
if not os.path.exists(KEYFRAMES_FOLDER):
    os.makedirs(KEYFRAMES_FOLDER, exist_ok=True)

class VideoProcessor(object):
    #For embedding, load a pretrained Sentence Transformer model
    st_model = SentenceTransformer("all-MiniLM-L6-v2")
 
    def __init__(self, filename):
        self.filename = filename
        self.uri = filename.rsplit('.', 1)[0].rsplit('\\', 1)[1]
        self.cap = cv2.VideoCapture(filename)

        self.created_time = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        self.ts_detections_dict = {}
        self.keyframes_path = os.path.join(KEYFRAMES_FOLDER, f'{self.uri}')
        if not os.path.exists(self.keyframes_path):
            os.makedirs(self.keyframes_path, exist_ok=True)

        if keyword_does_not_exist(self.uri): #Add new keyword-vector entry for the filename if it doesn't exist
            embedding = self.keyword_vector(self.uri)
            newrow = KeywordModel(word = self.uri, vector = embedding, created = self.created_time)
            db.session.add(newrow)
            db.session.commit()
    
    #method for embedding vectors. Made public so that I can call this manually if required
    def keyword_vector(self, keyword):
        embeddings = [keyword]
        result = self.st_model.encode(embeddings)
        return result[0]
    
    #method for adding video to database. Might consider calling this on __init__ since videos should be added if they're going to be processed
    def add_video(self):
        new_video = VideoModel(filename = self.filename, created = self.created_time, uri = self.uri)
        try:
            db.session.add(new_video)
            db.session.commit()
        except IntegrityError:
            print("Something went wrong, integrity error raised. Video may already exist")
            db.session.rollback()


class MobileNetProcessor(VideoProcessor):
    #Object Detection network
    classNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

    #Hardcoded network files :/
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")

    #return array of detected objects in a list of strings. Takes in threshold confidence as an arg
    #This function also adds any newly detected objects to the embedded vectors database
    def detect_objects_in_frame(self, frame, confidence_threshold : float = 0.5, frame_number : int = 0):

        detected_objects_list = []

        # Perform object detection on the frame
        # Get frame dimensions
        # (For drawing bounding box)
        (h, w) = frame.shape[:2]

        # Preprocess the frame for the MobileNet model
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # Set the input to the network and perform a forward pass
        self.net.setInput(blob)
        detections = self.net.forward()

        # Loop over the detections
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections by ensuring the confidence is greater than a minimum threshold
            if confidence > confidence_threshold: # Adjust confidence threshold as needed
                # Extract the index of the class label and the bounding box coordinates
                idx = int(detections[0, 0, i, 1])

                #Info for drawing bounding boxes and labels 
                #Might use for highlighting stuff later... Commented out for now
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, self.classNames[idx], (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Add the className to the list of detected objects associated with the frame_timestamp
                detected_objects_list.append(self.classNames[idx])

                # Check if the keyword already exists within the table
                # (Not sure if this is the best place to do the check but i'll leave it here for now)
                if keyword_does_not_exist(self.classNames[idx]): #Add new keyword-vector entry if it doesn't exist
                    embedding = self.keyword_vector(self.classNames[idx])
                    newrow = KeywordModel(word = self.classNames[idx], vector = embedding, created = self.created_time)
                    db.session.add(newrow)
                    db.session.commit()
                else:
                    pass

        #save image to keyframes folder
        cv2.imwrite(os.path.join(self.keyframes_path, f'{frame_number}.jpg'), frame)
        
        return detected_objects_list

    #Generate dictionary where keys are interesting frames and values are lists of detected objects
    def get_framets_keyword_dict(self, histogram_threshold : float = 0.999):
        current_frame = 0
        self.ts_detections_dict = {}

        #Setup initial histogram

        incoming_data, frame = self.cap.read()
        previous_histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        previous_histogram = cv2.normalize(previous_histogram, previous_histogram).flatten()

        last_scene_change = 0
        saved_frames = 0

        while True:
            incoming_data, frame = self.cap.read()
            #break loop once no more incoming data, i.e. reached the end of the file
            if not incoming_data:
                break
            
            
            current_frame += 1
            histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            histogram = cv2.normalize(histogram, histogram).flatten()

            #Get similarity score between histograms which indicates whether there was a significant change between frames
            d = cv2.compareHist(previous_histogram, histogram, cv2.HISTCMP_CORREL)
            current_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            #It looks like since most of the sample vids i found have stationary camera POVs, the histogram match between frames
            #is usually pretty high, so I have to set d relly high to get any practical value
            if d < histogram_threshold and (current_time - last_scene_change >= 1 or last_scene_change == 0):

                #Get frame timestamp
                frame_ts = timedelta(seconds=int(current_time * 100)/100)

                #perform object detection on the frame and assign list of objects to key frame in the timestamp dictionary, and save frame to folder
                self.ts_detections_dict[frame_ts] = self.detect_objects_in_frame(frame, 0.5, saved_frames)
                saved_frames += 1

            previous_histogram = histogram

        return self.ts_detections_dict

    #iterate through frame_ts to object detections dict to add mappings to the database table
    def process(self):

        for frame_timestamp in self.ts_detections_dict.keys():
            for keyword in self.ts_detections_dict[frame_timestamp]:

                #To map: Add video_id, keyword_id, frame timestamp of associated keyword and created timestamp as new entries
                #video_id and created timestamp remains the same throughout. ts_detections_dict can be iterated through for adding
                #keyword_id and frame_ts 

                v_id = db.session.execute(db.select(VideoModel).order_by(desc(VideoModel.rowid))).scalars().first().rowid
                k_id = db.session.execute(db.select(KeywordModel).where(KeywordModel.word == keyword)).scalars().first().id
                mapping_new_row = VideoKeywordMapModel(video_id = v_id, keyword_id = k_id, frame_ts = f"{frame_timestamp}", created = self.created_time)
                db.session.add(mapping_new_row)
                db.session.commit()


if __name__ == "__main__":

    pass