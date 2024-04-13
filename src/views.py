from flask import Blueprint, render_template
import threading
from ai import ai
from datetime import datetime

views = Blueprint(__name__, "views")

neural_network = ai.AI()
threading.Thread(target=neural_network.ai_stuff).start()

def get_time():
  return datetime.now().strftime('%I:%M:%S %p')

def get_occupancy():
  return neural_network.get_occupancy()

@views.route("/")
def home():
  return render_template("index.html",
                         time=get_time(),
                         current_occupancy=get_occupancy())
