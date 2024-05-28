
# Smart Seating Arrangement

Smart Seating Arrangement is a Python application designed to optimize seating arrangements in a classroom setting. The application uses a genetic algorithm to find the best seating plan based on a set of user-defined constraints. Users can input a list of students, specify the number of rows and columns, and add constraints such as preferred seating partners, undesired neighbors, and preferred seating locations. The application then calculates the optimal seating arrangement and allows for adjustments and ratings.

## Features
- Input a list of students and classroom dimensions
- Add constraints for seating preferences:
  - "Not next to" constraints
  - "Next to" constraints
  - Preferred location constraints
- Calculate the optimal seating arrangement using a genetic algorithm
- Display the seating arrangement and the constraints considered
- Recalculate seating arrangements as needed
- Rate the seating arrangement
- Display current constraints and allow for their removal

## Requirements
- Python 3.x
- Tkinter (for the UI)
- NumPy (for array manipulation)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Miri-Shtul/Smart-Seating-Arrangement.git
   ```
2. Navigate to the project directory:
   ```bash
   cd smart-seating-arrangement
   ```
3. Install the required dependencies:
   ```bash
   pip install numpy
   ```

## Usage
Run the application:
```bash
python main.py
```

## How to Use
1. **Input Students and Dimensions:**
   - Enter a comma-separated list of student names.
   - Enter the number of rows and columns in the classroom.
   - Click "Submit Students" to save the input.

2. **Add Constraints:**
   - Click "Add Constraints" to open the constraint window.
   - Select a student from the dropdown.
   - Choose the type of constraint ("Not next to", "Next to", "Preferred location").
   - For "Not next to" and "Next to" constraints, select one or more students from the list.
   - For "Preferred location" constraints, enter the preferred row and column as "row,col".
   - Click "Add Constraint" to save the constraint.

3. **Calculate Seating:**
   - Click "Calculate Seating" to compute the optimal seating arrangement.
   - The result will be displayed in a text box.
   - Rate the seating arrangement if desired.

4. **Manage Constraints:**
   - Current constraints are displayed in a list.
   - Select a constraint and click "Remove Selected Constraint" to delete it.

## License
This project is licensed under the MIT License.

