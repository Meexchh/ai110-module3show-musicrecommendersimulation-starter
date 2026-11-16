# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 5 songs from a small catalog based on a user's favorite genre, favorite mood, and target energy level. It explains every pick with a short reason.

- It assumes the user can describe their taste with one genre, one mood, and one energy number.
- It is for **classroom exploration**, not real users.
- It should **not** be used to run a real music service, to judge people's taste, or to make decisions about artists.

---

## 3. How the Model Works

Every song gets points from three simple rules, then the songs are sorted from highest score to lowest.

- If the song's **genre** is the user's favorite genre, it gets **2 points**.
- If the song's **mood** is the user's favorite mood, it gets **1 point**.
- For **energy**, the closer the song is to the energy the user wants, the more points it gets, up to **1 point**. A song that is too calm and a song that is too intense are treated the same way: both lose points for being far away.

The best possible score is 4. The system also writes down *why* each song got its points, so the user can see the reasons.

Changes from the starter: the starter had empty placeholders. I wrote the CSV loader, the scoring rule, the ranking step, the terminal output, and the tests. I also added 10 songs.

---

## 4. Data

- The catalog has **20 songs**: the 10 starter songs plus 10 I added.
- Each song has: genre, mood, energy, tempo (BPM), valence, danceability, and acousticness.
- Genres now include pop, indie pop, lofi, rock, ambient, jazz, synthwave, hip hop, country, classical, EDM, R&B, metal, reggae, folk, blues, and latin.
- I added songs to cover more genres and moods (for example sad, euphoric, aggressive, and nostalgic).
- Missing from the data: lyrics, language, artist popularity, release year, and any listening history. Most genres have only one song, and lofi has three.
- Only genre, mood, and energy are used in scoring. The other columns are loaded but not scored yet.

---

## 5. Strengths

- It works well for users whose taste is clear and fits the catalog, like **Chill Lofi** and **Deep Intense Rock**. In both cases the exact-match song came first.
- The energy rule is a good fit for how "vibe" feels. Songs near the target energy rise, and songs far from it fall, whether they are too loud or too quiet.
- Every result comes with reasons, so it is easy to see why a song ranked where it did.
- The top results matched my intuition for the Default Pop/Happy profile. *Sunrise City* ranked first.

---

## 6. Limitations and Bias

The biggest weakness I found is that **genre is worth twice as much as mood, so a song can rank high mostly because of its genre label.** For a happy pop fan, *Gym Hero* ranks #2 even though it is an intense workout song with the wrong mood. Its genre match (+2.0) and high energy outweigh the mood it misses. A happier song in another genre (*Rooftop Lights*) lands lower, because "indie pop" is a different string from "pop" and gets no partial credit. The system also fails users whose genre is not in the catalog: the k-pop profile never earned a genre bonus, so its best score was only 1.98 out of 4. Finally, the catalog is small, so after the top two or three picks the lists are filled with songs that only match on energy.

---

## 7. Evaluation

**Profiles tested.** Four standard profiles (Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial ones (conflicting preferences, a genre that is not in the catalog, and a middle-of-the-road profile with no genre). I looked at the top 5 for each and checked whether they matched my sense of the vibe.

**What surprised me.**
- *Gym Hero* showed up for people who only asked for happy pop. The reason is simple: it is pop, and its energy is high, so it collects points even without the right mood.
- For the conflicting profile (blues, sad, energy 0.9), the one sad blues song ranked first even though it is quiet. The genre and mood points overwhelmed the energy gap. The rest of the list was loud songs with the wrong mood.

**Comparing profiles.**
- *Default Pop/Happy vs. High-Energy Pop:* Both pick pop songs first, but the happy profile puts *Sunrise City* first and the high-energy profile puts *Gym Hero* first. That makes sense: the mood and the higher energy target changed which pop song fits best.
- *Chill Lofi vs. Deep Intense Rock:* These are opposites. Lofi returns calm, acoustic songs (*Library Rain*, *Midnight Coding*) and rock returns loud songs (*Storm Runner*, then high-energy songs from other genres). The system separates these two moods well.
- *High-Energy Pop vs. Deep Intense Rock:* Both want very high energy and an intense mood, so their top 5 lists contain the same five songs in a different order. The genre bonus is what changes the top spot (*Gym Hero* for pop, *Storm Runner* for rock). That is valid, because the two tastes really are close. It also shows how small the catalog is: there are only about five very loud songs to choose from.
- *Chill Lofi vs. the no-genre chill profile:* Without a genre match, the lofi songs still win on mood and energy, but the scores drop from about 4 to under 2. This shows how much of a score comes from genre.
- *Default Pop/Happy vs. the k-pop profile:* Same mood and energy, but no genre match. *Sunrise City* stays first on mood and energy alone, and *Gym Hero* drops out of the top 5, because it only had genre to offer.

**Experiment: weight shift.** I halved genre (2.0 to 1.0) and doubled energy (1.0 to 2.0). For the happy pop profile, *Rooftop Lights* moved above *Gym Hero*, which feels more accurate. For the high-energy pop profile, *Storm Runner* moved above *Sunrise City*. The results were different in a way that matched the new priorities. I would call this version a bit more accurate for the happy pop profile, but it is a judgment call.

**Tests.** `pytest` runs 6 tests: CSV loading, score plus reasons, energy closeness vs. height, ranking order, and the OOP wrapper.

### Terminal output

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

============================================================
Middle-of-the-road energy, no genre  ->  {'genre': '', 'mood': 'chill', 'energy': 0.5}
============================================================
1. Midnight Coding by LoRoom  [lofi/chill]
   Score: 1.92
   Because: mood match (+1.0); energy 0.42 vs target 0.50 (+0.92)
2. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 1.85
   Because: mood match (+1.0); energy 0.35 vs target 0.50 (+0.85)
3. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 1.78
   Because: mood match (+1.0); energy 0.28 vs target 0.50 (+0.78)
4. Dusty Porch Light by Hollis Ray  [country/nostalgic]
   Score: 0.98
   Because: energy 0.52 vs target 0.50 (+0.98)
5. Island Breeze by Tropic Roots  [reggae/laid-back]
   Score: 0.98
   Because: energy 0.48 vs target 0.50 (+0.98)
```

### Weight-shift experiment output

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

============================================================
High-Energy Pop (shifted weights)  ->  {'genre': 'pop', 'mood': 'intense', 'energy': 0.9}
============================================================
1. Gym Hero by Max Pulse  [pop/intense]
   Score: 3.94
   Because: genre match (+1.0); mood match (+1.0); energy 0.93 vs target 0.90 (+1.94)
2. Storm Runner by Voltline  [rock/intense]
   Score: 2.98
   Because: mood match (+1.0); energy 0.91 vs target 0.90 (+1.98)
3. Sunrise City by Neon Echo  [pop/happy]
   Score: 2.84
   Because: genre match (+1.0); energy 0.82 vs target 0.90 (+1.84)
4. Neon Overdrive by Pulse Theory  [edm/euphoric]
   Score: 1.88
   Because: energy 0.96 vs target 0.90 (+1.88)
5. Iron Cathedral by Black Meridian  [metal/aggressive]
   Score: 1.86
   Because: energy 0.97 vs target 0.90 (+1.86)
```

---

## 8. Future Work

1. **Use more features.** Add valence, danceability, tempo and acousticness (and finally use `likes_acoustic`) so the score reflects more of what a "vibe" is.
2. **Give partial credit for related genres and moods.** For example, "indie pop" should count as close to "pop", and "chill" as close to "relaxed".
3. **Add diversity.** Stop the top 5 from being filled with near-duplicates, and mix in a few songs outside the user's usual taste.
4. **Handle complex tastes.** Let a profile list several favorite genres or moods instead of just one.

---

## 9. Personal Reflection

> **Draft for you to edit.** I wrote this from what the project showed. Change anything that does not match your real experience, and add your own AI-tool story.

My biggest learning moment was seeing how much one number can matter. Making genre worth 2.0 instead of 1.0 was a small choice, but it decided why *Gym Hero* kept showing up for happy pop listeners. A recommender is just a pile of choices like that, and each one quietly decides who gets good results.

AI tools helped me move faster on things like the CSV loader, the scoring structure, and the test cases. I still had to check them myself. I ran the code, read every score by hand, and compared the output to my own sense of the music, because a result can look reasonable and still be wrong for the reasons I intended.

What surprised me most is how a few simple rules plus a plain-language reason can *feel* like a real recommendation. The reasons ("genre match (+2.0)") made the output feel trustworthy, even though there is no real understanding behind it.

If I extended this, I would score more features, give partial credit to similar genres and moods, and add diversity so the top 5 are not all the same kind of song.
