import json
import math
import sys

def normalize_agents(agents):
    if isinstance(agents, dict):
        return agents

    return {
        agent["id"]: agent["location"]
        for agent in agents
    }


def normalize_warehouses(warehouses):
    if isinstance(warehouses, dict):
        return warehouses

    return {
        warehouse["id"]: warehouse["location"]
        for warehouse in warehouses
    }


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_agent(warehouse_location, agents):
    nearest_agent = None
    minimum_distance = float("inf")

    for agent_id, agent_location in agents.items():
        distance = calculate_distance(
            agent_location,
            warehouse_location
        )

        if distance < minimum_distance:
            minimum_distance = distance
            nearest_agent = agent_id

    return nearest_agent


def assign_packages(packages, warehouses, agents):
    assignments = {}

    for package in packages:
        package_id = package["id"]

        # Support both input formats
        warehouse_id = package.get("warehouse") or package.get("warehouse_id")

        warehouse_location = warehouses[warehouse_id]

        nearest_agent = find_nearest_agent(
            warehouse_location,
            agents
        )

        assignments[package_id] = nearest_agent

    return assignments

def group_packages_by_agent(assignments):
    agent_packages = {}

    for package_id, agent_id in assignments.items():
        if agent_id not in agent_packages:
            agent_packages[agent_id] = []

        agent_packages[agent_id].append(package_id)

    return agent_packages

# Assumption:
# Delivery distance is calculated from the package warehouse
# to its destination. The agent-to-warehouse distance is used
# only for assigning the nearest agent.

def calculate_package_distance(package, warehouses):
    # Support both package formats
    warehouse_id = package.get("warehouse") or package.get("warehouse_id")

    warehouse_location = warehouses[warehouse_id]
    destination = package["destination"]

    return calculate_distance(
        warehouse_location,
        destination
    )

def calculate_agent_totals(packages, assignments, warehouses):
    agent_totals = {}

    for package in packages:
        package_id = package["id"]
        agent_id = assignments[package_id]

        distance = calculate_package_distance(
            package,
            warehouses
        )

        if agent_id not in agent_totals:
            agent_totals[agent_id] = {
                "packages_delivered": 0,
                "total_distance": 0.0
            }

        agent_totals[agent_id]["packages_delivered"] += 1
        agent_totals[agent_id]["total_distance"] += distance

    return agent_totals

def calculate_efficiency(agent_totals):
    for agent_id, details in agent_totals.items():
        packages_delivered = details["packages_delivered"]
        total_distance = details["total_distance"]

        if packages_delivered > 0:
            details["efficiency"] = (
                total_distance / packages_delivered
            )
        else:
            details["efficiency"] = 0.0

    return agent_totals

# Assumption:
# An agent with lower average distance per delivered package
# is considered more efficient.

def find_best_agent(agent_totals):
    if not agent_totals:
        return None

    return min(
        agent_totals,
        key=lambda agent_id: agent_totals[agent_id]["efficiency"]
    )

def generate_report(agent_totals, best_agent):
    report = {}

    for agent_id, details in agent_totals.items():
        report[agent_id] = {
            "packages_delivered": details["packages_delivered"],
            "total_distance": round(details["total_distance"], 2),
            "efficiency": round(details["efficiency"], 2)
        }

    report["best_agent"] = best_agent

    return report

def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    warehouses = normalize_warehouses(data["warehouses"])
    agents = normalize_agents(data["agents"])
    packages = data["packages"]

    return warehouses, agents, packages

def validate_delivery_count(packages, agent_totals):
    total_packages = len(packages)

    delivered_packages = sum(
        details["packages_delivered"]
        for details in agent_totals.values()
    )

    if total_packages != delivered_packages:
        raise ValueError(
            f"Package count mismatch: "
            f"{total_packages} packages found, "
            f"but {delivered_packages} delivered."
        )

    return True

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "base_case.json"

    warehouses, agents, packages = load_data(file_path)
    try:
        warehouses, agents, packages = load_data(file_path)
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file -> {file_path}")
        return

    assignments = assign_packages(
        packages,
        warehouses,
        agents
    )

    agent_totals = calculate_agent_totals(
        packages,
        assignments,
        warehouses
    )

    validate_delivery_count(
        packages,
        agent_totals
    )

    agent_totals = calculate_efficiency(agent_totals)

    best_agent = find_best_agent(agent_totals)

    report = generate_report(
        agent_totals,
        best_agent
    )

    # Save the final report to report.json
    with open("report.json", "w") as file:
        json.dump(report, file, indent=4)

    print("Report saved successfully to report.json")


if __name__ == "__main__":
    main()