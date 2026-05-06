n = int(input("How many numbers? "))
numbers = [int(input(f"Enter number {i+1}: ")) for i in range(n)]
print(numbers)
sum = 0
for i in range(0, n):
    sum += numbers[i]
print(sum)
