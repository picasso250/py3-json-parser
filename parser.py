
class JsonString(object):
    """docstring for JsonString"""
    def __init__(self, string):
        super(JsonString, self).__init__()
        self.string = string
    def __repr__(self):
        return self.string
        
class Lexer(object):
    """docstring for Lexer"""
    def __init__(self, s):
        super(Lexer, self).__init__()
        self.s = s
        self.n = len(s)
        self.i = -1
        self.state = 'normal'
        self.token = ''
    def analyze(self):
        tl = []
        while True:
            nt = self.next_token()
            if nt is not None:
                tl.append(nt)
            else:
                return tl
    def next_token(self):
        if self.state == 'normal':
            while True:
                if not self.step():
                    return None
                lh = self.lookahead()
                if lh == '{' or lh == '}' or lh == '[' or lh == ']' or lh == ',' or lh == ':':
                    if len(self.token) > 0:
                        return self.current_token()
                    else:
                        return lh
                if lh == '"':
                    if len(self.token) > 0:
                        return self.current_token()
                    else:
                        self.state == 'string'
                        return self.match_string()
                self.token += lh
                print(self.token)
    def match_string(self):
        self.token = ''
        while True:
            if not self.step():
                raise Exception('no end of string')
            lh = self.lookahead()
            print(lh)
            if lh == '"':
                js = JsonString(self.token)
                self.token = ''
                self.state = 'normal'
                return js
            if lh == '\\':
                self.token += lh
                if not self.step():
                    raise Exception('no end of string after back slash')
                self.token += self.lookahead()
                continue
            # fix \u
            self.token += lh
            # print(self.token)

    def current_token(self):
        self.back()
        token = self.token
        self.token = ''
        return token
    def back(self):
        self.i -= 1
    def lookahead(self):
        lh = self.s[self.i]
        # print(lh)
        return lh
    def step(self):
        # fix utf8
        self.i += 1
        if self.i >= self.n:
            return False
        return True

# spaces between lookahead and nextTerminal should be ignored
def stmt():
    if lookahead == '{':
        while nextTerminal == '"':
            # match_pair()
            match_str()
            match(':')
            match_value()
    if lookahead == '[':
        # match elements
        while nextTerminal != ']':
            match_value()
    if lookahead == '"':
        match_str()

if __name__ == '__main__':
    s = '{"hello":"world"}'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)

    s = '[3.2,4,null,false]'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
