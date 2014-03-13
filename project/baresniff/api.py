from flask.ext import restful

api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}
        
    api.add_resource(HelloWorld, '/')

    if __name__ == '__main__':
        app.run(debug=True)