from datetime import datetime

def zellers_congruence(day, month, year):
    """
    Zeller's Congruence algorithm to determine the day of the week.
    Returns the name of the weekday.
    """

    # January and February are counted as months 13 and 14 of the previous year
    if month < 3:
        month += 12
        year -= 1

    q = day
    m = month
    K = year % 100        # Year of the century
    J = year // 100       # Zero-based century

    # Zeller's formula
    h = (q + (13 * (m + 1)) // 5 + K + K // 4 + J // 4 + 5 * J) % 7

    # Mapping Zeller output to weekdays (0 = Saturday, ..., 6 = Friday)
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return days[h]

def calculate_age(day, month, year):
    """
    Calculate the age of the person based on the birth date.
    """
    today = datetime.today()
    birth_date = datetime(year, month, day)
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# --- Example: Ask the user for their birth date ---
try:
    day = int(input("Enter your birth day (1-31): "))
    month = int(input("Enter your birth month (1-12): "))
    year = int(input("Enter your birth year (e.g., 2000): "))

    # Call functions
    weekday = zellers_congruence(day, month, year)
    age = calculate_age(day, month, year)

    print(f"\nYou were born on a {weekday}.")
    print(f"You are {age} years old.")

except ValueError:
    print("Invalid input. Please enter numeric values.")
