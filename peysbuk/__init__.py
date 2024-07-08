# peysbuk/__init__.py

from flask import Flask, render_template

def createApp():
    app = Flask(__name__)
    app.secret_key = 'Lorem Ipsum Loror Sit Emit'
    
    from .views import view
    app.register_blueprint(view, url_prefix='/')
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    return app
