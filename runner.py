from errors import MiniError,show_error
from environment import Environment
from statements import exec_ship,exec_lol,exec_bet,exec_sus,exec_idk,exec_spam,exec_fin,exec_vibe,exec_send

STATEMENTS = {
    "ship": exec_ship,
    "lol": exec_lol,
    "bet": exec_bet,
    "sus": exec_sus,
    "idk": exec_idk,
    "spam": exec_spam,
    "fin": exec_fin,
    "vibe": exec_vibe,
    "send": exec_send
}

def run(tokens,plugins):
    evn = Environment(plugins,execute)
    pos = 0
    try:
        pos = execute(tokens,pos,evn)
        if evn.stack:
            block = evn.stack[-1]
            if block.kind == "send":
                number = tokens[block.where - 1].line
                file_name = tokens[block.where - 1].file 
            else:
                number = tokens[block.where].line
                file_name = tokens[block.where].file
            raise MiniError("you ran it all and there's no finish line?! add the fin",number,file_name)
    except MiniError as e:
        if e.line is not None:
            show_error(e,None,e.file)
        else:
            show_error(e,tokens[evn.pos].line,tokens[evn.pos].file)
        last = None
        count = 0
        for block in reversed(evn.stack):
            if block.kind == "send":
                number = tokens[block.where - 1].line
                if number == last:
                    count += 1
                else:
                    if last is not None:
                        print_route(last,count)
                    last = number
                    count = 1
        if last is not None:
            print_route(last,count)
        return
    except RecursionError:
        err = MiniError("stack's overflowing, bro. this nest goes too deep, i'm bailing")
        show_error(err,tokens[evn.pos].line,tokens[evn.pos].file)
        return

def print_route(number,count):
    if count == 1:
        print(f"word from the send on line {number}")
    else:
        print(f"word from the send on line {number} (x{count})")

def execute(tokens,pos,evn,stop_depth=None):
    while pos < len(tokens) and (stop_depth is None or len(evn.stack) > stop_depth):
        evn.pos = pos
        token = tokens[pos]
        if token.kind == "word" and token.value in STATEMENTS:
            handler = STATEMENTS[token.value]
            pos = handler(tokens,pos,evn)
        elif token.kind == "newline":
                pos += 1
        else:
            raise MiniError("single-task, bro. something extra snuck in, check for foul play")
    return pos