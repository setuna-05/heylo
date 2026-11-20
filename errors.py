class MiniError(Exception):
    def __init__(self,message,line=None,file=None):
        super().__init__(message)
        self.line = line
        self.file = file

MAX_DEPTH = 100

def show_error(e,line=None,file=None):
    if e.line is not None:
        number = e.line
    else:
        number = line
    if e.file is not None:
        file = e.file
    if number is None:
        print(f"[{file}] {str(e)}")
    else: 
        print(f"[{file} line {number}] {str(e)}")