from flask_restful import fields

videoFields = {
    'id': fields.Integer,
    'file': fields.Raw,
    'filename':fields.String,
    'uri':fields.String,
    'created':fields.DateTime
}
