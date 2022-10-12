from flask import Flask

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
import pages
app.register_blueprint(pages.bp)

if __name__ == "__main__":
  app.run()