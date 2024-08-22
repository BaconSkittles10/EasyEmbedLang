import eel
import shell
import sys

if "-s" in sys.argv or "-shell" in sys.argv:
    shell.run()

else:
    FILENAME = "examples/example.eel"
    _, error = eel.run(FILENAME, open(FILENAME).read())
    if error:
        print(error.as_string())
