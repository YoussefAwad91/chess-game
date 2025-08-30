import re
from pathlib import Path
from typing import List
import glob
import os

ENCODINGS = ("utf-8", "latin-1", "cp1252")


def read_text_safe(path):
    """Try several encodings until one works (raises last error if none)."""
    last_exc = None
    for enc in ENCODINGS:
        try:
            return Path(path).read_text(encoding=enc)
        except UnicodeDecodeError as e:
            last_exc = e
    raise last_exc


def extract_games_moves(text, keep_move_numbers = True):

    # Primary strategy: find blocks that start with "1." up until a blank line (or EOF)
    pattern = re.compile(r"(?ms)^\s*(1\..*?)(?=\n\s*\n|\Z)")
    matches = pattern.findall(text)

    games: List[str] = []

    if not matches:
        # Fallback: split on double newlines and remove header-like lines
        parts = re.split(r"\n\s*\n", text.strip())
        for p in parts:
            lines = []
            for line in p.splitlines():
                line = line.strip()
                # skip bracketed tags like [Event "..."] OR malformed tags like Event "..." ]
                if line.startswith("[") and line.endswith("]"):
                    continue
                if re.match(r'^[A-Za-z]+ "\S.*"?\]?\s*$', line):  # e.g. Event "Troll Masters"] or Event "..."
                    continue
                lines.append(line)
            block = " ".join(lines).strip()
            if block:
                matches.append(block)

    for raw in matches:
        s = raw

        # remove {...} comments
        s = re.sub(r"\{.*?\}", " ", s, flags=re.S)
        # remove semicolon comments to end-of-line
        s = re.sub(r";[^\n]*", " ", s)
        # remove parenthetical variations (e.g. (1... Nf6))
        s = re.sub(r"\([^)]*\)", " ", s, flags=re.S)
        # collapse whitespace
        s = re.sub(r"\s+", " ", s).strip()

        # option: remove move numbers (1., 1..., 2., etc.)
        if not keep_move_numbers:
            s = re.sub(r"\b\d+\.(?:\.\.)?\s*", "", s)

        if s:
            games.append(s)

    return games


def clean_pgn_file(input_path, output_path, keep_move_numbers = True):
    """
    Read input PGN, extract/clean moves, write to output file.
    Returns number of games extracted.
    """
    text = read_text_safe(input_path)
    games = extract_games_moves(text, keep_move_numbers=keep_move_numbers)
    out = Path(output_path)
    out.write_text("\n\n".join(games), encoding="utf-8")
    return len(games)


if __name__ == "__main__":
    folder_in = "pgns/raw data"
    folder_out = "pgns/clean data"
    n = 0

    pgn_files = glob.glob(os.path.join(folder_in, "*.pgn"))

    for pgn_file in pgn_files:

        base_name = os.path.basename(pgn_file)
        out_file = os.path.join(folder_out, base_name.replace(".pgn", "_games.txt"))
        
        n += clean_pgn_file(pgn_file, out_file, keep_move_numbers=True)

    print(f"Wrote {n} games to {folder_out}")
