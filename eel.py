import eel
import sys

print(sys.argv)
eel.run(sys.argv[1], open(sys.argv[1]).read())
