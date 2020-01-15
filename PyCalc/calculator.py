from enum import Enum
from collections import deque
import math


class Priority(Enum):
    LOW = 0
    MED = 1
    HIGH = 2


operations = {
    "+": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] + args[0]},
    "-": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] - args[0]},
    "_": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": True, "calc": lambda args: -args[0]},
    "*": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] * args[0]},
    "/": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] / args[0]},
    "%": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] % args[0]},
    "^": {"userDef": False, "pri": Priority.HIGH, "args": 2, "ltAssoc": True, "calc": lambda args: args[1] ** args[0]},
    # --------scientific---------
    "pi": {"userDef": False, "pri": Priority.HIGH, "args": 0, "ltAssoc": False, "calc": lambda _: math.pi},
    "e": {"userDef": False, "pri": Priority.HIGH, "args": 0, "ltAssoc": False, "calc": lambda _: math.e},
    "ceil": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.ceil(args[0])},
    "floor": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.floor(args[0])},
    "sqrt": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.sqrt(args[0])},
    "ln": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.log(args[0])},
    "log": {"userDef": False, "pri": Priority.HIGH, "args": 2, "ltAssoc": False, "calc": lambda args: math.log(args[1], args[0])},
    "log10": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.log10(args[0])},
    "log2": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.log2(args[0])},
    "sin": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.sin(args[0])},
    "cos": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.cos(args[0])},
    "tan": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: math.tan(args[0])},
    # --------bitwise op---------
    "and": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] & args[0]},
    "or": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] | args[0]},
    "xor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] ^ args[0]},
    "not": {"userDef": False, "pri": Priority.MED, "args": 1, "ltAssoc": False, "calc": lambda args: ~ args[0]},
    "nand": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (args[1] & args[0])},
    "nor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (args[1] | args[0])},
    "xnor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (args[1] ^ args[0])},
    "lls": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] << args[0]},
    "lrs": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] >> args[0]}
}

"""
User defined operations and constants will be appended to the dictionary. If userDef is set to true calc will be
associated with a string to be injected in the expression instead of a function to be executed on-place by the
calculator to obtain the result. The string will be analyzed in another pass and basic operations will be solved while
other user defined operations will be injected too
"""


class Calculator:
    def __init__(self, converter):
        self.converter = converter
        self.error = None

    def addSpaces(self, expr):
        exprOut = ""

        for i in range(0, len(expr), 1):
            if expr[i] in operations.keys():
                if expr[i] == "-":
                    # check num on the right and operation or start on the left
                    if (expr[i+1] != "-" and self.converter.isNum(expr[i+1]) and i - 1 < 0 or
                            expr[i + 1] != "-" and self.converter.isNum(expr[i+1]) and expr[i-1] in operations.keys()):
                        exprOut += expr[i]
                    else:
                        if i - 1 >= 0:  # avoid adding spaces in first position
                            exprOut += " "
                        exprOut += "_ "
                elif operations[expr[i]]["userDef"] and len(operations[expr[i]]["args"]) == 0:
                    exprOut += expr[i]  # check for used defined constant
                else:
                    if operations[expr[i]]["args"] != 0:
                        exprOut += " " + expr[i] + " "  # if function has zero args is a const
                    else:
                        exprOut += expr[i]  # don't add spaces around constants so they behave like numbers
            elif expr[i] == "(":
                if i > 0 and expr[i-1].isalpha():
                    exprOut += " "  # insert additional space between function and bracket cos(x) --> cos ( x )
                exprOut += "( "
            elif expr[i] == ")":
                exprOut += " )"
            elif expr[i] == ",":  # commas are like spaces to separate function arguments
                exprOut += " "
            else:
                exprOut += expr[i]

        return exprOut

    def rpnFormat(self, expr):
        if expr == "":
            self.error = "Empty string"
            return None

        output = list()
        operators = deque()
        exprToken = self.addSpaces(expr).split(" ")

        for t in exprToken:
            if t in operations:
                while (operators and operators[-1] != '(' and
                       operations[operators[-1]]["pri"].value >= operations[t]["pri"].value):
                    output.append(operators.pop())

                operators.append(t)
            elif t == '(':
                operators.append(t)
            elif t == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())

                if not operators:
                    self.error = "Mismatched parenthesis"
                    return None

                operators.pop()  # pop last open parenthesis
            elif self.converter.isNum(t):
                out = self.converter.toInt(t)
                if out is not None:
                    output.append(out)
                else:
                    self.error = self.converter.error
                    return None
            else:
                self.error = "Symbol "+str(t)+" could not be resolved as operation or number"
                return None

        for i in range(-1, -len(operators) - 1, -1):
            if operators[i] == '(':
                self.error = "Mismatched parenthesis"
                return None
            output.append(operators[i])

        return output

    def solve(self, expr):
        exprSanitized = expr.lower().strip()    # all chars are defaulted to lower case even ones in hex numbers
        tokenList = self.rpnFormat(exprSanitized)
        stack = []

        if not tokenList:
            return None

        for t in tokenList:
            if type(t) is not str:
                stack.append(t)
            elif t in operations:
                if operations[t]["userDef"]:
                    newExp = operations[t]["calc"]

                    if len(stack) >= len(operations[t]["args"]):
                        for arg in operations[t]["args"]:
                            currVal = stack.pop()
                            newExp = newExp.replace(arg, str(currVal))

                        result = self.solve(newExp)  # recursive step
                        stack.append(str(result))
                    else:
                        self.error = "insufficient number of arguments"

                else:
                    args = []

                    if len(stack) >= operations[t]["args"]:

                        for _ in range(0, operations[t]["args"], 1):
                            args.append(stack.pop())

                        result = operations[t]["calc"](args)
                        stack.append(result)
                    else:
                        self.error = "insufficient number of arguments"
            else:
                self.error = "Unrecognized symbol: "+str(t)

        res = self.converter.applyFormatting(stack.pop())  # last result in stack is final

        if res is not None:
            return str(res)
        else:
            self.error = self.converter.error
            return None
