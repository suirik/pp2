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

### **5. Practice 5: Python Regular Expressions (RegEx)**
This module focuses on mastering pattern matching and data extraction using Python's `re` library.

#### **RegEx Exercises**
* **Pattern Matching**: Implementing rules to match specific sequences, such as 'a' followed by varying numbers of 'b's.
* **Text Transformation**: Converting between naming conventions like `snake_case` and `camelCase` using `re.sub()`.
* **String Parsing**: Splitting strings at uppercase letters and inserting spaces between capitalized words.

#### **Practical Exercise: Receipt Parsing**
* **receipt_parser.py**: A specialized script for extracting structured data from pharmacy receipt text (`raw.txt`).
* **Data Extraction**: Using complex RegEx patterns to identify BIN numbers, transaction dates, and itemized costs.
* **Output Formatting**: Converting raw unstructured text into a structured JSON-like summary of items and totals.

---

### **6. Practice 6: File & Directory Management**
This module demonstrates system-level interactions and functional programming logic.

#### **File Handling**
* **write_files.py**: Creating and writing sample data using `open()`.
* **read_files.py**: Reading, printing, and appending data to existing text files.
* **copy_delete_files.py**: Managing file backups with `shutil` and safe deletion with `os.remove()`.

#### **Directory Management**
* **create_list_dirs.py**: Generating nested directory structures and filtering files by extension.
* **move_files.py**: Automating the movement of files between different folders using `shutil.move()`.

#### **Built-in Functions**
* **map_filter_reduce.py**: Using `map()` for transformations, `filter()` for extraction, and `reduce()` for aggregation.
* **enumerate_zip_examples.py**: Implementing paired iteration and demonstrating dynamic type checking with `isinstance()`.

---

### **7. Practice 7: Python & PostgreSQL PhoneBook**

#### **Project Structure**
* **phonebook.py**: The main application logic and user menu.
* **connect.py**: Handles the connection and error handling for the PostgreSQL server.
* **config.py**: Stores database credentials (host, user, password).
* **contacts.csv**: Data file used for bulk uploading contacts.

#### Key Features
1. **Insert from CSV**: Automatically populates the database from a `.csv` file.
2. **Interactive Search**: Find contacts using name patterns or phone prefixes.
3. **Safe Deletion**: Remove contacts by username or phone number.
4. **Data Persistence**: Uses `commit()` to ensure all changes are saved permanently.

---

### **8. Practice 8: PostgreSQL Functions & Stored Procedures**

#### **SQL Layer: PL/pgSQL**
In this section, logic was implemented using PostgreSQL's procedural language to handle complex operations.
#### **Functions (functions.sql)**:
Pattern Matching: Returning a table of records matching a substring in names or phone numbers.
Pagination: Implementing data retrieval in chunks using LIMIT and OFFSET to optimize performance.
#### **Stored Procedures (procedures.sql)**:
Upsert Logic: A procedure that automatically updates an existing contact or inserts a new one if it doesn't exist.
Bulk Insert & Validation: Using LOOP and IF logic to process multiple entries while validating data correctness.
Safe Deletion: A procedure to remove records based on either a username or a phone number.
#### **Python Layer: Application Logic**
**phonebook.py**: Refactored the main application to interface with the new SQL functions and procedures.
**connect.py**: Refined the database connection module for better error handling during function calls.
**config.py**: Managed database credentials securely (excluded via .gitignore).

---

### **9. Practice 9: Game Development with Pygame**

#### **1. Mickey's Clock**
A digital-style analog clock featuring Mickey Mouse's hands.
- **Functionality:** Synchronizes with the local system time.
- **Controls:** Automatically updates every second.
- **Key Concepts:** Image rotation (`pygame.transform.rotate`) and time-to-angle conversion.

#### **2. Music Player**
A fully functional music player with a custom keyboard controller.
- **Controls:**
  - `P`: Play
  - `S`: Stop
  - `N`: Next track
  - `B`: Previous track (Back)
- **Key Concepts:** `pygame.mixer` for audio management and playlist indexing.

#### **3. Moving Ball Game**
A simple interactive game where you control a red ball.
- **Controls:** Arrow keys (Up, Down, Left, Right).
- **Functionality:** The ball moves in 20-pixel increments and is blocked from leaving the screen boundaries.
- **Key Concepts:** Coordinate systems and boundary collision detection.

---

### **10. Practice 10: Advanced Game Development with Pygame**

##  Games Included

#### **1. Racer**
A high-speed driving game where you must dodge enemies and collect coins.
- **Objective:** Dodge the "Enemy" car and collect "Coins" to increase your score.
- **Controls:** Left/Right Arrow keys.
- **Key Features:** Random enemy spawning, scrolling background, and sound effects.

#### **2. Snake** 
The classic arcade game.
- **Objective:** Eat food to grow longer without hitting the walls or your own tail.
- **Controls:** Arrow keys (Up, Down, Left, Right).
- **Key Features:** Dynamic score display, speed increases as you grow, and boundary logic.

#### **3. Paint** 
A simple drawing application.
- **Objective:** Draw shapes and free-hand lines on a canvas.
- **Features:**
  - Change colors and brush sizes.
  - Draw circles, rectangles, and lines.
  - Clear the screen option.
- **Controls:** Mouse clicks and specific keyboard shortcuts for tools.

---

### **11. Practice 11: Advanced Pygame Mechanics**

##  Game Extensions

#### **1. Racer (Enhanced)**
- **Weighted Coins:** Coins now spawn with different "weights" (values). Collecting a heavy coin provides more points than a standard one.
- **Dynamic Difficulty:** The game tracks your progress. Once you collect **N** coins, the enemy vehicle's speed increases, making the game progressively harder.
- **Key Features:** Sprite groups, random coordinate generation, and speed increment logic.

#### **2. Snake (Enhanced)**
- **Multi-Weight Food:** Food items now have varying nutritional values. Some make the snake grow more than others.
- **Disappearing Food:** Some food items are now on a **Timer**. If you don't reach the food before the timer expires, it disappears and respawns elsewhere.
- **Key Features:** `pygame.time.get_ticks()` for timers and coordinate re-randomization.

#### **3. Paint (Enhanced)**
- **Advanced Geometry:** Beyond basic lines and circles, the toolkit now includes:
  - **Square:** Precise equal-side rectangles.
  - **Right Triangle:** 90-degree angular shapes.
  - **Equilateral Triangle:** Calculated points for equal side lengths.
  - **Rhombus:** Diamond-shaped polygons.
- **Key Features:** `pygame.draw.polygon()` and coordinate math.

---


1. **Stage all changes:**
   * `git add .`
2. **Commit with a clear message:**
   * `git commit -m "Add Practice examples"`
3. **Push to the remote repository:**
   * `git push origin main`
