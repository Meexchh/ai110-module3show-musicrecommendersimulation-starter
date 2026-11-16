"""
Command line runner for the Music Recommender Simulation.

Run from the project root:  python -m src.main
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

# Starter profile plus three distinct taste profiles.
PROFILES = {
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
}

# Edge cases meant to trick the scoring logic.
ADVERSARIAL_PROFILES = {
    "Conflicting: high energy + sad mood": {"genre": "blues", "mood": "sad", "energy": 0.9},
    "Genre not in catalog (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.8},
    "Middle-of-the-road energy, no genre": {"genre": "", "mood": "chill", "energy": 0.5},
}


def print_recommendations(title: str, user_prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    """Print a titled, readable top-k list with scores and reasons."""
    print("=" * 60)
    print(f"{title}  ->  {user_prefs}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k, weights=weights), start=1
    ):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print("##### STANDARD PROFILES #####\n")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    print("##### ADVERSARIAL PROFILES #####\n")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        print_recommendations(name, prefs, songs)

    print("##### EXPERIMENT: WEIGHT SHIFT (genre 2.0 -> 1.0, energy 1.0 -> 2.0) #####\n")
    shifted = {**DEFAULT_WEIGHTS, "genre": DEFAULT_WEIGHTS["genre"] / 2, "energy": DEFAULT_WEIGHTS["energy"] * 2}
    for name in ("Default Pop/Happy", "High-Energy Pop"):
        print_recommendations(f"{name} (shifted weights)", PROFILES[name], songs, weights=shifted)


if __name__ == "__main__":
    main()
