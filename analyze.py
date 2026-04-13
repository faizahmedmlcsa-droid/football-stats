"""
FIFA / Football Stats Dashboard
================================
Run: python analyze.py
Then: python -m http.server 8000
Open: http://localhost:8000/dashboard.html
"""

import json
import random
import webbrowser
import os

# ─── DATASET ──────────────────────────────────────────────────────────────────

PLAYERS = [
    # name, club, nation, position, age, goals, assists, matches, rating, pace, shooting, passing, dribbling, defending, physical
    ("Kylian Mbappé",       "Real Madrid",    "France",    "FW", 25, 38, 12, 42, 91, 97, 90, 82, 92, 36, 78),
    ("Erling Haaland",      "Man City",       "Norway",    "FW", 23, 42, 8,  40, 91, 89, 95, 65, 80, 45, 88),
    ("Vinicius Jr",         "Real Madrid",    "Brazil",    "FW", 24, 26, 18, 44, 89, 95, 83, 80, 95, 28, 73),
    ("Rodri",               "Man City",       "Spain",     "MF", 27, 8,  14, 46, 91, 58, 72, 90, 88, 85, 84),
    ("Jude Bellingham",     "Real Madrid",    "England",   "MF", 20, 22, 13, 43, 88, 78, 82, 85, 87, 72, 83),
    ("Lionel Messi",        "Inter Miami",    "Argentina", "FW", 36, 18, 24, 35, 90, 71, 85, 92, 96, 34, 65),
    ("Mohamed Salah",       "Liverpool",      "Egypt",     "FW", 31, 29, 16, 44, 88, 90, 87, 78, 87, 45, 75),
    ("Harry Kane",          "Bayern Munich",  "England",   "FW", 30, 36, 14, 42, 87, 72, 93, 78, 80, 52, 83),
    ("Kevin De Bruyne",     "Man City",       "Belgium",   "MF", 32, 11, 22, 38, 91, 76, 86, 94, 88, 64, 78),
    ("Lamine Yamal",        "Barcelona",      "Spain",     "FW", 16, 14, 19, 40, 86, 92, 78, 75, 91, 22, 65),
    ("Bukayo Saka",         "Arsenal",        "England",   "FW", 22, 20, 17, 43, 86, 86, 82, 76, 84, 55, 72),
    ("Phil Foden",          "Man City",       "England",   "MF", 23, 19, 15, 41, 87, 82, 83, 82, 87, 53, 76),
    ("Pedri",               "Barcelona",      "Spain",     "MF", 21, 9,  16, 38, 86, 68, 75, 90, 89, 68, 72),
    ("Federico Valverde",   "Real Madrid",    "Uruguay",   "MF", 25, 14, 11, 44, 87, 82, 80, 82, 86, 74, 88),
    ("Trent Alexander-Arnold","Liverpool",    "England",   "DF", 25, 8,  18, 43, 87, 72, 78, 86, 82, 74, 72),
    ("Achraf Hakimi",       "PSG",            "Morocco",   "DF", 25, 7,  13, 42, 85, 91, 72, 78, 80, 76, 76),
    ("Virgil van Dijk",     "Liverpool",      "Netherlands","DF",32, 4,  3,  43, 88, 68, 58, 72, 80, 92, 88),
    ("Rúben Dias",          "Man City",       "Portugal",  "DF", 26, 3,  2,  40, 87, 62, 52, 68, 76, 91, 85),
    ("Gianluigi Donnarumma","PSG",            "Italy",     "GK", 25, 0,  0,  38, 89, 52, 42, 65, 58, 88, 82),
    ("Alisson Becker",      "Liverpool",      "Brazil",    "GK", 31, 0,  0,  40, 88, 54, 44, 68, 60, 86, 78),
    ("Robert Lewandowski",  "Barcelona",      "Poland",    "FW", 35, 24, 10, 38, 85, 72, 92, 78, 82, 44, 82),
    ("Antoine Griezmann",   "Atletico Madrid","France",    "FW", 32, 18, 14, 42, 84, 78, 85, 80, 83, 58, 76),
    ("Khvicha Kvaratskhelia","Napoli",        "Georgia",   "FW", 22, 16, 15, 40, 85, 90, 80, 74, 87, 38, 72),
    ("Florian Wirtz",       "Bayer Leverkusen","Germany",  "MF", 20, 18, 20, 41, 88, 82, 82, 82, 88, 56, 72),
    ("Declan Rice",         "Arsenal",        "England",   "MF", 25, 7,  8,  44, 85, 72, 68, 82, 84, 86, 84),
    ("Bruno Fernandes",     "Man United",     "Portugal",  "MF", 29, 16, 14, 42, 85, 74, 82, 84, 84, 58, 76),
    ("Bernardo Silva",      "Man City",       "Portugal",  "MF", 29, 10, 16, 43, 87, 78, 76, 88, 90, 68, 76),
    ("Jamal Musiala",       "Bayern Munich",  "Germany",   "MF", 21, 15, 14, 40, 87, 84, 78, 78, 88, 52, 74),
    ("Neymar Jr",           "Al-Hilal",       "Brazil",    "FW", 32, 8,  10, 22, 84, 88, 82, 82, 92, 30, 68),
    ("Cristiano Ronaldo",   "Al-Nassr",       "Portugal",  "FW", 39, 35, 8,  38, 84, 78, 94, 68, 76, 34, 84),
]

MATCHES = [
    # home, away, home_goals, away_goals, competition, date
    ("Real Madrid",    "Man City",       3, 3, "UCL",        "2024-04-09"),
    ("Liverpool",      "Arsenal",        2, 2, "Premier League", "2024-04-07"),
    ("Barcelona",      "PSG",            3, 2, "UCL",        "2024-04-10"),
    ("Bayern Munich",  "Bayer Leverkusen",1,1, "Bundesliga", "2024-04-06"),
    ("Man City",       "Arsenal",        0, 1, "Premier League", "2024-03-31"),
    ("Real Madrid",    "Barcelona",      3, 2, "La Liga",    "2024-04-21"),
    ("Liverpool",      "Man United",     2, 0, "Premier League", "2024-04-07"),
    ("PSG",            "Atletico Madrid",2, 1, "UCL",        "2024-03-06"),
    ("Man City",       "Real Madrid",    1, 1, "UCL",        "2024-04-17"),
    ("Arsenal",        "Bayern Munich",  2, 2, "UCL",        "2024-04-09"),
    ("Barcelona",      "Napoli",         3, 1, "UCL",        "2024-03-12"),
    ("Bayer Leverkusen","Man United",    2, 0, "UEL",        "2024-04-11"),
    ("Inter Miami",    "Al-Nassr",       3, 2, "Friendly",   "2024-02-01"),
    ("Liverpool",      "Man City",       1, 1, "Premier League","2024-03-10"),
    ("Real Madrid",    "Atletico Madrid",2, 1, "La Liga",    "2024-04-27"),
    ("Barcelona",      "Bayer Leverkusen",1,4, "UCL",        "2024-04-11"),
    ("Arsenal",        "Man United",     1, 0, "Premier League","2024-03-03"),
    ("Bayern Munich",  "Arsenal",        1, 0, "UCL",        "2024-04-17"),
    ("PSG",            "Barcelona",      4, 1, "UCL",        "2024-03-12"),
    ("Man City",       "Liverpool",      2, 1, "FA Cup",     "2024-03-16"),
]

# ─── ANALYSIS ─────────────────────────────────────────────────────────────────

# Top scorers
top_scorers = sorted(PLAYERS, key=lambda x: x[5], reverse=True)[:10]

# Top assisters
top_assisters = sorted(PLAYERS, key=lambda x: x[6], reverse=True)[:10]

# Top rated
top_rated = sorted(PLAYERS, key=lambda x: x[8], reverse=True)[:10]

# Goals by position
pos_goals = {}
for p in PLAYERS:
    pos = p[3]
    pos_goals[pos] = pos_goals.get(pos, 0) + p[5]

# Goals by nation
nation_goals = {}
for p in PLAYERS:
    n = p[2]
    nation_goals[n] = nation_goals.get(n, 0) + p[5]
nation_goals = dict(sorted(nation_goals.items(), key=lambda x: x[1], reverse=True)[:8])

# Club stats
club_stats = {}
for p in PLAYERS:
    c = p[1]
    if c not in club_stats:
        club_stats[c] = {"goals": 0, "assists": 0, "players": 0, "avg_rating": 0}
    club_stats[c]["goals"] += p[5]
    club_stats[c]["assists"] += p[6]
    club_stats[c]["players"] += 1
    club_stats[c]["avg_rating"] += p[8]
for c in club_stats:
    club_stats[c]["avg_rating"] = round(club_stats[c]["avg_rating"] / club_stats[c]["players"], 1)
top_clubs = dict(sorted(club_stats.items(), key=lambda x: x[1]["goals"], reverse=True)[:8])

# Match stats
total_goals = sum(m[2] + m[3] for m in MATCHES)
avg_goals = round(total_goals / len(MATCHES), 2)
high_scoring = sorted(MATCHES, key=lambda x: x[2]+x[3], reverse=True)[:5]

# Competition breakdown
comp_goals = {}
for m in MATCHES:
    comp_goals[m[4]] = comp_goals.get(m[4], 0) + m[2] + m[3]

# Radar data for top 5 players (pace, shooting, passing, dribbling, defending, physical)
radar_players = [
    {"name": p[0], "club": p[1],
     "stats": {"Pace": p[9], "Shooting": p[10], "Passing": p[11],
               "Dribbling": p[12], "Defending": p[13], "Physical": p[14]}}
    for p in [
        next(x for x in PLAYERS if x[0] == "Kylian Mbappé"),
        next(x for x in PLAYERS if x[0] == "Erling Haaland"),
        next(x for x in PLAYERS if x[0] == "Jude Bellingham"),
        next(x for x in PLAYERS if x[0] == "Vinicius Jr"),
        next(x for x in PLAYERS if x[0] == "Rodri"),
    ]
]

# ─── BUILD PAYLOAD ────────────────────────────────────────────────────────────

data = {
    "total_players": len(PLAYERS),
    "total_matches": len(MATCHES),
    "total_goals": sum(p[5] for p in PLAYERS),
    "total_assists": sum(p[6] for p in PLAYERS),
    "avg_goals_per_match": avg_goals,
    "top_scorers": [{"name": p[0], "club": p[1], "nation": p[2], "goals": p[5], "rating": p[8]} for p in top_scorers],
    "top_assisters": [{"name": p[0], "club": p[1], "nation": p[2], "assists": p[6], "rating": p[8]} for p in top_assisters],
    "top_rated": [{"name": p[0], "club": p[1], "position": p[3], "rating": p[8]} for p in top_rated],
    "pos_goals": pos_goals,
    "nation_goals": nation_goals,
    "top_clubs": {k: v for k, v in top_clubs.items()},
    "comp_goals": comp_goals,
    "high_scoring": [{"home": m[0], "away": m[1], "score": f"{m[2]}–{m[3]}", "comp": m[4], "date": m[5]} for m in high_scoring],
    "radar_players": radar_players,
    "all_players": [{"name": p[0], "club": p[1], "nation": p[2], "position": p[3],
                     "age": p[4], "goals": p[5], "assists": p[6], "matches": p[7], "rating": p[8]} for p in PLAYERS],
}

with open("data.json", "w") as f:
    json.dump(data, f)

print("✅ Analysis complete!")
print(f"   Players analyzed : {len(PLAYERS)}")
print(f"   Matches analyzed : {len(MATCHES)}")
print(f"   Total goals      : {sum(p[5] for p in PLAYERS)}")
print(f"   Top scorer       : {top_scorers[0][0]} ({top_scorers[0][5]} goals)")
print(f"   Top assister     : {top_assisters[0][0]} ({top_assisters[0][6]} assists)")
print()
print("🌐 Now run:  python -m http.server 8000")
print("   Open   :  http://localhost:8000/dashboard.html")
