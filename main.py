from flask import Flask

my_app = Flask(__name__)


@my_app.route('/')
def home_page():
    return f"Hello, Word! Hello, Flask! "


@my_app.route('/user/<name>')
def user_name(name):
    return f"Hello, {name}! Wellcome into Flask! "


if __name__ == "__main__":
    my_app.run(debug=True)
