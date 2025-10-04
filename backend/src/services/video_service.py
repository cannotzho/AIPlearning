


#Contains functions to process video and generate list of detected objects and frame timestamps

import cv2
import numpy as np
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from src.models import db, VideoModel, KeywordModel, VideoKeywordMapModel

#Input video path/filename
filename = "GuyBicycle.mp4"


class VideoProcessor(object):
    #For embedding, load a pretrained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
 
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        self.created_time = str(datetime.utcnow())
        self.ts_detections_dict = {}
    pass

class MobileNetProcessor(VideoProcessor):
    #Object Detection network
    classNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")

    def detect_objects_in_frame(self, frame, confidence_threshold : float = 0.5): #return array of detected objects in a list of strings. Takes in threshold confidence as an arg
        detected_objects_list = []
        #do stuff
        #perform object detection on the frame
            # Get frame dimensions
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

                #Keep box info for highlighting stuff later...
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                # Add the className to the list of detected objects associated with the frame_timestamp
                detected_objects_list.append(self.classNames[idx])

                # Check if the keyword already exists within the table 

        return detected_objects_list

    def get_framets_keyword_dict(self, histogram_threshold = 0.999):
        # self.cap = cv2.VideoCapture(filename)

        current_frame = 0
        self.ts_detections_dict = {}

        #Setup initial histogram

        incoming_data, frame = self.cap.read()
        previous_histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        previous_histogram = cv2.normalize(previous_histogram, previous_histogram).flatten()

        last_scene_change = 0

        while True:
            incoming_data, frame = self.cap.read()
            if not incoming_data:
                break

            current_frame += 1
            histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            histogram = cv2.normalize(histogram, histogram).flatten()

            d = cv2.compareHist(previous_histogram, histogram, cv2.HISTCMP_CORREL)
            current_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            #It looks like since most of the sample vids i found have stationary camera POVs, the histogram match between frames
            #is usually pretty high, so I have to set d relly high to get any practical value
            if d < histogram_threshold and (current_time - last_scene_change >= 1 or last_scene_change == 0):

                #Get frame timestamp
                frame_ts = str(timedelta(seconds=current_time))
                last_scene_change = current_time

                #perform object detection on the frame and assign list of objects to key frame in the timestamp dictionary
                self.ts_detections_dict[frame_ts] = self.detect_objects_in_frame(frame, 0.5)

            previous_histogram = histogram

        return self.ts_detections_dict

    def writeToDB():
        pass

    
    def process():
        pass

if __name__ == "__main__":
    #Run process on sample video
    
    pass