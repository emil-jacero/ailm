from app import api
from rest_api import Release

#api.add_resource(HelloWorld, '/hello', '/world')
#api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo_ep')
api.add_resource(Release, '/api/v1/release/')