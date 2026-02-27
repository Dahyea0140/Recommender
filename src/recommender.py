import sys
import os
import matplotlib.pyplot as plt

# Add the parent directory (project root) to sys.path
project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_root)

from src.data_utils import df_movies, movies_rating


def recommend_high_quality(movies_rating, min_raters, top_n):
    movies_rating["avg_rating"] = movies_rating["avg_rating"].round(1)
    reliable_movies = movies_rating[movies_rating["num_rating"] > min_raters]
    reliable_movies = reliable_movies.sort_values(
        by=["avg_rating", "num_rating"], ascending=[False, False]
    ).reset_index(drop=True)
    return reliable_movies.head(top_n)


def recommend_genre_based(movies, movies_ratings):

    movies["genres"] = movies["genres"].str.split("|")

    # Explode genre list to have one genre per row
    exploded_genres = movies[["movieid", "genres"]].explode("genres")

    valid_genres = exploded_genres[exploded_genres["genres"] != "(no genres listed)"]

    movies_ratings = movies_ratings.merge(valid_genres, on="movieid", how="inner")

    genre_stats = movies_ratings.groupby("genres", as_index=False).agg(
        genre_rating=("avg_rating", "mean"), genre_count=("genres", "count")
    )
    top_genres = genre_stats.sort_values(
        ascending=False, by="genre_rating"
    ).reset_index(drop=True)

    return top_genres
