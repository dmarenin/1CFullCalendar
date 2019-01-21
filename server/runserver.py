from server import app

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 13000

    app.run(HOST, PORT, threaded=True) 

