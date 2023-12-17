import re
class Calculator:
    def __init__(self):
        self.operators = {
            '+': {'priority': 1, 'function': lambda x, y: x + y},
            '-': {'priority': 1, 'function': lambda x, y: x - y},
            '*': {'priority': 2, 'function': lambda x, y: x * y},
            '/': {'priority': 2, 'function': lambda x, y: x / y},
            '**': {'priority': 3, 'function': lambda x, y: x ** y},
            'u-': {'priority': 4, 'function': lambda x: -x}
        }

    def evaluate(self, expression):
        tokens = self.tokenize(expression)
        postfix = self.to_postfix(tokens)
        return self.calculate_postfix(postfix)

    def tokenize(self, expression):
        token_pattern = re.compile(r'\*\*|[\+\-\*/\(\)]|\d+\.\d+|\d+')
        tokens = token_pattern.findall(expression)

        processed_tokens = []
        for i, token in enumerate(tokens):
            if token == '-' and (i == 0 or tokens[i-1] in self.operators or tokens[i-1] == '('):
                processed_tokens.append('u-')
            else:
                processed_tokens.append(token)

        return [float(token) if token.replace('.', '', 1).isdigit() else token for token in processed_tokens]

    def to_postfix(self, tokens):
        stack = []
        postfix = []
        for token in tokens:
            if token in self.operators:
                while stack and stack[-1] != '(' and self.operators[token]['priority'] <= self.operators[stack[-1]]['priority']:
                    postfix.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            else:
                postfix.append(token)
        while stack:
            postfix.append(stack.pop())
        return postfix

    def calculate_postfix(self, postfix):
        stack = []
        for token in postfix:
            if token in self.operators:
                if token == 'u-':
                    stack.append(self.operators[token]['function'](stack.pop() if stack else 0))
                else:
                    y, x = (stack.pop() if stack else 0), (stack.pop() if stack else 0)
                    if token == '/' and y == 0:
                        return "Error: Division by zero"
                    stack.append(self.operators[token]['function'](x, y))
            else:
                stack.append(token)
        return stack[0] if stack else 0