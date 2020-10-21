import pynetree

class Calculator(pynetree.Parser):
    stack = []

    def __init__(self):
        super(Calculator, self).__init__(
            """
                %skip /\s+/;
                @int /\d+/;
                @var /[a-z]/;

                @factor: int var | int | var;

                @mul: term '*' factor;
                term: mul | factor;

                @add: expr '+' term;
                expr$: add | term;

                @calc$: expr;
            """)

    def post_int(self, node):
        print("int")
        self.stack.append(float(node.match))
    def post_var(self, node):
        print("variable")
        self.stack.append(node.match)
    def post_factor(self, node):
        result = dict()
        first = self.stack.pop()
        second = self.stack.pop()
        # print(first)
        # print(second)
        if (type(first) is str and type(second) is float ):
            # print("int var")
            result[first]=second
        elif(type(first) is str):
            # print("var")
            result[first]=1
            self.stack.append(second)
        else:
            # print("int")
            result["const"]=first
            self.stack.append(second)
        
        print(result)
        self.stack.append(result)
        print(self.stack)

    def post_add(self, node):
        first = self.stack.pop()
        second = self.stack.pop()
        result = dict(first)
        for key in second:
            print(key)
            if (key in result.keys()):
                result[key]+=second[key]
            else:
                result[key]=second[key]
        print(result)
        self.stack.append(result)
        # self.stack.append(self.stack.pop() + self.stack.pop())

    def post_sub(self, node):
        pass
        # x = self.stack.pop()
        # self.stack.append(self.stack.pop() - x)

    def post_mul(self, node):
        pass
        # self.stack.append(self.stack.pop() * self.stack.pop())

    def post_div(self, node):
        pass
        # x = self.stack.pop()
        # self.stack.append(self.stack.pop() / x)

    def post_calc(self, node):
        print(self.stack.pop())

c = Calculator()
c.traverse(c.parse("3s + 4"))
# p = pynetree.Parser("""
#     %skip /\s+/;
#     @int /\d+/;
#     @var /[a-z]/;

#     @singleterm: int var | var;
#     factor: int var | '(' expr ')' | int | var;

#     @mul: term '*' factor;
#     term: mul | factor;

#     @add: expr '+' term;
#     expr$: add | term;
# """)
# p.parse("x + 2y * ( 3s + 4 ) * 5").dump()