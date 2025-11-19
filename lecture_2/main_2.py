"""
This script collects user information including name, birth year,
and hobbies, then generates a profile summary based
on the collected data.
"""


def generate_profile(age: int) -> str:
    """
    Generate a life stage profile based on age.
    Args:
        age (int): The age of the user.
    Returns:
        str: The life stage category.
    """
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"


user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
current_year = 2025
birth_year = int(birth_year_str)
current_age = current_year - birth_year
hobbies = []

while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    hobbies.append(hobby)

life_stage = generate_profile(current_age)
user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies,
}

print(
    f"---\n"
    f"Profile Summary:\n"
    f"Name: {user_profile['name']}\n"
    f"Age: {user_profile['age']}\n"
    f"Life Stage: {user_profile['stage']}"
)

if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hobby in hobbies:
        print(f"- {hobby}")

print("---")
