from app.views import app, scheduler
from app.lib.log_handle import Log

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler._logger = Log()
    scheduler.start()
    app.run(use_reloader=False, threaded=True, port=80, host='0.0.0.0', debug=True)
