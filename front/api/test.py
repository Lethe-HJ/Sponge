from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

a_language = api.model('language', {
    'language': fields.String('TheLanguage'),
    'id': fields.Integer('ID')
})

languages = list()
python = {'language': 'python', 'id': 1}
languages.append(python)

@api.route('/language')
class language(Resource):
    @api.marshal_with(a_language, envelope='data') # envelope在这里
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        new_language = api.payload
        new_language['id'] = len(languages) + 1
        languages.append(new_language)
        return {'result': 'language added'}, 201

if __name__ == '__main__':
    app.run(debug=True)