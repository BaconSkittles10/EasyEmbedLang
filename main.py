import eel


FILENAME = "graphics_test.eel"
_, error = eel.run(FILENAME, open(FILENAME).read())
if error:
    print(error.as_string())
