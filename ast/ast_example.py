import ast
expression = '(1 + 2) * 3'
my_ast = ast.dump(ast.parse(expression))
print my_ast