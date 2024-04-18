from flask import Flask
import views
import flask_socketio

app = Flask(__name__)
socketio = flask_socketio.SocketIO(app)
app.register_blueprint(views.views, url_prefix="/views")
# do /views/ if you want to see the views.py content when you run it


@socketio.on('get_info')
def update_info():
    socketio.emit(
        'send_info', {'time': views.get_time(), 'occupancy': views.get_occupancy()})


if __name__ == '__main__':
    socketio.run(app=app,
                 host="0.0.0.0",
                 port=8000,
                 use_reloader=False,
                 log_output=True,
                 debug=False)
