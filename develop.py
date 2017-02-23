from project import create_app
from project.config import DevelopmentConfig


application = create_app(DevelopmentConfig)


if __name__ == "__main__":
    application.run(port=5000, host="0.0.0.0", threaded=True)
