from flask_sqlalchemy import SQLAlchemy
from pgvector.sqlalchemy import Vector

db = SQLAlchemy()

#Model data structure for keyword row
#Contains id, word, vector, created

class KeywordModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(50), unique = True, nullable = False)
    vector = db.Column(Vector(384), unique = True, nullable = False)
    created = db.Column(db.DateTime, unique = False, nullable = False)
    association = db.relationship('VideoKeywordMapModel', backref = 'keyword')
    
    def __repr__(self):
        return f"Keyword(id = {self.id}, word = {self.word}, created = {self.created})"
    

#Model data structure for video row
#Contains id, filename, uri, created

class VideoModel(db.Model):
    rowid = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(60), unique = True, nullable = False)
    uri = db.Column(db.String(50), unique = False)
    created = db.Column(db.DateTime, unique = False, nullable = False)
    association = db.relationship('VideoKeywordMapModel', backref = 'video')

    def __repr__(self):
        return f"Video(id = {self.rowid}, filename = {self.filename}, created = {self.created})"
    
    
#Model data structure for video-keyword map row
#Contains id, video id, keyword id, frame timestamp, created

class VideoKeywordMapModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_model.rowid'))
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword_model.id'))
    frame_ts = db.Column(db.String(10), unique = False, nullable = False)
    created = db.Column(db.DateTime, unique = False, nullable = False)

    def __repr__(self):
        return f"MapEntry(video_id = {self.video_id}, keyword_id = {self.keyword_id}, frame_ts = {self.frame_ts}, created = {self.created})"
    

# def add_keyword(keyword):
#         try:
#             db.session.add()
#             db.session.commit()
#         except (IntegrityError):
#             db.session.rollback()
#             print("Entry already exists")
#             return False
        
def keyword_does_not_exist(keyword):
    return db.session.execute(db.select(KeywordModel).where(KeywordModel.word == keyword)).first() is None