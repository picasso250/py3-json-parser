
class JsonString(object):
    """docstring for JsonString"""
    def __init__(self, string):
        super(JsonString, self).__init__()
        self.string = string
    def __repr__(self):
        return '"{}"'.format(self.string)
    def value(self):
        # fix
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
                    if len(self.token) > 0:
                        return self.current_token()
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
        self.i = 0
    def analyze(self):
        return self.match_value()
    def match_value(self):
        # todo spaces between lookahead and self.nextTerminal() should be ignored
        lookahead = self.lookahead()
        print(lookahead)
        if lookahead == '{':
            self.step()
            value = {}
            while self.nextTerminal() != ']':
                k,v = self.match_pair()
                value.update(k, v)
            self.match('}')
            return value
        if lookahead == '[':
            self.step()
            # self.match elements
            value = []
            while self.nextTerminal() != ']':
                v = match_value()
                value.append(v)
                if self.nextTerminal() == ']':
                    self.match(']')
                    return v
                else:
                    self.match(',')
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
    def match(self, token):
        if self.lookahead() == token:
            self.step()
        raise Exception('unmatch {}'.format(token))
    def match_pair(self):
        k = self.match_string()
        self.match(':')
        v = self.match_value()
        return k,v
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
            print(2)
            return '[{}]'.format([self.repr_value(v) for v in value])
        if isinstance(value, dict):
            print(3)
            return '{{}}'.format([self.repr_string(k)+':'+self.repr_value(v) for v in value.items()])
        if isinstance(value, str):
            print(4)
            return '"{}"'.format(value)
        return str(value)

if __name__ == '__main__':
    # s = 'true'
    # lex = Lexer(s)
    # tl = lex.analyze()
    # print(tl)
    # g = Grammar(tl)
    # tree = g.analyze()
    # print(JsonFormat(tree))

    s = '{"hello":"world"}'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
    g = Grammar(tl)
    tree = g.analyze()
    print(JsonFormat(tree))

    s = '[3.2,4,null,false]'
    lex = Lexer(s)
    tl = lex.analyze()
    print(tl)
