import eel
import shell
import sys

sys_arguments = sys.argv[1:]
if "-shell" in sys_arguments or "-s" in sys_arguments:
    shell.run()

else:
    FILENAME = "examples/example.eel"
    _, error = eel.run(FILENAME, open(FILENAME).read())
    if error:
        print(error.as_string())
