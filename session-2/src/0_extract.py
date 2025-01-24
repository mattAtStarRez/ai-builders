import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import csv
import re
import time


# -------------------------------------------
# A. Helper function: Clean text for analysis
# -------------------------------------------
def clean_text(text: str) -> str:
    """
    Remove URLs, special characters, and excessive whitespace from text.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters (except basic punctuation)
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ----------------------------------------------------------
# B. Function to scrape a single page from old.reddit.com
# ----------------------------------------------------------
def scrape_subreddit_page(url: str, headers: dict):
    """
    Fetches a single page of subreddit posts and returns a list of dictionaries
    containing post data (title, URL, etc.), as well as the link to the 'next' page.
    """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url} (Status code: {response.status_code})")
        return [], None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all post entries on the page
    posts_data = []
    post_containers = soup.find_all("div", class_="thing")

    for post in post_containers:
        # Each post might have a title in a <p class="title"> or <a class="title"> (depending on the version of Reddit)
        title_tag = post.find("a", class_="title")
        if not title_tag:
            continue  # skip if we can't find a title

        title = title_tag.get_text(strip=True)
        post_url = title_tag.get("href")

        # Some posts have selftext previews, but they are often not displayed in the HTML feed.
        # We'll rely mainly on the title for sentiment for demonstration purposes.
        cleaned_title = clean_text(title)

        # Basic sentiment from TextBlob
        blob = TextBlob(cleaned_title)
        polarity = blob.sentiment.polarity       # -1.0 (negative) to 1.0 (positive)
        subjectivity = blob.sentiment.subjectivity  # 0.0 (objective) to 1.0 (subjective)

        posts_data.append({
            "title": title,
            "post_url": post_url,
            "polarity": polarity,
            "subjectivity": subjectivity
        })

    # Find link to the "next" page (if it exists)
    next_button = soup.find("span", class_="next-button")
    next_page_url = None
    if next_button:
        next_link = next_button.find("a")
        if next_link:
            next_page_url = next_link.get("href")

    return posts_data, next_page_url

# -------------------------------
# C. Main scraping + analysis flow
# -------------------------------
def main():
    # Starting URL for old.reddit.com (often easier to parse than new Reddit)
    start_url = "https://old.reddit.com/r/college/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"
    }

    all_posts = []
    current_url = start_url
    pages_to_scrape = 3  # You can adjust how many pages to scrape

    for page_number in range(1, pages_to_scrape + 1):
        print(f"Scraping page {page_number}: {current_url}")
        page_posts, next_page_url = scrape_subreddit_page(current_url, headers)
        
        if not page_posts:
            # If we failed to get data or hit a rate-limit, stop
            print("No posts found or error occurred. Stopping.")
            break
        
        all_posts.extend(page_posts)

        if not next_page_url:
            # No more pages
            print("No further pages found.")
            break
        
        current_url = next_page_url
        # Sleep to respect rate limits and not hammer Reddit
        time.sleep(2)

    # ------------------------------------
    # D. Save the Results into a CSV File
    # ------------------------------------
    csv_filename = "reddit_college_scraped_analysis.csv"
    fieldnames = ["title", "post_url", "polarity", "subjectivity"]

    with open(csv_filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for post in all_posts:
            writer.writerow(post)

    print(f"Scraped {len(all_posts)} posts total, saved to '{csv_filename}'.")

if __name__ == "__main__":
    main()



















# import pandas as pd
# from sqlalchemy import create_engine, text

# # Adjust pandas display settings
# pd.set_option('display.max_columns', None)  # Show all columns

# # Load the spreadsheet
# file_path = 'pricing-spreadsheet.xlsx'  # Path to your spreadsheet
# sheet_name = 'Sheet1'  # Specify the sheet name or index
# data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

# # Clean column names
# data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

# # Split up key features into separate columns
# # Specify the column to split
# column_to_split = "key_features" 

# # Split the column based on the delimiter and create new columns
# split_columns = data[column_to_split].str.split(",", expand=True)

# # Rename the new columns
# split_columns.columns = [f"{column_to_split}_{i+1}" for i in range(split_columns.shape[1])]
# data = pd.concat([data, split_columns], axis=1)

# # Save the updated DataFrame back to a new file
# output_file_path = "updated-pricing-spreadsheet.xlsx"
# data.to_excel(output_file_path, index=False)

# print(f"Updated spreadsheet saved to: {output_file_path}")

# # Split into products and pricing tables
# products = data[['plan_name', 'key_features_1', 'key_features_2', 'key_features_3', 'add-ons', 'support_level' ]].drop_duplicates()
# pricing = data[['monthly_price_(usd)', 'annual_price_(usd)', 'usage_limits']]

# # Create a database engine (SQLite in this case)
# engine = create_engine('sqlite:///pricing_data.db')

# # Write data to database
# products.to_sql('products', engine, index=False, if_exists='replace')
# pricing.to_sql('pricing', engine, index=False, if_exists='replace')

# print("Data inserted into the database successfully!")

# # Query data from the database
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM products LIMIT 5"))
#     for row in result:
#         print(row)