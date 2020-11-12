import pynetree
import sys

class Calculator(pynetree.Parser):
    stack = []
    answer = ""
    def __init__(self):
        super(Calculator, self).__init__(
            """
                %skip /\s+/;
                @int /\d+/;
                @var /[a-z]/;

                @factor: int var | int | var;

                @mul: term '*' term;
                term: mul | factor | '(' expr ')';

                @add: expr '+' term;
                @sub: expr '-' term;
                expr$: add | sub | term;

                @calc$: expr;
            """)

    def post_int(self, node):
        self.stack.append(float(node.match))
    def post_var(self, node):
        self.stack.append(node.match)
    def post_factor(self, node):
        result = dict()
        first = self.stack.pop()
        if self.stack == []:
            second = ""
        else:
            second = self.stack.pop()
        if (type(first) is str and type(second) is float ):
            result[first]=second
        elif(type(first) is str):
            result[first]=1
            self.stack.append(second)
        else:
            result["const"]=first
            self.stack.append(second)
        self.stack.append(result)
    def post_add(self, node):
        first = self.stack.pop()
        second = self.stack.pop()
        result = dict(first)
        for key in second:
            if (key in result.keys()):
                result[key]+=second[key]
            else:
                result[key]=second[key]
        self.stack.append(result)

    def post_sub(self, node):        
        first = self.stack.pop()
        second = self.stack.pop()
        result = dict(second)
        for key in first:
            if (key in result.keys()):
                result[key]-=first[key]
            else:
                result[key]=-1.0*first[key]
        self.stack.append(result)

    def post_mul(self, node): 
        first = self.stack.pop()
        second = self.stack.pop()
        result = dict()
        for key1 in first:
            for key2 in second:
                keylist = list(filter(lambda x: x!="const", [key1,key2]))
                keylist.sort()
                key = "".join(keylist)
                if key == "":
                    key = "const"
                result[key] = first[key1] * second[key2]
        self.stack.append(result)
        pass


    def post_calc(self, node):
        result = self.stack.pop()
        keylist = list(filter(lambda x: x!="const", result.keys()))
        answer = ""
        for key in keylist:
            if answer == "":
                answer = str(int(result[key])) + key 
            else:
                answer += " + " + str(int(result[key])) + key 
        answer = answer + " + " + str(int(result["const"]))
        self.answer = answer


if __name__ == "__main__":

    c = Calculator()
    print("Please enter the Polynomial you want to calculate(e.g. x + ( 2y + 3 )* ( 3s + 4 ) * 5):")
    for line in sys.stdin: 
        if line == "\n":   
            line = "x + ( 2y + 3 )* ( 3s + 4 ) * 5"
        try:
            c.traverse(c.parse(line))
            print("Result :")
            print(line + " = " + c.answer)
        except:
            print("An error occured")
        print("\nPlease enter the Polynomial you want to calculate(e.g. x + ( 2y + 3 )* ( 3s + 4 ) * 5):")

