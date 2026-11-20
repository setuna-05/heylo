# heylo

heylo (hey + hallo) is a carefree language.
Mess up, and its error messages roast you.
Why .helo and not .heylo? Good catch! I just wanted it simple.

## Examples

    bet ok = yeet "nonexistent_cmd"
    sus ok
        lol "nice play"
    idk
        lol "command not found. skill issue"
    fin

Output:

    'nonexistent_cmd' は、内部コマンドまたは外部コマンド、
    操作可能なプログラムまたはバッチ ファイルとして認識されていません。
    command not found. skill issue

The first lines are the shell's error; the last line is heylo's own message.

    lol "Let's go"
    bet ready = based
    sus ready
        lol "good"

Output:

    Let's go
    good
    [main.helo line 3] you ran it all and there's no finish line?! add the fin

We're closing doors in life. It's like you never closed your sus.

## Running it

To enjoy heylo, you need Python. I tested it on 3.15.
How do you run it? Don't worry. Type this in your terminal:

    python heylo.py main.helo

On Windows, add the folder containing heylo.bat to your PATH.
Then you can always just type `heylo main.helo`.

## How it works

The word you'll use most often is `lol`!
`lol` prints its contents to your screen. I think it just bursts out involuntarily.

    lol "hallo"

Output:

    hallo

`bet` is simple. It stores a value in a variable. You can branch on it later.

    bet a = "hey"
    lol a

Output:

    hey

Not sure what will happen? Use `sus`.
`sus` compares things, and runs its block only if the comparison is true.
Everything else is caught by `idk`.

    bet a = 3
    sus a > 5
        lol "big"
    idk
        lol "small"
    fin

Output:

    small

Change `a` to `8` and you'll get `big`.

Look at the end of the block. `fin` marks where it ends.
You don't need indentation.
If you forget `fin`, you get an error.

`spam` is a loop. It repeats its block while the condition is true.
It's handy, but be careful: change the value in the condition inside the block.
Otherwise, it never stops.
To update a value, use `bet` again.

    bet a = 0
    spam a < 3
        lol a
        bet a = a + 1
    fin

Output:

    0
    1
    2

Let's yeet something! `yeet` runs a shell command.
If it succeeds, it returns `based` (true). If it fails, it returns `cringe` (false).
Catch the result with `bet`, then judge it with `sus`.

    bet ok = yeet "ver"
    sus ok
        lol "Yes"
    idk
        lol "No"
    fin

Output (tested on Windows; `ver` is a Windows command):

    Microsoft Windows [Version 10.0.26300.9974]
    Yes

Let's set up some work. Here's what happens, in order.
First, write a function with `vibe`.
Next, use `ship` to send a value back.
Last, call it with `send`. Nothing runs until you call it.

    vibe greet name
        ship "hey" + name
    fin
    bet r = send greet "lo"
    lol r

Output:

    heylo

`tbh` adds hidden notes to your code. The whole line is ignored.
Even a `lol` after it never runs.

    lol "comment check"
    tbh to be honest, I built this language in about two weeks. I was tired, haha.
    tbh lol "I'm freedom! fuuuuuu"

Output:

    comment check

Time to combine some conditions.
`fam` means both sides must be true. `ig` means at least one side must be true.
`no` flips a condition.
`based` is true, and `cringe` is false.

    bet a = 80
    bet b = 30
    sus a > 70 fam no b > 50
        lol "nice"
    idk
        lol "not nice"
    fin

Output:

    nice

Here, `a > 70` is true, and `b > 50` is false.
`no` flips that false to true, so both sides of `fam` are true.

Yoink another file!
`yoink` grabs a file from next door.

base.helo:

    vibe praise name
        ship name + " is a W"
    fin

main.helo:

    yoink "base.helo"
    bet r = send praise "heylo"
    lol r

Output:

    heylo is a W

If you write it like the example below, the error will steal your time.

a.helo:

    yoink "b.helo"

b.helo:

    yoink "a.helo"

Output when you run `a.helo`:

    [b.helo line 1] double-booked yourself? solo gig, one file at a time

`send` and `yeet` take everything after them as one argument.

    vibe double n
        ship n * 2
    fin
    bet r = send double 3 + 1
    lol r

Output:

    8

You might expect 7, but actually `3 + 1` becomes 4, then it's doubled to 8. Careful!
Also, if you want to call `send` twice, split it up with `bet`.

## Plugins

You can bring your own Python functions!
Put your code in the `plugins` folder.

plugins/basic_plugins.py:

    from plugin_api import plugin
    import os

    @plugin
    def check_file(path):
        return os.path.exists(path)

The only rule is to put `@plugin` above the function. That's easy.
Then call it from your .helo file with `send`.

    bet ok = send check_file "main.helo"
    bet missing = send check_file "great.helo"
    sus ok
        lol "found it, W"
    fin
    sus no missing
        lol "that file doesn't exist. are your eyes decorative? lol"
    fin

Output:

    found it, W
    that file doesn't exist. are your eyes decorative? lol

Also, the return value is `True` or `False`. That's why you can judge it with `sus`.

## Tests

Introduction something, let's test!
Type `python test_all.py` in your terminal.
If the output ends with `12 / 12 passed`, that's proof it works.
After each `PASS:` comes a description of what was tested.

    PASS: missing fin
    PASS: full program
    PASS: missing ship
    PASS: error inside vibe with route
    PASS: ship return value
    PASS: recursion limit with route
    PASS: small expressions
    PASS: unclosed quote
    PASS: yoink nested
    PASS: yoink error in other file
    PASS: yoink circular
    PASS: plugin
    12 / 12 passed

## Syntax highlighting

You can paint your code!
After downloading, run this in the `heylo-vscode` folder in your terminal:

    code --install-extension heylo-lang-0.0.1.vsix

After installing, reopen VS Code. Then VS Code will color your .helo files.
I've only tried it on Windows, because I'm not sure about other systems.

## License

License: MIT
Feel free to use it however you like. Let's go!!! yeaaaaaaaaaaaah

## Maybe later

Here's what I might do someday:

- Standalone app (no Python needed)
- A separate Japanese version (not a replacement)
