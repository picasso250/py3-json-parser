
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
                # print(self.token)
    def match_string(self):
        self.token = ''
        while True:
            if not self.step():
                raise Exception('no end of string')
            lh = self.lookahead()
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
        self.n = len(token_list)
        self.i = -1
    def analyze(self):
        return self.match_value
    def match_value(self):
        # todo spaces between lookahead and self.nextTerminal() should be ignored
        lookahead = self.lookahead()
        if lookahead == '{':
            value = {}
            while self.nextTerminal() != ']':
                k,v = match_pair()
                value.update(k, v)
            match(')')
            return value
        if lookahead == '[':
            # match elements
            value = []
            while self.nextTerminal() != ']':
                v = match_value()
                value.append(v)
                if self.nextTerminal() == ']':
                    match(']')
                    return v
                else:
                    match(',')
            return value
        if isinstance(lookahead, JsonString):
            return lookahead.value()
        if isinstance(lookahead, int) or isinstance(lookahead, float):
            return lookahead
        if isinstance(lookahead, str):
            if lookahead == 'true':
                return True
            elif lookahead == 'false':
                return False
            elif lookahead == 'null':
                return None
            else:
                raise Exception('unkonwn token {}'.format(lookahead))
        raise Exception('unkonwn token type {}'.format(type(lookahead)))
    def match_pair(self):
        k = match_string()
        match(':')
        v = match_value()
    def match_string(self):
        lookahead = self.lookahead()
        if isinstance(lookahead, JsonString):
            self.step()
            return lookahead.value()
        raise Exception('unkonwn token type {}'.format(type(lookahead)))
    def step(self):
        self.i += 1
        if self.i >= self.n:
            return False
        return True
    def lookahead(self):
        lh = self.token_list[self.i]
        # print(lh)
        return lh
    def nextTerminal(self):
        i = self.i + 1
        if i >= self.n:
            return None
        return self.token_list[i]

class JsonFormat(object):
    """docstring for JsonFormat"""
    def __init__(self, tree):
        super(JsonFormat, self).__init__()
        self.tree = tree
    def __repr__(self):
        return self.repr_value(self.tree)
    def repr_value(self, value):
        if isinstance(value, list):
            return '[{}]'.format([self.repr_value(v) for v in value])
        if isinstance(value, dict):
            return '{{}}'.format([self.repr_string(k)+':'+self.repr_value(v) for v in value.items()])
        if isinstance(value, str):
            return '"{}"'.format(value)
        return str(value)
def repr_tree():
    pass

if __name__ == '__main__':
    s = '{"hello":"world"}'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
    g = Grammar(tl)
    tree = g.analyze()
    print(tree)

    s = '[3.2,4,null,false]'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
