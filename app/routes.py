from app import api
from main import HelloWorld, Todo

api.add_resource(HelloWorld, '/hello', '/world')
api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo_ep')