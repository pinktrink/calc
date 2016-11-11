"""
This is the main package for Calc. It contains the primary class that
will implement different features of the calculator.
The only external dependency here is pyparsing.
"""

import sys

from pyparsing import (
    Combine,
    Word,
    Literal,
    Forward,
    Optional,
    ZeroOrMore,
    nums,
    oneOf
)


# Define a basic language for pyparsing to parse, so that we can
# properly parse any incoming logic.


def calcLang():
    """
    This function defines the overall language that will be used to
    to represent mathematical logic.
    Thanks to pyparsing this is defined in a pseudo Backus-Naur form.
    """

    point = Literal('.')
    # Combining a positive or negative integer with a possible point
    # and followup number
    number = Combine(Word('+-' + nums, nums) +
                     Optional(point + Optional(Word(nums)))).setParseAction(
                         lambda n: float(n[0])
                     )
    operation = oneOf('+ - / * ^')
    expression = Forward()
    # Resursive logic here to allow for as many expressions as possible.
    expression << number + ZeroOrMore(operation + expression)

    return expression

class Calc():
    """
    This class defines the overall structure for operations and logical
    execution. We need evaluation to be recursive so that we can
    continuously parse the string that is input and generate a result.
    """

    def evaluate(self, stack, sign='^'):
        """
        This function recursively evaulates the stack of logic to
        process it.
        First we look for ^ and the slice what is before and after it
        out of the array. We then send it to evaluateExpr which will
        return the result of the individual expression. We then replace
        the aforementioned slice with the result.
        We do this then for '*', '/', '+', and '-', until the stack
        is only 1 element long, at which point we return it.
        """

        if len(stack) == 1:
            return stack[0]

        for i, n in enumerate(stack):
            if n == sign:
                stack[i - 1:i + 2] = self.evaluateExpr(stack[i - 1:i + 2])
                return self.evaluate(stack, sign)

        self.evaluate(stack, sign='*')
        self.evaluate(stack, sign='/')
        self.evaulate(stack, sign='+')
        self.evaluate(stack, sign='-')

    def evaluateExpr(self, stack):
        """
        This function simply reduces the 3 element stack down to 1 by
        performing the operation contained in [1] on [0] and [2].
        """

        if stack[1] == '^':
            return [stack[0] ** stack[2]]
        elif stack[1] == '*':
            return [stack[0] * stack[2]]
        elif stack[1] == '/':
            return [stack[0] / stack[2]]
        elif stack[1] == '+':
            return [stack[0] + stack[2]]
        elif stack[1] == '-':
            return [stack[0] - stack[2]]

if __name__ == '__main__':
    result = calcLang().parseString(' '.join(sys.argv[1:]))
    Calc().evaluate(result)
