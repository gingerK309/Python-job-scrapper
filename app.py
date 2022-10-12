from flask import Flask

def create_app():
  app = Flask(__name__)
  app.jinja_env.add_extension('jinja2.ext.loopcontrols')
  import pages
  app.register_blueprint(pages.bp)
  return app