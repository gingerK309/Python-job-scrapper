from flask import Flask

app = Flask(__name__)
import pages
app.register_blueprint(pages.bp)

if __name__ == "__main__":
  app.run()