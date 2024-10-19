import sqlite3
import os
import argparse


# SQL to create a `trivia` table.
# `id` - primary key, integer.
# `season` - season number, integer.
# `category` - name of the category, string.
# `question` - question text, string.
# `answer` - answer text, string.
# `score` - number of points for the question, integer.
CREATE_TABLE = """
CREATE TABLE trivia (
    id INTEGER PRIMARY KEY,
    season INTEGER,
    category TEXT,
    question TEXT,
    answer TEXT,
    score INTEGER
);
"""


# Process all TSV files in the input directory and write to DB.
# TSV files are a Jeopardy question database laid out with these columns:
# `round` - round when the question was asked.
# `clue_value` - dollar value of the clue.
# `daily_double_value` - amount wagered.
# `category` - category of the question.
# `comments` - additional comments.
# `answer` - the text displayed on the board.
# `question` - the correct question to the answer.
# `air_date` - date the episode aired.
# `notes` - additional notes.
# In addition, the name of the file specifies the season like `seasonX.tsv`
def build_db(input_dir: str, db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)

    id_ = 0
    for file in os.listdir(input_dir):
        if file.endswith(".tsv"):
            season = int(file.split(".")[0].split("season")[1])
            with open(os.path.join(input_dir, file), "r") as f:
                for line in f:
                    round, clue_value, daily_double_value, category, comments, answer, question, air_date, notes = line.split("\t")
                    id_ += 1
                    cursor.execute(
                        """
                        INSERT INTO trivia
                        (id, season, category, question, answer, score)
                        VALUES
                        (?, ?, ?, ?, ?, ?)
                        """,
                        (id_, season, category, question, answer, clue_value)
                    )

    conn.commit()
    conn.close()


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Directory containing TSV files.")
    parser.add_argument("db_path", help="Path to the SQLite database.")
    args = parser.parse_args()
    build_db(args.input_dir, args.db_path)


if __name__ == "__main__":
    print("Building database...")
    cli()