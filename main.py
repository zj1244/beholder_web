from app.views import app, scheduler
from app.lib.log_handle import Log

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler._logger = Log()
    scheduler.start()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(use_reloader=False, threaded=True, port=8000, host='0.0.0.0', debug=True)
