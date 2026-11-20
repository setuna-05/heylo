from plugin_loader import load_plugins
from tokens import tokenize,expand_yoink
from errors import MiniError,show_error
from runner import run
import sys
import os

if len(sys.argv) < 2:
    print("an intro with no title? amateur hour. give me a filename")
    sys.exit()
else:
    try:
        with open(sys.argv[1],"r",encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        print("handing me a 404? bold move. go recheck the name")
        sys.exit()

try:
    plugins = load_plugins()
    if not data.endswith("\n"):
        data += "\n"
    tokens = tokenize(data,sys.argv[1])
    main_path = os.path.abspath(sys.argv[1])
    done = [main_path]
    tokens = expand_yoink(tokens,[main_path],done,os.path.dirname(main_path))
    run(tokens,plugins)
except MiniError as e:
    show_error(e)