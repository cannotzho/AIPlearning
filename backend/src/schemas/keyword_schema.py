from flask_restful import fields

keywordFields = {
    'id': fields.Integer,
    'word':fields.String,
    'vector':fields.String,
    'created':fields.DateTime
}