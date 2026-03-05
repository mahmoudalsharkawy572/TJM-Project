import logging
import requests
from config import API_URL


def fetch_posts() -> list | None:
    """
    Fetches posts from the API.
    Returns a list of post dicts, or None if the request fails.
    """
    try:
        response = requests.get(API_URL, timeout=5)

        if response.status_code != 200:
            logging.error(f"API returned status {response.status_code}")
            return None

        data = response.json()

        if "posts" not in data:
            logging.error("Invalid API structure: 'posts' key not found")
            return None

        posts = data["posts"]

        if not isinstance(posts, list):
            logging.error("'posts' is not a list")
            return None

        if len(posts) != 30:
            logging.warning(f"Expected 30 posts but got {len(posts)}")

        logging.info(f"Successfully fetched {len(posts)} posts.")
        return posts

    except requests.exceptions.Timeout:
        logging.error("API request timed out.")
        return None

    except Exception as e:
        logging.error(f"API request failed: {str(e)}")
        return None
