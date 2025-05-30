import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # fill people dictionary
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # fill names dictionary
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # fill names dictionary
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # fill movies dictionary in people dictionary
                people[row["person_id"]]["movies"].add(row["movie_id"])
                # fill stars dictionary in movies dictionary
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # source => return value in person_id format
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    # target => return value in person_id format
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Initialize frontier to just the starting position => source
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier() # Queue is used for Breadth-First Search
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()
       
    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            raise None

        # Choose a node from the frontier
        node = frontier.remove()

        # If node is the goal, then we have a solution as a path => target
        if node.state == target:
            path = []
            # Backtrack to construct the path
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(
                    state=person_id,    # The new actor we're moving to
                    parent=node,        # Previous actor's node
                    action=movie_id     # The movie that connects them
                )
                frontier.add(child)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    # person_ids list to store all sets of actors' ids with the given name in names dictionary
    person_ids = list(names.get(name.lower(), set()))
    # If no person_ids found, return None
    if len(person_ids) == 0:
        return None
    # If more than one person_id found, prompt the user to choose one
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    # If only one person_id found, return it = the first element of person_ids list
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    # movie_ids are the commmon ground to identify the neighbors
    # use inputted person_id to map with key in from movies table to find movie_ids
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        # use collected movie_ids to find the appropriate data pairs from stars table
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors    

"""
This construct is particularly useful for organizing code and ensuring 
that certain parts of your script (like tests or main logic) 
don't run unintentionally when the file is imported elsewhere.
"""
if __name__ == "__main__":
    main()
