import json

def read_json_file_by_criteria_name(name):
    """Reads a JSON file and returns its content as a Python dictionary."""
    file_path = f"src/review_points/points/{name}.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found.")
    except json.JSONDecodeError:
        raise Exception(f"File {file_path} is not a valid JSON.")
    except Exception as e:
        raise Exception(f"An error occurred while reading {file_path}: {str(e)}")

def create_review_points_dict(criteria_names):
    """Creates a dictionary of review points based on a list of criteria names."""
    points = {}
    for name in criteria_names:
        try:
            points[name] = read_json_file_by_criteria_name(name)
        except Exception as e:
            continue
    return points

if __name__ == "__main__":
    criteria_names = ["finalAttrs", "meta"]
    review_points_dict = create_review_points_dict(criteria_names)
    print(review_points_dict)

