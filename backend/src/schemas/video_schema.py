from src.schemas import ma
from marshmallow import fields
from src.models import VideoModel

class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VideoModel
        load_instance = True 