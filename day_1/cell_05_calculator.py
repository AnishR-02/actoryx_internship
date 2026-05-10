num1 = float(input("Enter first number: "))
operator = input("Enter operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))

match operator:
    case '+':
        print(f"{num1} + {num2} = {num1 + num2}")
    case '-':
        print(f"{num1} - {num2} = {num1 - num2}")
    case '*':
        print(f"{num1} * {num2} = {num1 * num2}")
    case '/':
        if num2 == 0:
            print("Error: Division by zero!")
        else:
            print(f"{num1} / {num2} = {num1 / num2}")
    case _:
        print("Invalid operator!")
