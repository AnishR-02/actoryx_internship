import gradio as gr

def prime_checker(n):
    n = int(n)
    if n < 2:
        return f"{n} is not a prime number ❌"
    is_prime = True
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            is_prime = False
            break
    if is_prime:
        return f"{n} is a Prime number ✅\n{n} is only divisible by 1 and {n}"
    else:
        divisors = [i for i in range(2, n) if n % i == 0]
        return f"{n} is not a Prime number ❌\nIt is divisible by {divisors}"

app = gr.Interface(
    fn=prime_checker,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Result"),
    title="Prime Number Checker 🔢"
)

app.launch()
