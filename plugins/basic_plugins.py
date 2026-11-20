# plugin rules (just 3, chill)
# 1. only functions with @plugin can be called with send
# 2. one argument only: send name "arg"
# 3. return True/False if you catch it with bet (as a plain
#    `send name "arg"` line, the return value doesn't matter)

from plugin_api import plugin
import os

# prints the message and hands back True
@plugin
def notify(msg):
    print("notification:" + msg)
    return True

# True if the file exists, False if not
@plugin
def check_file(path):
    return os.path.exists(path)