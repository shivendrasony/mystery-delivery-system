# Mystery Delivery System

A Python-based logistics simulator for assigning packages to the nearest
delivery agent and generating a delivery performance report.

## Features

- Reads package, warehouse, and agent data from JSON files.
- Calculates Euclidean distance between coordinates.
- Assigns each package to the nearest agent based on warehouse location.
- Calculates delivery distance for each package.
- Calculates total distance and average distance per package for each agent.
- Identifies the most efficient agent.
- Validates that all packages are delivered.
- Generates the final result in `report.json`.
- Displays ASCII-style delivery routes for each package.
- Exports the top-performing agent to `top_performer.csv`.
- Simulates random delivery delays between 5 and 20 minutes.
- Supports a new agent joining during the delivery process.

## Project Structure

```text
Python Assignment -2026/
│
├── main.py
├── base_case.json
├── report.json
├── top_performer.csv
├── README.md
├── Python Assignment(Delivery System).pdf
│
└── Python Assignment(Delivery System Test Cases)/
    ├── test_case_1.json
    ├── test_case_2.json
    ├── ...
    └── test_case_10.json
```

## Assumptions

1. An agent is assigned to a package based on the minimum Euclidean
distance between the agent and the package's warehouse.

2. Delivery distance is calculated from the package warehouse to its
destination. The agent-to-warehouse distance is used only for
assigning the nearest agent.

3. Efficiency is calculated as:

    Average Distance = Total Distance / Packages Delivered

4. The agent with the lowest average distance per delivered package is
considered the most efficient agent.

5. If two agents have exactly the same distance while assigning a package,
the first agent encountered in the input order is selected.

6. The solution supports both the base-case JSON structure and the provided
test-case structure by normalizing the input data.

7. Random delivery delay is simulated as a value between 5 and 20 minutes
for each package.

8. A new agent can join after a configurable number of packages. In the
current simulation, agent A4 joins after the first 3 packages and is
available for subsequent package assignments.


## How to Run

Run the base case:

    python main.py

Run a specific test case:

    python main.py "Python Assignment(Delivery System Test Cases)/test_case_1.json"

Example for Test Case 10:

    python main.py "Python Assignment(Delivery System Test Cases)/test_case_10.json"

The generated result is saved to:

    report.json

The top-performing agent is also exported to:

    top_performer.csv


## Validation

The program validates that the number of delivered packages matches the
number of packages present in the input.

If there is a mismatch, the program raises an error.

The solution was tested with all 10 provided test cases.

Technologies
    
Python

JSON

Built-in Python json module

Built-in Python math module

Built-in Python csv module

Built-in Python random module