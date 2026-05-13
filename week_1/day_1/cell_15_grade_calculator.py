maths_score = int(input("Enter the maths score"))
physics_score = int(input("Enter the physics score"))
chemistry_score = int(input("Enter the chemistry score"))
total = maths_score + physics_score + maths_score
if (total // 3 > 90):
    print("A+")
elif (total // 3 > 80):
    print("A")
elif (total // 3 > 70):
    print("B")
elif (total // 3 > 60):
    print("C")
elif (total // 3 > 50):
    print("D")
else:
    print("F")
