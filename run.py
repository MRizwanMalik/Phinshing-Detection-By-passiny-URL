import threading
from app import run_flask_app
from fyp import app as dash_app
from flask import Flask

def run_dash_and_flask():
    
    def run_dash():
        dash_app.run_server(debug=False)

   
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    
    run_flask_app()

   
    dash_thread.join()

if __name__ == '__main__':
    run_dash_and_flask()
