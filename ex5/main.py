# action-actionAndGoto表
import re

actionAndGoto = [{'i': '', '+': '', '-': '', '*': '', '/': '', '(': '', ')': '', '#': '', 'E': '', 'T': '', 'F': ''} for
                 y in range(16)]


# actionAndGoto = [{'E': '', 'T': '', 'F': ''} for y in range(16)]

def calculate(op, a, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        raise ValueError(f"Unknown operator: {op}")


def parse_expression(expression):
    def helper(stack, index):
        num = 0
        sign = '+'
        while index < len(expression):
            ch = expression[index]
            if ch.isdigit():
                num = num * 10 + int(ch)
            if ch == '(':
                num, index = helper([], index + 1)
            if index == len(expression) - 1 or ch in '+-*/)':
                if sign == '+':
                    stack.append(num)
                elif sign == '-':
                    stack.append(-num)
                elif sign == '*':
                    stack[-1] *= num
                elif sign == '/':
                    stack[-1] /= num
                sign = ch
                num = 0
                if ch == ')':
                    break
            index += 1
        return sum(stack), index

    return helper([], 0)[0]


def fuzhi(i, j, value):
    actionAndGoto[i][j] = value


fuzhi(0, 'i', 's5')
fuzhi(0, '/', 's4')
fuzhi(1, '+', 's6')
fuzhi(1, '-', 's12')
fuzhi(1, '#', 'acc')
fuzhi(2, '+', 'R3')
fuzhi(2, '-', 'R3')
fuzhi(2, '*', 's7')
fuzhi(2, '/', 's13')
fuzhi(2, ')', 'R3')
fuzhi(2, '#', 'R3')
fuzhi(3, '+', 'R6')
fuzhi(3, '-', 'R6')
fuzhi(3, '*', 'R6')
fuzhi(3, '/', 'R6')
fuzhi(3, ')', 'R6')
fuzhi(3, '#', 'R6')
fuzhi(4, 'i', 's5')
fuzhi(4, '(', 's4')
fuzhi(5, '+', 'R8')
fuzhi(5, '-', 'R8')
fuzhi(5, '*', 'R8')
fuzhi(5, '/', 'R8')
fuzhi(5, ')', 'R8')
fuzhi(5, '#', 'R8')
fuzhi(6, 'i', 's5')
fuzhi(6, '(', 's4')
fuzhi(7, 'i', 's5')
fuzhi(7, '(', 's4')
fuzhi(8, '+', 's6')
fuzhi(8, '-', 's12')
fuzhi(8, ')', 's11')
fuzhi(9, '+', 'R1')
fuzhi(9, '-', 'R1')
fuzhi(9, '*', 's7')
fuzhi(9, '/', 's13')
fuzhi(9, ')', 'R1')
fuzhi(9, '#', 'R1')
fuzhi(10, '+', 'R4')
fuzhi(10, '-', 'R4')
fuzhi(10, '*', 'R4')
fuzhi(10, '/', 'R4')
fuzhi(10, ')', 'R4')
fuzhi(10, '#', 'R4')
fuzhi(11, '+', 'R7')
fuzhi(11, '-', 'R7')
fuzhi(11, '*', 'R7')
fuzhi(11, '/', 'R7')
fuzhi(11, ')', 'R7')
fuzhi(11, '#', 'R7')
fuzhi(12, 'i', 's5')
fuzhi(12, '(', 's4')
fuzhi(13, 'i', 's5')
fuzhi(13, '(', 's4')
fuzhi(14, '+', 'R2')
fuzhi(14, '-', 'R2')
fuzhi(14, '*', 's7')
fuzhi(14, '/', 's13')
fuzhi(14, ')', 'R2')
fuzhi(14, '#', 'R2')
fuzhi(15, '+', 'R5')
fuzhi(15, '-', 'R5')
fuzhi(15, '*', 'R5')
fuzhi(15, '/', 'R5')
fuzhi(15, ')', 'R5')
fuzhi(15, '#', 'R5')

fuzhi(0, 'E', '1')
fuzhi(0, 'T', '2')
fuzhi(0, 'F', '3')
fuzhi(4, 'E', '8')
fuzhi(4, 'T', '2')
fuzhi(4, 'F', '3')
fuzhi(6, 'T', '9')
fuzhi(6, 'F', '3')
fuzhi(7, 'F', '10')
fuzhi(12, 'T', '14')
fuzhi(12, 'F', '3')
fuzhi(13, 'F', '15')

TOKENS_REGEX = [
    ('1', r'(int|float|char|if|else|for|while|do|break|continue|return)'),
    ('2', r'(\+|\-|\*|\/|\%|\=|\+\+|\-\-|==|!=|<=|>=|<|>|\!|\&\&|\|\|)'),
    ('3', r'[;,()\[\]\{\}]'),
    ('4', r'[a-zA-Z_]\w*'),
    ('5', r'"[^"]*"'),
    ('6', r"'.'"),
    ('7', r'\d+'),
    ('8', r'\d+\.\d+'),
    ('9', r'\$'),
]

production = [
    ['E\'', 'E'],
    ['E', 'E+T'],
    ['E', 'E-T'],
    ['E', 'T'],
    ['T', 'T*F'],
    ['T', 'T/F'],
    ['T', 'F'],
    ['F', '(E)'],
    ['F', 'i']
]


def lexer(source_code):
    tokens = []
    source_code = source_code.strip()  # 去除空格
    # 注释删除
    pattern = re.compile(r'(\/\/.*?\n)|(/\*.*?\*/)', re.MULTILINE | re.DOTALL)
    source_code = pattern.sub("", source_code)
    # 匹配词法符号，并将其加入到tokens列表中
    while source_code:
        match = None
        for token in TOKENS_REGEX:
            name, regex = token
            pattern = re.compile(regex)
            match = pattern.match(source_code)
            if match:
                value = match.group(0)
                tokens.append([name, value])
                source_code = source_code[len(value):].strip()
                break
        if not match:
            raise ValueError(f"Invalid syntax at: {source_code}")

    return tokens


# 语法分析
source_code = input("请输入源代码：")
tokens = lexer(source_code)
tokens.append(['#', '#'])
for i in range(len(tokens)):
    try:
        tokens[i][1] = eval(tokens[i][1])
        tokens[i][1] = 'i'
    except:
        pass
input_stack = []
for i in tokens:
    input_stack.append(i[1])

analysis_stack = [['#', 0]]
i = 0
k = 0
while True:
    print(analysis_stack)
    id = actionAndGoto[int(analysis_stack[k][1])][input_stack[i]]
    # print("id:" + id)
    if id != "" and id[0] == 's':
        print(i)
        analysis_stack.append([input_stack[i], int(id[1:])])
        # print(analysis_stack)
        i += 1
        k += 1
    elif id != "" and id[0] == 'R':
        try:
            # for j in range(len(production[int(id[1:]) - 1]) - 1):
            #     print(len(production[int(id[1:]) - 1]))
            #     analysis_stack.pop()
            # analysis_stack.append([production[int(id[1:]) - 1][0], actionAndGoto[int(analysis_stack[-1][1])][production[int(id[1:]) - 1][0]]])
            # i = i
            # print("R")

            guiyue = int(id[1:])
            # print("len:" + str(len(production[guiyue][1])))
            for j in range(len(production[guiyue][1])):
                # print("j:" + str(j))
                analysis_stack.pop()

            zhuangtai = actionAndGoto[int(analysis_stack[-1][1])][production[int(id[1:])][0]]
            analysis_stack.append([production[int(id[1:]) - 1][0], int(zhuangtai)])
            i = i
            k = k - len(production[guiyue][1]) + 1
        except IndexError:
            # print(IndexError)
            # print(analysis_stack)
            break
    elif id == 'acc':
        print("语法正确")
        break
    else:
        print("语法错误，出错位置为:" + str(i))
        break

result = parse_expression(source_code)
print(result)
