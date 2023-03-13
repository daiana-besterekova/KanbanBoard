import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import db
    from . import db
    db.init_app(app)

    # import the auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # point to the index page when / is opened
    from . import task
    app.register_blueprint(task.bp)
    app.add_url_rule('/', endpoint='index')

    return app
