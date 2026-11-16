from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_converts_numeric_fields():
    from src.recommender import load_songs

    songs = load_songs("data/songs.csv")
    assert len(songs) >= 10
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)
    assert isinstance(songs[0]["id"], int)


def test_score_song_returns_score_and_reasons():
    from src.recommender import score_song

    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, song)
    assert score == 4.0  # 2.0 genre + 1.0 mood + 1.0 perfect energy
    assert any("genre match" in r for r in reasons)
    assert any("mood match" in r for r in reasons)


def test_energy_rewards_closeness_not_height():
    from src.recommender import score_song

    prefs = {"genre": "x", "mood": "y", "energy": 0.5}
    close, _ = score_song(prefs, {"genre": "a", "mood": "b", "energy": 0.55})
    far_high, _ = score_song(prefs, {"genre": "a", "mood": "b", "energy": 0.95})
    assert close > far_high


def test_recommend_songs_is_sorted_and_limited_to_k():
    from src.recommender import load_songs, recommend_songs

    songs = load_songs("data/songs.csv")
    results = recommend_songs({"genre": "pop", "mood": "happy", "energy": 0.8}, songs, k=3)
    scores = [score for _, score, _ in results]
    assert len(results) == 3
    assert scores == sorted(scores, reverse=True)
