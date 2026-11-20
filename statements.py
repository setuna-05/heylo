from expressions import or_expr,expr,enter_function,check_send_target
from environment import Block,Function
from tokens import get_tokens
from errors import MiniError,MAX_DEPTH


def exec_ship(tokens,pos,evn):
    result,new_pos = or_expr(tokens,pos + 1,evn)
    found = False
    while evn.stack:
        block = evn.stack.pop()
        if block.kind == "send":
            found = True
            break
    if found:
        evn.variables.pop()
        new_pos = block.where
        evn.ship = result
        return new_pos
    else:
        raise MiniError("ship from where? build a vibe first")

def exec_lol(tokens,pos,evn):
    result,new_pos = or_expr(tokens,pos + 1,evn) 
    if isinstance(result,bool):
        if result:
            print("based")
        else:
            print("cringe")
    else:
        print(result)
    return new_pos

def exec_bet(tokens,pos,evn):
    name = get_tokens(tokens,pos + 1)
    eq = get_tokens(tokens,pos + 2)
    if name.kind == "word":
        if eq.kind == "symbol" and eq.value == "=":
            result,new_pos = or_expr(tokens,pos + 3,evn) 
            evn.variables[-1][name.value] = result
            return new_pos
        else:
            raise MiniError("no bridge, no bet. where's the =?")
    else:
        raise MiniError("no name, no bet. manners")

def exec_sus(tokens,pos,evn):
    evn.stack.append(Block("sus",pos))
    result,new_pos = or_expr(tokens,pos + 1,evn)
    if isinstance(result,bool):
        if result:
            pos = new_pos
        else:
            pos = skip_block(tokens,new_pos,True)
            token = tokens[pos]
            if token.kind == "word" and token.value == "fin":
                evn.stack.pop()
            pos += 1
        return pos
    else:
        raise MiniError("can't decide, huh? it's gotta be based or cringe")

def exec_idk(tokens,pos,evn):
    if not evn.stack or evn.stack[-1].kind != "sus":
        raise MiniError("can't idk what you never sus")
    else:
        pos = skip_block(tokens,pos + 1,False)
        token = tokens[pos]
        if token.kind == "word" and token.value == "fin":
            evn.stack.pop()
            pos += 1
        return pos

def exec_spam(tokens,pos,evn):
    evn.stack.append(Block("spam",pos))
    result,new_pos = or_expr(tokens,pos + 1,evn)
    if isinstance(result,bool):
        if result:
            pos = new_pos
        else:
            pos = skip_block(tokens,new_pos,False)
            token = tokens[pos]
            if token.kind == "word" and token.value == "fin":
                evn.stack.pop()
                pos += 1
        return pos
    else:
        raise MiniError("can't decide, huh? it's gotta be based or cringe")

def exec_fin(tokens,pos,evn):
    if not evn.stack:
        raise MiniError("closing nothing? the void stays void")
    else:
        block = evn.stack.pop()
        if block.kind == "spam":
            pos = block.where
        elif block.kind == "send":
            evn.variables.pop()
            pos = block.where
        else:
            pos += 1
        return pos

def exec_vibe(tokens,pos,evn):
    token = get_tokens(tokens,pos + 1)
    next_token = get_tokens(tokens,pos + 2)
    if token.kind == "word":
        if token.value in evn.function:
            raise MiniError("spot-the-difference game? wrong, there should be one")
        else:
            if next_token.kind == "newline":
                evn.function[token.value] = Function(pos + 2,None)
                pos = skip_block(tokens,pos + 2,False)
            else:
                if next_token.kind == "word":    
                    evn.function[token.value] = Function(pos + 3,next_token.value)
                    pos = skip_block(tokens,pos + 3,False)
                else:
                    raise MiniError("an argument name that's not a word? useless")
        return pos + 1
    else:
        raise MiniError("et tu, bro? give me a name")

def exec_send(tokens,pos,evn):
    kind,name = check_send_target(tokens,pos,evn)
    if kind  == "plugin":
        result,pos = expr(tokens,pos + 2,evn)
        evn.plugins[name](result)
        return pos
    else:
        point,new_pos = enter_function(tokens,pos,evn,name)
        return point

def skip_block(tokens,pos,stop_at_idk):
    depth = 0
    while pos < len(tokens):
        token = tokens[pos]
        if token.kind == "word":
            if token.value in ("sus","spam","vibe"):
                depth += 1
            elif token.value == "fin" and depth != 0:
                depth -= 1
            elif token.value == "fin" and depth == 0:
                break
            elif token.value =="idk" and depth == 0 and stop_at_idk:
                break
        pos += 1
    if pos >= len(tokens):
        raise MiniError("left the door open? lock it with fin")
    else:
        return pos