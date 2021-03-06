import math
from collections import deque
from enum import Enum

from PyCalc.formatModule import Converter, ConvertionException


class Priority(Enum):
    LOW = 0
    MED = 1
    HIGH = 2


operations = {
    "+": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] + args[0]},
    "-": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: args[1] - args[0]},
    "_": {"userDef": False, "pri": Priority.HIGH, "args": 1, "ltAssoc": False, "calc": lambda args: -args[0]},
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
    "and": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: int(args[1]) & int(args[0])},
    "or": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: int(args[1]) | int(args[0])},
    "xor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: int(args[1]) ^ int(args[0])},
    "not": {"userDef": False, "pri": Priority.MED, "args": 1, "ltAssoc": False, "calc": lambda args: ~ int(args[0])},
    "nand": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (int(args[1]) & int(args[0]))},
    "nor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (int(args[1]) | int(args[0]))},
    "xnor": {"userDef": False, "pri": Priority.LOW, "args": 2, "ltAssoc": False, "calc": lambda args: ~ (int(args[1]) ^ int(args[0]))},
    "lls": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: int(args[1]) << int(args[0])},
    "lrs": {"userDef": False, "pri": Priority.MED, "args": 2, "ltAssoc": False, "calc": lambda args: int(args[1]) >> int(args[0])}
}

"""
User defined operations and constants will be appended to the dictionary. If userDef is set to true calc will be
associated with a string to be injected in the expression instead of a function to be executed on-place by the
calculator to obtain the result. The string will be analyzed in another pass and basic operations will be solved while
other user defined operations will be injected too
"""


class ParseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

class Calculator:
    def __init__(self, converter: Converter):
        self.converter = converter

    def addSpaces(self, expr: str):
        items = []
        tmpString = ""
        for i in range(0, len(expr), 1):
            if expr[i] == "-":
                if tmpString != "":
                    items.append(tmpString)
                    tmpString = ""

                if i - 1 >= 0 and (self.converter.isNum(expr[i + 1]) or expr[i + 1] == "(") and (
                            (self.converter.isNum(expr[i - 1]) and expr[i - 1] != "-") or expr[i - 1] == ")"):
                    items.append(expr[i])
                else:
                    items.append("_")
            elif self.converter.isNum(expr[i]) or expr[i].isalpha():
                tmpString += expr[i]
            else:
                if tmpString != "":
                    items.append(tmpString)
                    tmpString = ""
                if not(expr[i] == "," or expr[i] == " "):
                    items.append(expr[i])

        if tmpString != "":
            items.append(tmpString)
        return items

    def rpnFormat(self, expr: str, forceDecimal: bool = False):
        try:
            if expr == "":
                raise ParseException("Empty string")

            output = list()
            operators = deque()
            exprToken = self.addSpaces(expr)

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
                        raise ParseException("Mismatched brackets")

                    operators.pop()  # pop last open parenthesis
                elif not forceDecimal and self.converter.isNum(t):
                    out = self.converter.toInt(t)
                    output.append(out)
                elif forceDecimal and self.converter.isDecimal(t):
                    output.append(float(t))
                else:
                    raise ParseException("Symbol "+str(t)+" could not be resolved as operation or number")

            for i in range(-1, -len(operators) - 1, -1):
                if operators[i] == '(':
                    raise ParseException("Mismatched brackets")
                output.append(operators[i])

            return output
        except ParseException:
            raise
        except ConvertionException:
            raise

    def solve(self, expr: str):
        try:
            exprSanitized = expr.lower().strip()  # all chars are defaulted to lower case even ones in hex numbers
            tokenList = self.rpnFormat(exprSanitized, False)

            result = self._solve(tokenList)
            return str(self.converter.applyFormatting(result))

        except ParseException:
            raise
        except ConvertionException:
            raise
        except ArithmeticError:
            raise
        except RecursionError:
            raise

    def _solve(self, tokenList: list):  # recursive function used to iterate on user defined functions
        stack = []

        if not tokenList:
            return None

        for t in tokenList:
            if type(t) is not str:
                stack.append(t)
            elif t in operations:
                if operations[t]["userDef"]:
                    newExpr = operations[t]["calc"]

                    if operations[t]["args"] is not None:
                        if len(stack) >= len(operations[t]["args"]):
                            for arg in operations[t]["args"]:
                                currVal = stack.pop()
                                newExpr = newExpr.replace(arg, str(currVal))
                        else:
                            raise ParseException("insufficient number of arguments")

                    newExpr = newExpr.lower().strip()
                    newTokenList = self.rpnFormat(newExpr, True)
                    result = float(self._solve(newTokenList))  # recursive step
                    stack.append(result)
                else:
                    args = []

                    if len(stack) >= operations[t]["args"]:

                        for _ in range(0, operations[t]["args"], 1):
                            args.append(stack.pop())

                        result = operations[t]["calc"](args)
                        stack.append(result)

                    else:
                        raise ParseException("insufficient number of arguments")
            else:
                raise ParseException("Unrecognized symbol: "+str(t))

        return str(stack.pop())  # last result in stack is final
