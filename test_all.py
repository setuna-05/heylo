import subprocess
import os

TESTS = [
    {"name": "missing fin",
     "code": """sus based
  lol "a"
""",
     "expected": """a
[main.helo line 1] you ran it all and there's no finish line?! add the fin"""
    },
    {"name": "full program",
     "code": """bet a = 0
bet ok = yeet "echo hi"
spam a < 3
  sus a == 1
    lol "one"
  idk
    lol a
  fin
  bet a = a + 1
fin
sus ok fam no cringe
  lol "success"
fin
lol 2 * 3 + 4 / 2
""",
     "expected": """hi
0
one
2
success
8.0"""
    },
    {"name": "missing ship",
     "code": """vibe f
  lol "1"
  lol "2"
  lol "3"
fin
bet r = send f
lol r
""",
     "expected": """1
2
3
[main.helo line 6] nothing to ship but vibes. go write the ship, i'll wait"""
    },
    {"name": "error inside vibe with route",
     "code": """vibe f x
  lol x + 1
fin
lol "start"
send f "a"
""",
     "expected": """start
[main.helo line 2] this ain't a smoothie. match your types
word from the send on line 5"""
    },
    {"name": "ship return value",
     "code": """vibe double x
  ship x * 2
fin
bet r = send double 4
lol r
""",
     "expected": """8"""
    },
    {"name": "recursion limit with route",
     "code": """vibe loop x
  ship send loop x
fin
bet r = send loop 1
lol r
""",
     "expected": """[main.helo line 2] too many loops, bro. i'm out before the labor board calls
word from the send on line 2 (x98)
word from the send on line 4"""
    },
    {"name": "small expressions",
     "code": """lol 1 + 2
lol 2 * 3
lol 2 * 3 + 4 / 2
""",
     "expected": """3
6
8.0"""
    },
    {"name": "unclosed quote",
     "code": """lol "a"
lol "b
lol 1
""",
"expected": "[main.helo line 2] on a never-ending road trip? close the quote already"
    },
    {"name": "yoink nested",
     "code": """yoink "base.helo"
lol "main"
""",
     "files": {"base.helo": """lol "base stuff"
"""},
     "expected": """base stuff
main"""
    },
    {"name": "yoink error in other file",
     "code": """lol "ok"
yoink "common.helo"
""",
     "files": {"common.helo": """lol "a"
lol
"""},
     "expected": """ok
a
[common.helo line 2] bro, a value goes here, not whatever that is"""
    },
    {"name": "yoink circular",
     "code": """yoink "a.helo"
""",
     "files": {"a.helo": """yoink "b.helo"
""",
               "b.helo": """yoink "a.helo"
"""},
     "expected": """[b.helo line 1] double-booked yourself? solo gig, one file at a time"""
    },
    {"name": "plugin",
     "code": """lol "start"
send notify "deploy done"
bet ok = send check_file "main.helo"
lol ok
lol "end"
""",
     "expected": """start
notification:deploy done
based
end"""
    },
]

def run_test(test):
    with open("main.helo","w",encoding="utf-8") as f:
        f.write(test["code"])
    for file_name,content in test.get("files",{}).items():
        with open(file_name,"w",encoding="utf-8") as g:
            g.write(content)

    result = subprocess.run(["python","heylo.py","main.helo"],capture_output=True,text=True,encoding="utf-8")
    actual = result.stdout.replace("\r\n","\n").strip()
    answer = test["expected"].replace("\r\n","\n").strip()
    if actual == answer:
        print(f"PASS: {test['name']}")
        return True
    else:
        print(f"FAIL: {test['name']}")
        print("expected:")
        print(answer)
        print("actual:")
        print(actual)
        return False

passed = 0
for test in TESTS:
    if run_test(test):
        passed += 1
print(f"{passed} / {len(TESTS)} passed")
for test in TESTS:
     for file_name in test.get("files",{}):
          if os.path.exists(file_name):
               os.remove(file_name)