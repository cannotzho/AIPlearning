
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KDTree, BallTree
import numpy as np
from src.models import db, VideoModel, KeywordModel, VideoKeywordMapModel
from sqlalchemy import func


class SearchHandler(object):
    #Initiate transformer to encode queries
    st_model = SentenceTransformer("all-MiniLM-L6-v2")

    #There should be a check here if the sentence transformer can't load, then it needs to eventually return a message to the frontend server to indicate the service is down

    def __init__(self):
        #Initialize np array from keyword database
        self.Corpus = np.array(db.session.execute(db.select(KeywordModel.vector).order_by(KeywordModel.id)).scalars().all())
        self.kdt = KDTree(self.Corpus, leaf_size=2, metric='euclidean')
        
    #Test function for checking embedded vector space
    def _corpus(self):
        print(self.Corpus)

    #Returns a list of closest neighboring indices pointing to the associated keyword.
    #Indices must +1 before being used in keyword table as ids start at 1
    def get_sentence_ann(self, search_query, k : int = 1):
        search_query = [str(search_query)]
        #encode search_query
        embedded_vector = self.st_model.encode(search_query)
        result = self.kdt.query(embedded_vector, k=k, return_distance=False)
        return result

    def get_word_ann(self, search_query, k : int = 1):
        
        words = search_query.split(' ')
        #encode search_query
        embedded_vectors = self.st_model.encode(words)
        result = self.kdt.query(embedded_vectors, k=k, return_distance=False)
        return result

    #Function made for testing VSS is working as intended
    def get_keyword_from_index(self, keyword_indices):
        suggested_keywords = []
        for i in keyword_indices:
            #ids in keyword table start at 1, so need to +1
            keyword_row = db.session.execute(db.select(KeywordModel).where(KeywordModel.id == int(i + 1))).scalars().first()
            suggested_keywords.append(keyword_row)

        return suggested_keywords
    
    def get_suggested_keywords(self, search):
        indices = self.get_sentence_ann(search)
        return self.get_keyword_from_index(indices)
    
    #Function to get videos from keyword ids using the map.
    #Returns a list of VideoModel objects
    def get_associated_videos_from_keywords(self, keyword_indices : list[int]):
        associated_videos = []
        #For each keyword, get all videos associated with that keyword via the map
        for keyword_id in keyword_indices[0]:
            associations = db.session.execute(db.select(VideoKeywordMapModel).where(VideoKeywordMapModel.keyword_id == int(keyword_id + 1))).scalars().unique(self.get_unique_video).all()
            for row in associations:
                associated_videos.append(row.video)
        return associated_videos
    
    def get_associated_videos_from_filename(self, filename_indices : list[int]):
        associated_videos = []
        #For each keyword, get all videos associated with that keyword via the map
        for index in filename_indices[0]:
            filename = db.session.execute(db.select(KeywordModel).where(KeywordModel.id == int(index + 1))).scalars().first().word
            associated_vid = db.session.execute(db.select(VideoModel).where(VideoModel.uri == filename)).scalars().first()
            if associated_vid != None:
                associated_videos.append(associated_vid)

        return associated_videos
    
    #Callable for compressing association results into unique video rows
    def get_unique_video(self, map_row):
        return map_row.video
    
    def process_search_results(self, query, search_type: int):

        #search by detected objects
        if int(search_type):
            keyword_indices = self.get_sentence_ann(query)
            associated_videos = self.get_associated_videos_from_keywords(keyword_indices)
        
        #search by filenames
        else:
            keyword_indices = self.get_sentence_ann(query, k =3)
            associated_videos = self.get_associated_videos_from_filename(keyword_indices)

        return associated_videos

    #Test function for checking database    
    def display_associations(self):
        print(db.session.execute(db.select(VideoKeywordMapModel)).scalars().all())