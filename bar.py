import ast


with open("foo.py") as f:
    content = f.read()

tree = ast.parse(content)
class_def = tree.body[2]

p1 = class_def.body[0]
p2 = class_def.body[1]

breakpoint()