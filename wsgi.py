
import os

print(os.getcwd())
print(os.listdir())


from webapp.routes import application


if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8080, debug=True)