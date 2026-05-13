import gradio as gr

def sum_of_list(numbers):
    try:
        number_list = [int(x.strip()) for x in numbers.split(",")]
        total = sum(number_list)
        average = total / len(number_list)
        return f"Numbers: {number_list}\nSum = {total} ✅\nAverage = {average:.2f}"
    except:
        return "Please enter valid numbers separated by commas. Example: 1, 2, 3, 4, 5"

app = gr.Interface(
    fn=sum_of_list,
    inputs=gr.Text(label="Enter numbers separated by commas (e.g. 1, 2, 3)"),
    outputs=gr.Text(label="Result"),
    title="Sum of a List of Numbers ➕"
)

app.launch()
