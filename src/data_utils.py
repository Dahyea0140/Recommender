import pandas as pd
import matplotlib.pyplot as plt


def load_clean_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    df = df.dropna()
    df = df.drop_duplicates()
    return df


df_movies = load_clean_data("raw/movies.csv")

df_movies.to_csv("processed/cleaned_movies.csv", index=False)


df_ratings = load_clean_data("raw/ratings.csv")

df_ratings.to_csv("processed/cleaned_ratings.csv", index=False)

df_ratings = df_ratings.drop(columns=["timestamp"])


num_of_user_ratings = df_ratings.groupby("userid", as_index=False).agg(
    num_user_ratings=("movieid", "count")
)
df_ratings = df_ratings.merge(num_of_user_ratings, on="userid", how="left")
df_ratings = df_ratings[df_ratings["num_user_ratings"] > 20]


movies_rating = df_movies.merge(df_ratings, on="movieid", how="left")
movies_rating = movies_rating.groupby(["movieid", "title"], as_index=False).agg(
    avg_rating=("rating", "mean"), num_rating=("rating", "count")
)
