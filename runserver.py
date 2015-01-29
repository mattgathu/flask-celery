"""
Run Flask's bundled web server

"""
from flascelery import app

if __name__ == '__main__':
    app.run(debug=True)
