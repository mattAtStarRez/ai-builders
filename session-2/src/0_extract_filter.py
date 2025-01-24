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

# -------------------------------------------
# B. Helper function: Check if title contains
#    any of the target keywords
# -------------------------------------------
def contains_any_keyword(text: str, keywords: list) -> bool:
    """
    Returns True if 'text' contains at least one keyword
    from the 'keywords' list (case-insensitive).
    """
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return True
    return False

# ----------------------------------------------------------
# C. Function to scrape a single page from old.reddit.com
# ----------------------------------------------------------
def scrape_subreddit_page(url: str, headers: dict, keywords: list):
    """
    Fetches a single page of subreddit posts and returns a list of dictionaries
    containing post data (title, URL, etc.) for posts that match at least one
    of the keywords, as well as the link to the 'next' page.
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

        # 1. Check if the title contains any relevant keywords
        if not contains_any_keyword(title, keywords):
            # Skip this post, no relevant keywords found
            continue

        # 2. Clean title for sentiment analysis
        cleaned_title = clean_text(title)

        # 3. Basic sentiment from TextBlob
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
# D. Main scraping + analysis flow
# -------------------------------
def main():
    # 1. Define your starting URL and headers
    start_url = "https://old.reddit.com/r/college/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"
    }

    # 2. Define relevant keywords (housing-related)
    KEYWORDS = [
        "housing", "roommate", "dorm", "rent", "landlord",
        "lease", "resident", "property management", "maintenance", "amenities",
        "off-campus", "on-campus", "apartment", "utilities", "sublet"
    ]

    all_posts = []
    current_url = start_url
    pages_to_scrape = 10  # You can adjust how many pages to scrape

    for page_number in range(1, pages_to_scrape + 1):
        print(f"Scraping page {page_number}: {current_url}")
        page_posts, next_page_url = scrape_subreddit_page(current_url, headers, KEYWORDS)
        
        if not page_posts:
            print("No matching posts found on this page or an error occurred.")
        
        all_posts.extend(page_posts)

        if not next_page_url:
            # No more pages
            print("No further pages found or next link missing.")
            break
        
        current_url = next_page_url
        # Sleep to respect rate limits and not hammer Reddit
        time.sleep(2)

    # 3. Save the filtered results into a CSV file
    csv_filename = "reddit_filtered_scraped_analysis.csv"
    fieldnames = ["title", "post_url", "polarity", "subjectivity"]

    with open(csv_filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for post in all_posts:
            writer.writerow(post)

    print(f"Scraped {len(all_posts)} posts total (matching keywords), saved to '{csv_filename}'.")

if __name__ == "__main__":
    main()