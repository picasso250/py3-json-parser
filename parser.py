
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
        # current token must be a number
        self.back()
        token = self.token
        self.token = ''
        first = token[0]
        if first == '-' or first.isdigit():
            return self.match_number(token)
        else:
            return token
    def match_number(self, token):
        if '.' in token or 'e' in token or 'E' in token:
            return float(token)
        return int(token)
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

class Grammar(object):
    """docstring for Grammar"""
    def __init__(self, token_list):
        super(Grammar, self).__init__()
        self.token_list = token_list
    def stmt():
        value = None
        # todo spaces between lookahead and nextTerminal should be ignored
        lookahead = self.lookahead()
        if lookahead == '{':
            if value is None:
                value = {}
            while nextTerminal != ']':
                k,v = match_pair()
                value.update(k, v)
            match(')')
            return value
        if lookahead == '[':
            # match elements
            while nextTerminal != ']':
                match_value()
            match(']')
            return value
        if lookahead == '"':
            match_string()
    def match_pair(self):
        match_string()
        match(':')
        match_value()
    def step(self):
        self.i += 1
        if self.i >= self.n:
            return False
        return True
    def lookahead(self):
        lh = self.s[self.i]
        # print(lh)
        return lh

if __name__ == '__main__':
    s = '{"hello":"world"}'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)

    s = '[3.2,4,null,false]'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
