import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("reddit_college_scraped_analysis.csv")

# Quick preview
# print(df.head())

# Basic info and descriptive stats
# print(df.info())
# print(df.describe())

## Distribution of Sentiment Polarity
# plt.figure(figsize=(8, 5))
# sns.histplot(df['polarity'], bins=20, kde=True, color='blue')
# plt.title("Distribution of Post Polarity")
# plt.xlabel("Polarity")
# plt.ylabel("Count")
# plt.show()

## Distribution of Subjectivity
# plt.figure(figsize=(8, 5))
# sns.histplot(df['subjectivity'], bins=20, kde=True, color='green')
# plt.title("Distribution of Post Subjectivity")
# plt.xlabel("Subjectivity")
# plt.ylabel("Count")
# plt.show()


## Scatter Plot of Polarity vs. Subjectivity
# plt.figure(figsize=(8, 6))
# sns.scatterplot(data=df, x="subjectivity", y="polarity", hue="polarity", palette="coolwarm")
# plt.title("Polarity vs. Subjectivity")
# plt.xlabel("Subjectivity (0 = objective, 1 = subjective)")
# plt.ylabel("Polarity (-1 = negative, 1 = positive)")
# plt.show()

## Categorize & Count Sentiment

# import numpy as np

# def classify_polarity(pol):
#     if pol > 0.1:
#         return "Positive"
#     elif pol < -0.1:
#         return "Negative"
#     else:
#         return "Neutral"

# df['sentiment_label'] = df['polarity'].apply(classify_polarity)

# sentiment_counts = df['sentiment_label'].value_counts()
# print(sentiment_counts)

# plt.figure(figsize=(6, 5))
# sns.countplot(x="sentiment_label", data=df, palette="viridis")
# plt.title("Count of Posts by Sentiment Category")
# plt.xlabel("Sentiment Category")
# plt.ylabel("Number of Posts")
# plt.show()