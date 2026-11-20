from errors import MiniError
from typing import NamedTuple,Any
import os

class Token(NamedTuple):
    kind: str
    value: Any
    line: int
    file: str = None

def tokenize(text,file=None):
    tokens = []
    line = 1
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isalpha() or ch == "_":
            start = i
            while  i < len(text) and (text[i].isalnum() or text[i] == "_"):
                i += 1
            if text[start:i] == "tbh":
                while i < len(text) and text[i] != "\n":
                    i += 1
            else:
                tokens.append(Token("word",text[start:i],line,file))
        elif ch.isdigit():
            start = i
            while i < len(text) and text[i].isdigit():
                i += 1
            tokens.append(Token("number",int(text[start:i]),line,file))
        elif ch == " ":
            i += 1
        elif ch == '"':
            i += 1
            start = i
            while i < len(text) and text[i] != '"' and text[i] != "\n":
                i += 1
            if i >= len(text) or text[i] == "\n":
                raise MiniError("on a never-ending road trip? close the quote already",line,file)
            tokens.append(Token("string",text[start:i],line,file))
            i += 1
        elif ch == "\r":
            i += 1
        elif ch == "\n":
            tokens.append(Token("newline","\n",line,file))
            line += 1
            i += 1
        else:
            if i + 1 < len(text) and ch in "<>=!" and text[i + 1] == "=":
                tokens.append(Token("symbol",text[i:i+2],line,file))
                i += 2
            else:
                tokens.append(Token("symbol",text[i],line,file))
                i += 1
    return tokens

def get_tokens(tokens,pos):
    if pos >= len(tokens):
        raise MiniError("bro just ghosted mid-line")
    return tokens[pos]

def expand_yoink(tokens,chain,done,base_dir):
    pos = 0
    try:
        while pos < len(tokens):
            token = tokens[pos]
            if token.kind == "word" and token.value == "yoink":
                name = get_tokens(tokens,pos + 1)
                if name.kind == "string":
                    cmd = get_tokens(tokens,pos + 2)
                    if cmd.kind == "newline":
                        yoink_path = os.path.abspath(os.path.join(base_dir,name.value))
                        if yoink_path in chain:
                            raise MiniError("double-booked yourself? solo gig, one file at a time",tokens[pos].line,tokens[pos].file)
                        else:
                            if yoink_path in done:
                                tokens = tokens[:pos] + tokens[pos + 3:]
                            else:
                                done.append(yoink_path)
                                with open(yoink_path,"r",encoding="utf-8") as f:
                                    text = f.read()
                                if not text.endswith("\n"):
                                    text += "\n"
                                new_tokens = tokenize(text,name.value)
                                new_tokens = expand_yoink(new_tokens,chain + [yoink_path],done,os.path.dirname(yoink_path))
                                tokens = tokens[:pos] + new_tokens + tokens[pos + 3:]
                                pos += len(new_tokens)
                    else:
                        raise MiniError("yoink it and bounce. no revenge tour after the filename",tokens[pos].line,tokens[pos].file)
                else:
                    raise MiniError("yoink with nothing to yoink? hand over a filename",tokens[pos].line,tokens[pos].file)
            else:
                pos += 1
        return tokens
    except FileNotFoundError:
        raise MiniError("swing and a miss. that file was an afterimage",tokens[pos].line,tokens[pos].file)
