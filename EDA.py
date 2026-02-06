import pandas as pd
import matplotlib.pyplot as plt

from data_ml_25m.clean_data import load_clean_data

# Load and clean movies data
df_movies = load_clean_data("data_ml_25m/raw/movies.csv")
# Sacve cleaned movies data into processed folder
df_movies.to_csv("data_ml_25m/processed/cleaned_movies.csv", index=False)

df_ratings = load_clean_data("data_ml_25m/raw/ratings.csv")

# Save cleaned ratings data into processed folder before dropping timestamp column
df_ratings.to_csv("data_ml_25m/processed/temp_cleaned_ratings.csv", index=False)
df_ratings = df_ratings.drop(columns=["timestamp"])

# Rating filter based on number of user ratings
num_of_user_ratings = df_ratings.groupby("userid", as_index=False).agg(
    num_user_ratings=("movieid", "count")
)
df_ratings = df_ratings.merge(num_of_user_ratings, on="userid", how="left")
df_ratings = df_ratings[df_ratings["num_user_ratings"] > 20]

# Ratings based on average rating

df_ratings = df_ratings[df_ratings["rating"] > 4]
movies_rating = df_movies.merge(df_ratings, on="movieid", how="left")
movies_rating = movies_rating.groupby(["movieid", "title"], as_index=False).agg(
    avg_rating=("rating", "mean"), num_rating=("rating", "count")
)
movies_rating["avg_rating"] = movies_rating["avg_rating"].round(1)
reliable_movies = movies_rating[movies_rating["num_rating"] > 100]
reliable_movies = reliable_movies.sort_values(
    by="avg_rating", ascending=False
).reset_index(drop=True)


# Ratings based on genre list

# Create genre list. From [Action|Adventure|Sci-Fi] to [Action, Adventure, Sci-Fi]
df_movies["genre_list"] = df_movies["genres"].str.split("|")
# Explode genre list to have one genre per row
exploded_genres = df_movies[["movieid", "genre_list"]].explode("genre_list")
movies_rating = movies_rating.merge(exploded_genres, on="movieid", how="left")
genre_stats = movies_rating.groupby("genre_list", as_index=False).agg(
    genre_count=("genre_list", "count"), genre_rating=("avg_rating", "mean")
)
top_genres = genre_stats.sort_values(ascending=False, by="genre_rating").reset_index(
    drop=True
)

# Plot distribution of average ratings based on genres
plt.figure(figsize=(10, 6))
bins = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
plt.hist(genre_stats["genre_rating"], bins=bins, edgecolor="black")
plt.title("Distribution of Average Ratings by Genre")
plt.xlabel("Average Rating", fontsize=12)
plt.ylabel("Frequency(count)", fontsize=12)
plt.grid(True, alpha=0.3, linestyle="--")
plt.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
plt.show()

# Overall Ratings Distribution
plt.figure(figsize=(10, 6))
bins = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
plt.hist(movies_rating["avg_rating"], bins=bins, edgecolor="black")
plt.title("Distribution of Average Ratings")
plt.xlabel("Average Rating", fontsize=12)
plt.ylabel("Frequency(count)", fontsize=12)
plt.grid(True, alpha=0.3, linestyle="--")
plt.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
plt.show()
df_ratings.to_csv("data_ml_25m/processed/cleaned_ratings.csv", index=False)
