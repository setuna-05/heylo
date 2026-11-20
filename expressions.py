from errors import MiniError,MAX_DEPTH
from tokens import get_tokens
from environment import Block
import subprocess
import operator

def get_variable(evn,value):
    if value in evn.variables[-1]:
        return evn.variables[-1][value]
    elif value in evn.variables[0]:
        return evn.variables[0][value]
    else:
        raise MiniError("it's empty. quit playing solitaire and bet it")

def is_number(x):
    return isinstance(x,(int,float))and not isinstance(x,bool)

def enter_function(tokens,pos,evn,value):
    function = evn.function[value]
    if len(evn.variables) >= MAX_DEPTH:
        raise MiniError("too many loops, bro. i'm out before the labor board calls")
    else:
        next_kind = get_tokens(tokens,pos + 2).kind
        if next_kind != "newline" and function.arg_name != None:
            result,new_pos = expr(tokens,pos + 2,evn)
            pos = new_pos
            evn.stack.append(Block("send",pos))
            evn.variables.append({function.arg_name: result})
            return function.point,new_pos
        elif next_kind == "newline" and function.arg_name == None:
            evn.stack.append(Block("send",pos + 2))
            evn.variables.append({})
            return function.point,pos + 2
        else:
            if function.arg_name == None:
                raise MiniError("pulling from where? this vibe takes no args")
            else:
                raise MiniError("you set up an arg and then leave it hanging? use it")

def check_send_target(tokens,pos,evn):
    token = get_tokens(tokens,pos + 1)
    if token.kind == "word":
        in_function = token.value in evn.function
        in_plugins = token.value in evn.plugins
        if in_function and in_plugins:
            raise MiniError("you built it AND outsourced it? pick one name for each")
        elif not in_function and not in_plugins:
            raise MiniError("who you calling, bro? nobody's home by that name")
        elif in_plugins:
            eq = get_tokens(tokens,pos + 2)
            if eq.kind == "newline":
                raise MiniError("ordered the combo, served solo? bring the arg too")
            else:
                return "plugin",token.value
        else:
            return "function",token.value
    else:
        raise MiniError("can't even name your gift? give me a word")

def atom(tokens,pos,evn):
    token = tokens[pos]
    if token.kind == "number":
        result = token.value
    elif token.kind == "string":
        result = token.value
    elif token.kind == "symbol" and token.value == "-":
        result,pos = atom(tokens,pos + 1,evn)
        if is_number(result):
            result = -result
            return result,pos
        else:
            raise MiniError("numbers only, no cap. math has standards")
    elif token.kind == "word":
        if token.value == "based":
            result = True
        elif token.value == "cringe":
            result = False
        elif token.value == "yeet":
            result,pos = expr(tokens,pos + 1,evn)
            if isinstance(result,str):
                completed = subprocess.run(result,shell=True)
                result = (completed.returncode == 0)
                pos -= 1
            else:
                raise MiniError("sort it before you yeet it. i need a string")
        elif token.value == "send":
            kind,name = check_send_target(tokens,pos,evn)
            if kind == "plugin":
                result,pos = expr(tokens,pos + 2,evn)
                result = evn.plugins[name](result)
                if not isinstance(result,bool):
                    raise MiniError("outsource and vanish on me? return true or false")
            else:
                stop_depth = len(evn.stack)
                saved = evn.pos
                point,new_pos = enter_function(tokens,pos,evn,name)
                evn.execute(tokens,point,evn,stop_depth)
                evn.pos = saved
                result = evn.ship
                if result is None:
                    raise MiniError("nothing to ship but vibes. go write the ship, i'll wait")
                else:
                    evn.ship = None
                    pos = new_pos
            pos -= 1
        else:
            result = get_variable(evn,token.value)
    else:
        raise MiniError("bro, a value goes here, not whatever that is")
    pos += 1
    return result,pos
    
def term(tokens,pos,evn):
    result,pos = atom(tokens,pos,evn)
    while pos < len(tokens) and tokens[pos].kind == "symbol" and tokens[pos].value in ("*","/"):
        name_value = tokens[pos].value
        next_result,pos = atom(tokens,pos + 1,evn)
        if is_number(result) and is_number(next_result):
            if name_value == "*":
                result *= next_result
            else:
                if next_result == 0:
                    raise MiniError("dividing by zero? what are you creating out of nothing?")
                else:
                    result /= next_result 
        else:
            raise MiniError("numbers only, no cap. math has standards")
    return result,pos

def expr(tokens,pos,evn):
    result,pos = term(tokens,pos,evn)
    while pos < len(tokens) and tokens[pos].kind == "symbol" and tokens[pos].value in ("+","-"):
        token = tokens[pos]
        next_result,pos = term(tokens,pos + 1,evn)
        if token.value == "+":
            if (is_number(result) and is_number(next_result)) or (isinstance(result,str) and isinstance(next_result,str)):
                result += next_result
            else:
                raise MiniError("this ain't a smoothie. match your types")    
        else:
            if is_number(result) and is_number(next_result):
                result -= next_result
            else:
                raise MiniError("numbers only, no cap. math has standards")
    return result,pos

def not_expr(tokens,pos,evn):
    token = get_tokens(tokens,pos)
    if token.kind == "word" and token.value == "no":
        pos += 1
        result,pos = not_expr(tokens,pos,evn)
        result = not result
        return result,pos
    else:
        result,pos = compare(tokens,pos,evn)
        return result,pos

def and_expr(tokens,pos,evn):
    result,pos = not_expr(tokens,pos,evn)
    while pos < len(tokens) and tokens[pos].kind == "word" and tokens[pos].value == "fam":
        pos += 1
        next_result,pos = not_expr(tokens,pos,evn)
        result = result and next_result
    return result,pos

def or_expr(tokens,pos,evn):
    result,pos = and_expr(tokens,pos,evn)
    while pos < len(tokens) and tokens[pos].kind == "word" and tokens[pos].value == "ig":
        pos += 1
        next_result,pos = and_expr(tokens,pos,evn)
        result = result or next_result
    return result,pos

OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "!=": operator.ne,
    "==": operator.eq,
    }

def compare(tokens,pos,evn):
    result,pos = expr(tokens,pos,evn)
    if pos < len(tokens) and tokens[pos].kind == "symbol" and tokens[pos].value in OPS:
        op = tokens[pos].value
        pos += 1
        next_result,pos = expr(tokens,pos,evn)
        if op == "==" or  op == "!=":
            return OPS[op](result,next_result),pos
        else:
            if (is_number(result) and is_number(next_result)) or (isinstance(result,str) and isinstance(next_result,str)):
               return OPS[op](result,next_result),pos
            else:
                raise MiniError("neck and neck? only if you're the same type") 
    else:
        return result,pos