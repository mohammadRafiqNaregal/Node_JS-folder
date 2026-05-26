# ============================================================
# PYTHON BASICS — Complete Cheatsheet for JS/TS Developers
# ============================================================
# Run this file: python3 python-basics-cheatsheet.py


# ────────────────────────────────────────────────────────────
# 1. VARIABLES (No let/const/var — just assign)
# ────────────────────────────────────────────────────────────

name = "Rafi"            # string (like: let name = "Rafi")
age = 25                 # int
height = 5.9             # float
is_developer = True      # bool (True/False, not true/false)
nothing = None           # null equivalent (None, not null/undefined)

# Multiple assignment
x, y, z = 1, 2, 3       # like: const [x, y, z] = [1, 2, 3]
a = b = c = 0           # all set to 0

# Constants — Python has NO const keyword. Convention: ALL_CAPS
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com"

# Type hints (optional, like TypeScript annotations)
username: str = "rafi"
count: int = 42
prices: list[float] = [9.99, 19.99]


# ────────────────────────────────────────────────────────────
# 2. DATA TYPES
# ────────────────────────────────────────────────────────────

# Strings
greeting = "Hello"
multiline = """
This is a
multiline string
"""
# f-strings (like template literals `${}`)
message = f"Hello {name}, you are {age} years old"
# JS:     `Hello ${name}, you are ${age} years old`

# String methods
"hello".upper()          # "HELLO"
"HELLO".lower()          # "hello"
"hello world".split()    # ["hello", "world"]
" hi ".strip()           # "hi" (like .trim())
"hello".replace("l", "L")  # "heLLo"
"hello".startswith("he")   # True
len("hello")              # 5 (not .length — len() is a function)

# Numbers
integer = 42
floating = 3.14
big_num = 1_000_000      # underscores for readability (like JS)

# Type conversion
int("42")                # 42
str(42)                  # "42"
float("3.14")            # 3.14
bool(0)                  # False
bool("")                 # False
bool([])                 # False (empty collections are falsy)


# ────────────────────────────────────────────────────────────
# 3. OPERATORS
# ────────────────────────────────────────────────────────────

# Arithmetic (same as JS)
# +  -  *  /  %

# Different from JS:
result = 10 / 3          # 3.333... (always float division)
result = 10 // 3         # 3 (integer/floor division — no JS equivalent)
result = 2 ** 10         # 1024 (exponent — JS uses ** too)

# Comparison
# ==  !=  <  >  <=  >=   (same as JS)
# NOTE: == compares VALUE (like === in JS). No === in Python.
# Python doesn't have type coercion issues like JS.

# Logical (words, not symbols!)
# JS:     &&     ||     !
# Python: and    or     not

if age > 18 and is_developer:
    print("Adult developer")

if not is_developer:
    print("Not a developer")

# Identity (object reference comparison)
# JS:   ===  (for primitives)
# Python: is / is not (checks if same object in memory)
a_list = [1, 2]
b_list = [1, 2]
print(a_list == b_list)    # True  (same values)
print(a_list is b_list)    # False (different objects)

# Ternary / Conditional expression
# JS:   const status = age >= 18 ? "adult" : "minor"
status = "adult" if age >= 18 else "minor"


# ────────────────────────────────────────────────────────────
# 4. COLLECTIONS
# ────────────────────────────────────────────────────────────

# --- LIST (like JS Array) ---
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")       # push
fruits.insert(0, "kiwi")     # insert at index
fruits.pop()                 # remove last
fruits.pop(0)                # remove at index
fruits.remove("banana")      # remove by value
len(fruits)                  # length (not .length)
fruits[0]                    # first item
fruits[-1]                   # last item (no .at(-1) needed!)
fruits[1:3]                  # slice [index 1, 2] (not including 3)

# List comprehension (Python's superpower — like .map + .filter in one)
# JS:   const doubled = numbers.map(n => n * 2)
numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]               # [2, 4, 6, 8, 10]
evens = [n for n in numbers if n % 2 == 0]       # [2, 4]
# Combined map + filter:
big_doubled = [n * 2 for n in numbers if n > 2]  # [6, 8, 10]

# --- DICTIONARY (like JS Object / Map) ---
user = {
    "name": "Rafi",
    "age": 25,
    "skills": ["React", "Python"],
}
user["name"]                 # "Rafi" (bracket notation only, no dot notation)
user.get("email", "N/A")    # "N/A" (safe access with default — like ?? in JS)
user["email"] = "rafi@example.com"  # add/update
del user["age"]              # delete key

# Dict methods
user.keys()                  # dict_keys(["name", "skills", "email"])
user.values()                # dict_values([...])
user.items()                 # dict_items([("name", "Rafi"), ...])  key-value pairs
"name" in user               # True (check if key exists)

# Dict comprehension
# JS:  Object.fromEntries(arr.map(x => [x, x.length]))
words = ["hello", "world", "python"]
word_lengths = {w: len(w) for w in words}  # {"hello": 5, "world": 5, "python": 6}

# --- TUPLE (immutable list) ---
point = (10, 20)
lat, lng = point             # destructuring

# --- SET (unique values, like JS Set) ---
unique_nums = {1, 2, 3, 3, 3}   # {1, 2, 3}
unique_nums.add(4)
unique_nums.discard(2)
# Set operations
a_set = {1, 2, 3}
b_set = {2, 3, 4}
a_set | b_set                # union: {1, 2, 3, 4}
a_set & b_set                # intersection: {2, 3}
a_set - b_set                # difference: {1}


# ────────────────────────────────────────────────────────────
# 5. CONTROL FLOW
# ────────────────────────────────────────────────────────────

# --- IF/ELIF/ELSE (no braces, use indentation!) ---
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# --- MATCH (like switch, Python 3.10+) ---
command = "quit"
match command:
    case "start":
        print("Starting...")
    case "stop" | "quit":     # multiple values
        print("Stopping...")
    case _:                   # default
        print("Unknown command")

# --- FOR LOOP ---
# Iterating a list (like for...of in JS)
for fruit in fruits:
    print(fruit)

# With index (like .forEach((item, index) => ...))
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# Range (like for(let i=0; i<10; i++))
for i in range(10):          # 0 to 9
    print(i)

for i in range(2, 10):      # 2 to 9
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8 (step of 2)
    print(i)

# Iterating a dict
for key, value in user.items():
    print(f"{key}: {value}")

# --- WHILE LOOP ---
count = 0
while count < 5:
    print(count)
    count += 1
    # NOTE: no count++ in Python, use count += 1

# break, continue — same as JS
for i in range(10):
    if i == 3:
        continue     # skip 3
    if i == 7:
        break        # stop at 7
    print(i)


# ────────────────────────────────────────────────────────────
# 6. FUNCTIONS
# ────────────────────────────────────────────────────────────

# Basic function
# JS:  function greet(name) { return `Hello ${name}` }
def greet(name):
    return f"Hello {name}"

# Default parameters
def greet_with_default(name="World"):
    return f"Hello {name}"

# Multiple return values (returns a tuple)
def get_dimensions():
    return 1920, 1080          # returns tuple (1920, 1080)

width, height = get_dimensions()  # destructuring

# Keyword arguments (named parameters — Python's killer feature)
def create_user(name, age, email="", role="user"):
    return {"name": name, "age": age, "email": email, "role": role}

# Can call with named args in any order:
user1 = create_user("Rafi", 25, role="admin", email="rafi@email.com")

# *args — variable positional args (like ...rest in JS)
def sum_all(*numbers):
    return sum(numbers)

sum_all(1, 2, 3, 4)        # 10

# **kwargs — variable keyword args (like spreading an object)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Rafi", age=25, city="Mumbai")

# Lambda (like arrow functions, but single expression only)
# JS:  const double = (x) => x * 2
double = lambda x: x * 2
double(5)  # 10

# Type-hinted function (like TypeScript)
def add(a: int, b: int) -> int:
    return a + b

def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}


# ────────────────────────────────────────────────────────────
# 7. CLASSES
# ────────────────────────────────────────────────────────────

# JS:
# class User {
#   constructor(name, age) {
#     this.name = name;
#     this.age = age;
#   }
#   greet() { return `Hi, I'm ${this.name}` }
# }

class User:
    # Constructor
    def __init__(self, name: str, age: int):
        self.name = name       # this.name = name
        self.age = age         # self = this in Python

    # Method
    def greet(self) -> str:    # methods always take `self` as first param
        return f"Hi, I'm {self.name}"

    # String representation (like toString())
    def __repr__(self) -> str:
        return f"User(name={self.name}, age={self.age})"

# Usage
user1 = User("Rafi", 25)      # no `new` keyword!
print(user1.greet())
print(user1.name)

# Inheritance
class AdminUser(User):         # class AdminUser extends User
    def __init__(self, name: str, age: int, permissions: list[str]):
        super().__init__(name, age)   # super()
        self.permissions = permissions

    def has_permission(self, perm: str) -> bool:
        return perm in self.permissions


# ────────────────────────────────────────────────────────────
# 8. ERROR HANDLING
# ────────────────────────────────────────────────────────────

# JS:   try { } catch (error) { } finally { }
# Python: try / except / finally

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
except Exception as e:         # catch-all (like catch(error))
    print(f"Unexpected error: {e}")
finally:
    print("This always runs")

# Raising errors (like `throw new Error(...)`)
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# ────────────────────────────────────────────────────────────
# 9. FILE I/O
# ────────────────────────────────────────────────────────────

# Writing a file
with open("output.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# Reading a file
with open("output.txt", "r") as f:
    content = f.read()         # entire file as string
    # or: lines = f.readlines()  # list of lines

# `with` = context manager — auto-closes the file (like try-with-resources in Java)
# No need to manually call f.close()

# JSON (like JSON.parse / JSON.stringify)
import json

data = {"name": "Rafi", "age": 25}
json_string = json.dumps(data, indent=2)   # JSON.stringify(data, null, 2)
parsed = json.loads(json_string)            # JSON.parse(jsonString)

# Read/write JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)


# ────────────────────────────────────────────────────────────
# 10. MODULES & IMPORTS
# ────────────────────────────────────────────────────────────

# Built-in modules
import os                     # like: import os from 'os'
import sys
from pathlib import Path      # like: import { Path } from 'pathlib'
from datetime import datetime, timedelta   # multiple imports

# Import with alias
import json as j              # like: import json as j
from collections import defaultdict as dd

# Your own modules
# utils.py:  def helper(): ...
# main.py:   from utils import helper

# Relative imports (inside a package)
# from .utils import helper       # from same package
# from ..config import settings   # from parent package


# ────────────────────────────────────────────────────────────
# 11. COMMON PATTERNS — JS → Python
# ────────────────────────────────────────────────────────────

# --- Array methods → Python equivalents ---

items = [3, 1, 4, 1, 5, 9, 2, 6]

# .map()    → list comprehension or map()
squared = [x**2 for x in items]

# .filter() → list comprehension with condition
big = [x for x in items if x > 4]

# .reduce() → functools.reduce or just a loop
from functools import reduce
total = reduce(lambda acc, x: acc + x, items, 0)
# Or simpler: total = sum(items)

# .find()   → next() with generator
first_big = next((x for x in items if x > 4), None)  # None = default

# .some()   → any()
has_big = any(x > 4 for x in items)    # True

# .every()  → all()
all_positive = all(x > 0 for x in items)  # True

# .includes() → in operator
has_five = 5 in items                    # True

# .sort()   → sorted() (returns new) or .sort() (in-place)
sorted_items = sorted(items)             # new list
items.sort()                             # mutates in place

# .reverse() → reversed() or .reverse()
reversed_items = list(reversed(items))

# .join()   → "sep".join(list)  (note: method is on the STRING, not the list)
words_list = ["hello", "world"]
sentence = " ".join(words_list)          # "hello world"
# JS: words.join(" ")

# .split()
"hello world".split(" ")                # ["hello", "world"]

# Spread operator → unpacking
# JS:   const merged = [...arr1, ...arr2]
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
merged = [*arr1, *arr2]                 # [1, 2, 3, 4, 5, 6]

# Object spread → dict unpacking
# JS:   const merged = { ...obj1, ...obj2 }
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged_dict = {**dict1, **dict2}        # {"a": 1, "b": 3, "c": 4}

# Destructuring
# JS:   const { name, age } = user
# Python: no direct object destructuring, but for tuples/lists:
first, *rest = [1, 2, 3, 4, 5]          # first=1, rest=[2,3,4,5]
a, _, c = (1, 2, 3)                      # _ means "ignore this"

# Optional chaining
# JS:   user?.address?.city
# Python: no ?. operator — use .get() for dicts or try/except
city = user.get("address", {}).get("city", "Unknown")

# Nullish coalescing
# JS:   const val = input ?? "default"
# Python: use `or` (but careful: it's falsy-check, not just None)
val = None
result = val or "default"                # "default"
# For strictly None only:
result = val if val is not None else "default"


# ────────────────────────────────────────────────────────────
# 12. STRING FORMATTING
# ────────────────────────────────────────────────────────────

name = "Rafi"
age = 25

# f-string (preferred — like template literals)
print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")
print(f"Price: ${19.99:.2f}")          # formatted float
print(f"{'hello':>10}")                 # right-aligned, padded to 10 chars

# .format() method (older style)
print("Name: {}, Age: {}".format(name, age))


# ────────────────────────────────────────────────────────────
# 13. USEFUL BUILT-IN FUNCTIONS
# ────────────────────────────────────────────────────────────

# len()     — length of anything
len([1, 2, 3])          # 3
len("hello")            # 5
len({"a": 1})           # 1

# range()   — generate number sequence
list(range(5))          # [0, 1, 2, 3, 4]
list(range(2, 8))       # [2, 3, 4, 5, 6, 7]

# enumerate() — loop with index
for i, item in enumerate(["a", "b", "c"]):
    print(f"{i}: {item}")

# zip() — combine two lists (like lodash _.zip)
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# sorted(), min(), max(), sum()
sorted([3, 1, 2])      # [1, 2, 3]
min([3, 1, 2])          # 1
max([3, 1, 2])          # 3
sum([1, 2, 3])          # 6

# type() — check type (like typeof)
type(42)                # <class 'int'>
type("hi")              # <class 'str'>
isinstance(42, int)     # True (preferred for type checking)

# input() — read user input (like readline in Node)
# user_input = input("Enter your name: ")

# print() — console.log equivalent
print("Hello")
print("a", "b", "c")           # a b c (space-separated)
print("a", "b", sep=", ")      # a, b
print("no newline", end="")    # suppress newline


# ────────────────────────────────────────────────────────────
# 14. MINI PROJECT — Putting It All Together
# ────────────────────────────────────────────────────────────

def main():
    """A simple contact book program."""

    contacts: list[dict[str, str]] = []

    def add_contact(name: str, email: str, phone: str = ""):
        contact = {"name": name, "email": email, "phone": phone}
        contacts.append(contact)
        print(f"✓ Added {name}")

    def find_contact(search: str) -> list[dict[str, str]]:
        return [
            c for c in contacts
            if search.lower() in c["name"].lower()
            or search.lower() in c["email"].lower()
        ]

    def display_all():
        if not contacts:
            print("No contacts yet.")
            return
        for i, c in enumerate(contacts, start=1):
            print(f"  {i}. {c['name']} — {c['email']} {c['phone']}")

    # Add some contacts
    add_contact("Alice Johnson", "alice@example.com", "555-0101")
    add_contact("Bob Smith", "bob@example.com", "555-0102")
    add_contact("Charlie Brown", "charlie@example.com")

    # Display all
    print("\n📒 All Contacts:")
    display_all()

    # Search
    print("\n🔍 Search for 'bob':")
    results = find_contact("bob")
    for c in results:
        print(f"  Found: {c['name']} ({c['email']})")

    # Summary
    print(f"\nTotal contacts: {len(contacts)}")


# This is Python's equivalent of: if (require.main === module)
# It means: only run main() if this file is executed directly
if __name__ == "__main__":
    main()
