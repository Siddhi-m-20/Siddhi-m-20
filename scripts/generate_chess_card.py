import html
import json
import urllib.request
from pathlib import Path


USERNAME = "siddhim76"

PROFILE_URL = f"https://api.chess.com/pub/player/{USERNAME}"
STATS_URL = f"https://api.chess.com/pub/player/{USERNAME}/stats"

OUTPUT = Path("assets/chess-stats.svg")


def fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Siddhi-Manjarekar-GitHub-Profile/1.0"
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_value(data, *keys, default="—"):
    current = data

    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default

        current = current[key]

    return current


def safe(value):
    return html.escape(str(value))


def game_stats(stats, game_type):
    return stats.get(f"chess_{game_type}", {})


def rating(stats, game_type):
    return get_value(
        game_stats(stats, game_type),
        "last",
        "rating"
    )


def best_rating(stats, game_type):
    return get_value(
        game_stats(stats, game_type),
        "best",
        "rating"
    )


def collect_games(stats):
    wins = 0
    losses = 0
    draws = 0

    for game_type in ["rapid", "blitz", "bullet"]:
        record = game_stats(stats, game_type).get("record", {})

        wins += int(record.get("win", 0) or 0)
        losses += int(record.get("loss", 0) or 0)
        draws += int(record.get("draw", 0) or 0)

    total = wins + losses + draws

    return total, wins, losses, draws


def generate_svg(profile, stats):

    avatar = profile.get("avatar", "")

    rapid = rating(stats, "rapid")
    blitz = rating(stats, "blitz")
    bullet = rating(stats, "bullet")

    rapid_best = best_rating(stats, "rapid")
    blitz_best = best_rating(stats, "blitz")
    bullet_best = best_rating(stats, "bullet")

    tactics = stats.get("tactics", {})
    puzzle_rush = stats.get("puzzle_rush", {})
    lessons = stats.get("lessons", {})

    puzzle_rating = get_value(
        tactics,
        "highest",
        "rating"
    )

    puzzle_rush_score = get_value(
        puzzle_rush,
        "best",
        "score"
    )

    puzzle_rush_attempts = get_value(
        puzzle_rush,
        "best",
        "total_attempts"
    )

    lesson_rating = get_value(
        lessons,
        "highest",
        "rating"
    )

    total, wins, losses, draws = collect_games(stats)

    win_rate = "—"

    if total > 0:
        win_rate = f"{wins / total * 100:.1f}%"

    username = safe(profile.get("username", USERNAME))

    # Profile photo
    avatar_svg = ""

    if avatar:
        avatar_svg = f"""
        <defs>
          <clipPath id="avatarClip">
            <circle cx="62" cy="62" r="34"/>
          </clipPath>
        </defs>

        <image
          href="{safe(avatar)}"
          x="28"
          y="28"
          width="68"
          height="68"
          preserveAspectRatio="xMidYMid slice"
          clip-path="url(#avatarClip)"
        />

        <circle
          cx="62"
          cy="62"
          r="34"
          fill="none"
          stroke="#d1d5db"
          stroke-width="2"
        />
        """

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="620"
     height="360"
     viewBox="0 0 620 360">

  <rect
    x="1"
    y="1"
    width="618"
    height="358"
    rx="20"
    fill="#f8fafc"
    stroke="#d1d5db"
    stroke-width="2"/>

  {avatar_svg}

  <!-- Header -->

  <text
    x="112"
    y="52"
    font-family="Arial, Helvetica, sans-serif"
    font-size="22"
    font-weight="700"
    fill="#111827">
    {username}
  </text>

  <text
    x="112"
    y="76"
    font-family="Arial, Helvetica, sans-serif"
    font-size="13"
    fill="#6b7280">
    Chess.com Profile
  </text>

  <!-- Chess.com mark -->

  <circle
    cx="558"
    cy="56"
    r="24"
    fill="#ffffff"
    stroke="#d1d5db"/>

  <text
    x="558"
    y="65"
    text-anchor="middle"
    font-family="Arial, Helvetica, sans-serif"
    font-size="25"
    fill="#111827">
    ♟
  </text>

  <!-- Ratings -->

  <text x="32" y="125"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    RAPID
  </text>

  <text x="32" y="151"
    font-family="Arial"
    font-size="25"
    font-weight="700"
    fill="#111827">
    {safe(rapid)}
  </text>

  <text x="32" y="170"
    font-family="Arial"
    font-size="11"
    fill="#6b7280">
    Best {safe(rapid_best)}
  </text>


  <text x="230" y="125"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    BLITZ
  </text>

  <text x="230" y="151"
    font-family="Arial"
    font-size="25"
    font-weight="700"
    fill="#111827">
    {safe(blitz)}
  </text>

  <text x="230" y="170"
    font-family="Arial"
    font-size="11"
    fill="#6b7280">
    Best {safe(blitz_best)}
  </text>


  <text x="428" y="125"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    BULLET
  </text>

  <text x="428" y="151"
    font-family="Arial"
    font-size="25"
    font-weight="700"
    fill="#111827">
    {safe(bullet)}
  </text>

  <text x="428" y="170"
    font-family="Arial"
    font-size="11"
    fill="#6b7280">
    Best {safe(bullet_best)}
  </text>

  <!-- Divider -->

  <line
    x1="32"
    y1="190"
    x2="588"
    y2="190"
    stroke="#e5e7eb"/>

  <!-- Activity -->

  <text x="32" y="220"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    PUZZLES
  </text>

  <text x="32" y="245"
    font-family="Arial"
    font-size="20"
    font-weight="700"
    fill="#111827">
    {safe(puzzle_rating)}
  </text>


  <text x="215" y="220"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    PUZZLE RUSH
  </text>

  <text x="215" y="245"
    font-family="Arial"
    font-size="20"
    font-weight="700"
    fill="#111827">
    {safe(puzzle_rush_score)}
  </text>


  <text x="405" y="220"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    LESSONS
  </text>

  <text x="405" y="245"
    font-family="Arial"
    font-size="20"
    font-weight="700"
    fill="#111827">
    {safe(lesson_rating)}
  </text>

  <!-- Bottom -->

  <line
    x1="32"
    y1="263"
    x2="588"
    y2="263"
    stroke="#e5e7eb"/>

  <text x="32" y="290"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    GAMES
  </text>

  <text x="32" y="314"
    font-family="Arial"
    font-size="19"
    font-weight="700"
    fill="#111827">
    {total}
  </text>

  <text x="32" y="334"
    font-family="Arial"
    font-size="11"
    fill="#6b7280">
    {wins}W · {losses}L · {draws}D
  </text>


  <text x="235" y="290"
    font-family="Arial"
    font-size="11"
    font-weight="700"
    fill="#6b7280">
    WIN RATE
  </text>

  <text x="235" y="314"
    font-family="Arial"
    font-size="19"
    font-weight="700"
    fill="#111827">
    {safe(win_rate)}
  </text>


  <text x="588" y="334"
    text-anchor="end"
    font-family="Arial"
    font-size="10"
    fill="#9ca3af">
    Chess.com Public API
  </text>

</svg>
"""

    return svg


def main():

    profile = fetch_json(PROFILE_URL)
    stats = fetch_json(STATS_URL)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        generate_svg(profile, stats),
        encoding="utf-8"
    )

    print("Chess.com card updated successfully.")


if __name__ == "__main__":
    main()
