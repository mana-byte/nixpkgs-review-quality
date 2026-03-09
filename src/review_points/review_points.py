import json

def read_json_file_by_criteria_name(name):
    """Reads a JSON file and returns its content as a Python dictionary."""
    file_path = f"src/review_points/points/{name}.json"
    with open(file_path, 'r') as file:
        return json.load(file)

def create_review_points_dict(criteria_names):
    """Creates a dictionary of review points based on a list of criteria names."""
    points = {}
    for name in criteria_names:
        points[name] = read_json_file_by_criteria_name(name)
    return points

if __name__ == "__main__":
    criteria_names = ["finalAttrs", "meta"]
    review_points_dict = create_review_points_dict(criteria_names)
    print(review_points_dict)

