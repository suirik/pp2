#  PP2 PROJECT

**Source:** W3Schools Python Tutorial  

---

##  Project Overview
* This repository is created to practice **basic Python syntax** and **Git workflow**.
* It follows the structure required for the **W3Schools "Topics to Cover"** assignment.

---

##  Project Structure

### **1. Practice 1: Python Basics**
* `hello_world.py` — Basic output examples.
* `variables.py` — Variable declaration and assignment.
* `data_types.py` — Demonstration of different Python data types.
* `strings.py` — String manipulation and methods.
* `numbers.py` — Working with integers and floats.

---

### **2. Practice 2: Control Flow & Logic**
In this section, I implemented more complex logic to make programs dynamic.

#### ** Boolean & Comparison**
* **`boolean/`** — Learning how to evaluate expressions to `True` or `False`.
* Using logical operators like `and`, `or`, and `not` to combine conditions.

#### ** Conditionals (If...Else)**
* **`if_else/`** — Implementing decision-making paths.
* Using `if`, `elif`, and `else` to handle multiple scenarios in the code.

#### ** Loops & Iteration**
* **`loops/`** — Automating repetitive tasks with `for` and `while` loops.
* **Loop Control**: Using `break` to exit a loop and `continue` to skip an iteration.

---

### **3. Practice 3: Functions and OOP**
This module covers the implementation of modular code using functions and the principles of Object-Oriented Programming (OOP) in Python.

#### ** Functions**
* **basic_functions.py**: Definition and invocation of simple functions.
* **function_arguments.py**: Handling parameters and default arguments.
* **return_values.py**: Capturing data sent back from functions using `return`.
* **args_kwargs.py**: Implementation of flexible arguments using `*args` and `**kwargs`.

#### ** Lambda**
* **lambda_basics.py**: Syntax for anonymous one-line functions.
* **lambda_with_map.py**: Applying logic to every item in a list.
* **lambda_with_filter.py**: Extracting specific items from a collection based on a condition.
* **lambda_with_sorted.py**: Custom sorting logic using lambda keys.

#### ** Classes**
* **class_definition.py**: Creating blueprints and instantiating objects.
* **init_method.py**: Using the `__init__` constructor to initialize object attributes.
* **class_methods.py**: Defining behaviors (functions) inside a class.
* **class_variables.py**: Understanding the difference between instance and class-level data.

#### ** Inheritance**
* **inheritance_basics.py**: Creating parent and child class relationships.
* **super_function.py**: Using `super()` to access parent class methods.
* **method_overriding.py**: Modifying inherited methods in a child class.
* **multiple_inheritance.py**: Deriving a class from multiple parent sources.

---

### **4. Practice 4: Advanced Python Topics**
This module covers advanced concepts including generators for memory efficiency, date manipulation, mathematical operations, and JSON handling.

#### **Iterators and Generators**
* **generators.py**: Implementation of functions that use the `yield` keyword to return sequences.
* **Squares Generator**: Generating a sequence of squares up to $N$.
* **Logic Filtering**: Creating generators that yield even numbers or numbers divisible by 3 and 4.
* **Countdown**: Implementing a reverse generator that counts down to zero.

#### **Python Dates**
* **dates.py**: Utilizing the `datetime` and `timedelta` modules to manage time-based data.
* **Date Arithmetic**: Subtracting days from the current date and calculating differences in seconds.
* **Time Management**: Printing yesterday, today, and tomorrow, and removing microseconds from time objects.

#### **Python Math**
* **math.py**: Applying the built-in `math` library for precise geometric calculations.
* **Conversion**: Transforming degrees into radians using `math.radians()`.
* **Area Formulas**: Calculating the area of trapezoids, regular polygons, and parallelograms using formulas like $Area = \frac{n \times s^2}{4 \times \tan(\frac{\pi}{n})}$.

#### **Python JSON**
* **json_task.py**: Parsing and processing JSON data to create structured reports.
* **Parsing**: Converting JSON strings into Python dictionaries with `json.loads()`.
* **Data Visualization**: Iterating through nested JSON objects to display "Interface Status" in an aligned tabular format.

---

##  How to Save Changes to GitHub
To sync this project with your GitHub account, use these commands in your terminal:

1. **Stage all changes:**
   * `git add .`
2. **Commit with a clear message:**
   * `git commit -m "Add Practice examples"`
3. **Push to the remote repository:**
   * `git push origin main`
