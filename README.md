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

## Project Structure

```text
Python Assignment -2026/
│
├── main.py
├── base_case.json
├── report.json
├── README.md
├── Python Assignment(Delivery System).pdf
│
└── Python Assignment(Delivery System Test Cases)/
    ├── test_case_1.json
    ├── test_case_2.json
    ├── ...
    └── test_case_10.json