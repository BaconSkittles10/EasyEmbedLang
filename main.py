import eel


FILENAME = "example.eel"
_, error = eel.run(FILENAME, open(FILENAME).read())
if error:
    print(error.as_string())
