import random
import requests

API_URL = "https://pokeapi.co/api/v2/pokemon/"
MAX_ATTEMPTS = 3

POKEMON_LIST = [
    "pikachu", "charizard", "bulbasaur", "squirtle", "charmander",
    "eevee", "snorlax", "jigglypuff", "mewtwo", "gengar",
]


def get_pokemon(name):
    """Fetch a Pokemon from the API. Raises requests.RequestException on failure."""
    response = requests.get(API_URL + name + "/", timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
    }


def play_round():
    try:
        answer = get_pokemon(random.choice(POKEMON_LIST))
    except requests.RequestException:
        print("Error: Unable to load Pokemon data.")
        return

    height_m = answer["height"] / 10
    weight_kg = answer["weight"] / 10

    print("\nA Pokemon has been selected.")
    print(f"Height: {height_m} meters")
    print(f"Weight: {weight_kg} kilograms")

    attempts = 0
    while attempts < MAX_ATTEMPTS:
        guess = input(f"\nAttempt {attempts + 1}/{MAX_ATTEMPTS}: ").strip().lower()

        if not guess:
            print("Invalid input. Enter a Pokemon name.")
            continue

        try:
            guessed = get_pokemon(guess)
        except requests.HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                print("Invalid input. Pokemon not found.")
                continue
            print("Error: Unable to load Pokemon data.")
            return
        except requests.RequestException:
            print("Error: Unable to load Pokemon data.")
            return

        attempts += 1

        if guessed["name"] == answer["name"]:
            print(f"Correct. The Pokemon is {answer['name'].title()}.")
            return

        print(f"Incorrect. Attempts left: {MAX_ATTEMPTS - attempts}.")

    print(f"Game over. The Pokemon was {answer['name'].title()}.")


def main():
    print("================================")
    print("     WHO'S THAT POKEMON?")
    print("================================")

    while True:
        play_round()
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            break

    print("Goodbye.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")