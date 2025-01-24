# Session 2: Software 2.0, Data Engineering, ML

1. Clone this repo
2. Navigate to downloaded folder and create new venv
```
python -m venv s2-env
```
3. Activate venv
```
# mac/linux
source s2-env/bin/activate

```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Launch Jupyter Lab
```
jupyter lab
```

# Student Sentiment & Experience Insights

## Goal
Understand how students feel about their housing and identify trends or pain points to guide improvements in property management and product features.

## Data Sources
	1.	Social Media: Reddit (Hashtags related to the university or student housing.)

## Pipeline Steps
	1.	Extract:
	•	Redit scraping
	•	Ideally use APIs (e.g., Redit API) to pull recent comments/posts (awaiting on registration)
	
	2.	Transform:
	•	Clean text (remove special characters, handle emojis, etc.).
	•	Extract features like sentiment scores, keywords (e.g., “rent too high,” “love the amenities”).

	3.	Load:
	•	Store the sentiment scores and user engagement metrics in a single data table for easy reporting.

## Approach

	1.	Scrape the Front Page of r/college (Old Reddit)
	•	We point our requests to https://old.reddit.com/r/college/ because Old Reddit’s HTML structure is simpler and more consistent for scraping.

	2.	Parse HTML with BeautifulSoup
	•	We look for each div with a class of thing, which (on Old Reddit) typically represents a single post container.
	•	Inside each container, we grab the <a class="title"> element to extract the post’s title (and link if needed).

	3.	Sentiment Analysis
	•	We run a TextBlob sentiment analysis on the cleaned version of each post’s title.
	•	polarity ranges from -1.0 (most negative) to +1.0 (most positive).
	•	subjectivity ranges from 0.0 (very objective) to 1.0 (very subjective).

	4.	Follow the ‘Next’ Button
	•	For pagination, we look for the “next-button” link at the bottom of the page.
	•	We can continue scraping multiple pages. (Adjust pages_to_scrape for a deeper crawl.)

	5.	Save Results to CSV
	•	Each row includes the post’s title, link, polarity, and subjectivity scores.