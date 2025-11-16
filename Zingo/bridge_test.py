import basic
from basic import String, Context, global_symbol_table

user_input = input("Enter something: ")

with open("example.zingo", "r") as f:
    zingo_code = f.read()

context = Context('<bridge_test>')
context.symbol_table = global_symbol_table

context.symbol_table.set("input_value", String(user_input))

result, error = basic.run("example.zingo", zingo_code, context) 

if error:
    print(error.as_string())
else:
    print("Zingo returned:", result)