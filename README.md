# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a small, explainable, content-based music recommender. It reads a 20-song catalog from `data/songs.csv`, compares each song to a user "taste profile" (favorite genre, favorite mood, target energy), gives every song a score, and prints the top 5 with the reasons behind each score. It runs entirely in the terminal and uses only Python's standard library.

---

## How The System Works

**How real platforms do it.** Services like Spotify and YouTube mix two ideas. *Collaborative filtering* looks at the behavior of many users (likes, skips, replays, playlist adds, watch time) and recommends what similar listeners enjoyed, even if it knows nothing about the song itself. *Content-based filtering* looks at the song's own attributes (genre, tempo, energy, mood, acousticness) and recommends songs that are close to what you already like. At scale, platforms blend both, add context like time of day, and re-rank for variety.

**What my version does.** My simulator is purely content-based. It has no other users, so it cannot do collaborative filtering. It prioritizes **matching the vibe I can measure**: a genre match matters most, then a mood match, then how close the song's energy is to what the user wants.

### Features

- **`Song`** uses: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0-1), `tempo_bpm`, `valence` (0-1), `danceability` (0-1), `acousticness` (0-1)
- **`UserProfile`** uses: `favorite_genre`, `favorite_mood`, `target_energy` (0-1), `likes_acoustic`
- The scoring function currently reads only **genre, mood and energy**. Tempo, valence, danceability and acousticness are loaded but not scored yet (see Future Work in the model card).

### Algorithm Recipe

Each song gets points from three rules:

| Rule | Points |
|---|---|
| Genre equals the user's favorite genre | **+2.0** |
| Mood equals the user's favorite mood | **+1.0** |
| Energy closeness: `1.0 x (1 - abs(song_energy - target_energy))` | **0.0 to +1.0** |

The energy rule rewards songs that are **close** to the target, not songs that are simply higher or lower. A perfect energy match earns the full +1.0, and a song 0.5 away earns +0.5. The maximum possible score is **4.0**.

**Scoring rule vs. ranking rule.** `score_song` judges *one* song and explains itself with a list of reasons. `recommend_songs` is the ranking step: it runs the scoring rule on *every* song, sorts the results from highest to lowest, and returns the top `k`. Keeping them separate means I can change the math without touching the sorting.

### Data flow

```
Input (user prefs)  ->  Process (loop over every song in the CSV, call score_song)  ->  Output (sort by score, return top k)
```

### Expected biases

- Genre is worth twice as much as mood, so the system can over-prioritize genre and bury a great mood-and-energy match in a different genre.
- Genre and mood are exact string matches, so "indie pop" gets no credit for a "pop" fan.
- With only 20 songs, many genres have one song, so results get thin after the first few picks.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the tests with:

```bash
pytest
```

The suite covers CSV loading (numeric conversion), the scoring rule (score plus reasons, energy closeness), and ranking order.

---

## Sample Recommendation Output

Default profile (`genre=pop, mood=happy, energy=0.8`), from `python -m src.main`:

```
============================================================
Default Pop/Happy  ->  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.98
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.87
   Because: genre match (+2.0); energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.96
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
4. Calle Sol by Mariposa Luz  [latin/joyful]
   Score: 1.00
   Because: energy 0.80 vs target 0.80 (+1.00)
5. Concrete Crown by Dre Valley  [hip hop/confident]
   Score: 0.98
   Because: energy 0.78 vs target 0.80 (+0.98)
```

Output for the other profiles is in the Experiments section below and in `model_card.md`.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I tested three standard profiles, three adversarial profiles, and one weight-shift experiment. Full terminal output for every run is in `model_card.md`.

**Standard profiles**

```
============================================================
High-Energy Pop  ->  {'genre': 'pop', 'mood': 'intense', 'energy': 0.9}
============================================================
1. Gym Hero by Max Pulse  [pop/intense]
   Score: 3.97
   Because: genre match (+2.0); mood match (+1.0); energy 0.93 vs target 0.90 (+0.97)
2. Sunrise City by Neon Echo  [pop/happy]
   Score: 2.92
   Because: genre match (+2.0); energy 0.82 vs target 0.90 (+0.92)
3. Storm Runner by Voltline  [rock/intense]
   Score: 1.99
   Because: mood match (+1.0); energy 0.91 vs target 0.90 (+0.99)
4. Neon Overdrive by Pulse Theory  [edm/euphoric]
   Score: 0.94
   Because: energy 0.96 vs target 0.90 (+0.94)
5. Iron Cathedral by Black Meridian  [metal/aggressive]
   Score: 0.93
   Because: energy 0.97 vs target 0.90 (+0.93)

============================================================
Chill Lofi  ->  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
============================================================
1. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 4.00
   Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 3.93
   Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 2.95
   Because: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95)
4. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 1.93
   Because: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93)
5. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 0.98
   Because: energy 0.37 vs target 0.35 (+0.98)

============================================================
Deep Intense Rock  ->  {'genre': 'rock', 'mood': 'intense', 'energy': 0.92}
============================================================
1. Storm Runner by Voltline  [rock/intense]
   Score: 3.99
   Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 1.99
   Because: mood match (+1.0); energy 0.93 vs target 0.92 (+0.99)
3. Neon Overdrive by Pulse Theory  [edm/euphoric]
   Score: 0.96
   Because: energy 0.96 vs target 0.92 (+0.96)
4. Iron Cathedral by Black Meridian  [metal/aggressive]
   Score: 0.95
   Because: energy 0.97 vs target 0.92 (+0.95)
5. Sunrise City by Neon Echo  [pop/happy]
   Score: 0.90
   Because: energy 0.82 vs target 0.92 (+0.90)
```

**Adversarial profiles**

```
============================================================
Conflicting: high energy + sad mood  ->  {'genre': 'blues', 'mood': 'sad', 'energy': 0.9}
============================================================
1. Blue Monday Blues by Otis Marlowe  [blues/sad]
   Score: 3.50
   Because: genre match (+2.0); mood match (+1.0); energy 0.40 vs target 0.90 (+0.50)
2. Storm Runner by Voltline  [rock/intense]
   Score: 0.99
   Because: energy 0.91 vs target 0.90 (+0.99)
3. Gym Hero by Max Pulse  [pop/intense]
   Score: 0.97
   Because: energy 0.93 vs target 0.90 (+0.97)
4. Neon Overdrive by Pulse Theory  [edm/euphoric]
   Score: 0.94
   Because: energy 0.96 vs target 0.90 (+0.94)
5. Iron Cathedral by Black Meridian  [metal/aggressive]
   Score: 0.93
   Because: energy 0.97 vs target 0.90 (+0.93)

============================================================
Genre not in catalog (k-pop)  ->  {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 1.98
   Because: mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.96
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
3. Calle Sol by Mariposa Luz  [latin/joyful]
   Score: 1.00
   Because: energy 0.80 vs target 0.80 (+1.00)
4. Concrete Crown by Dre Valley  [hip hop/confident]
   Score: 0.98
   Because: energy 0.78 vs target 0.80 (+0.98)
5. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 0.95
   Because: energy 0.75 vs target 0.80 (+0.95)
```

**Weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0), Default Pop/Happy profile**

```
============================================================
Default Pop/Happy (shifted weights)  ->  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.96
   Because: genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.80 (+1.96)
2. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 2.92
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+1.92)
3. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.74
   Because: genre match (+1.0); energy 0.93 vs target 0.80 (+1.74)
4. Calle Sol by Mariposa Luz  [latin/joyful]
   Score: 2.00
   Because: energy 0.80 vs target 0.80 (+2.00)
5. Concrete Crown by Dre Valley  [hip hop/confident]
   Score: 1.96
   Because: energy 0.78 vs target 0.80 (+1.96)
```

**What I noticed**

- With the original weights, *Gym Hero* (pop/intense) ranks #2 for a happy pop fan. It has no mood match, but the genre match (+2.0) and high energy still lift it above songs with the right mood.
- After the weight shift, *Rooftop Lights* (indie pop/happy) moves above *Gym Hero*. For a happy-pop listener that feels more accurate, because a happy song near their energy beats an intense song that only shares a genre label.
- The "conflicting" profile (blues + sad + energy 0.9) returns the one sad blues song first even though its energy is far from the target. After that, the list is just loud songs with the wrong mood.

---

## Limitations and Risks

- The catalog is tiny (20 songs). Most genres have one or two songs, so results get thin after the top few.
- Genre and mood are exact text matches, so close relatives like "pop" and "indie pop" get no partial credit.
- A genre that is not in the catalog (like k-pop) never earns the genre bonus, so those users get a weaker, less specific list.
- Genre carries the most weight, so a song can rank high mostly because of its label.
- It does not understand lyrics, language, artist similarity, or listening history.
- `tempo_bpm`, `valence`, `danceability`, `acousticness` and `likes_acoustic` are not used in scoring yet.

More detail is in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

**What I learned about turning data into predictions.** A recommender does not "understand" music. It turns each song into a few numbers and labels, compares them to a profile, and sorts by score. Even this very simple version felt like a real recommendation once each result came with a plain-language reason, like "genre match (+2.0)".

**Where bias can show up.** Every choice I made quietly shaped who gets good results: making genre worth double mood, matching genre by exact text, and using a small catalog. A listener whose taste fits the catalog and the weights gets great picks. A listener with unusual or mixed taste gets a weaker list. In a big system, the same kind of choices can create filter bubbles and leave some users underserved.
