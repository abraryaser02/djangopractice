import facebook_scraper as fs
import logging

# Configure logging to write to a file and show all log levels
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Path to your cookies file
cookies_file = './cookies.txt'

# Specify another group ID (public group for testing)
test_group_id = '613870175328566'  # Replace with a known public group ID

# Define the number of pages you want to scrape
pages_to_scrape = 1

# Function to scrape posts from the specified group and write to a file
def scrape_group_posts(group_id, pages, output_file):
    post_count = 0
    with open(output_file, 'w', encoding='utf-8') as file:
        try:
            logging.info(f"Starting to scrape group: {group_id} for {pages} pages")
            for post in fs.get_posts(group=group_id, pages=pages, cookies=cookies_file, options={"comments": True}):
                logging.debug("Entire Post Dictionary: %s", post)
                if 'text' in post:
                    raw_post_text = post['text']
                    logging.info(f"Raw Post Text: {raw_post_text[:50]}")  # Log first 50 chars of raw post text
                    file.write("Post:\n")
                    file.write(raw_post_text + '\n\n')

                    if 'comments_full' in post and post['comments_full']:
                        for comment in post['comments_full']:
                            file.write("Comment:\n")
                            file.write(comment['comment_text'] + '\n')
                            if 'replies' in comment and comment['replies']:
                                for reply in comment['replies']:
                                    file.write("Reply:\n")
                                    file.write(reply['comment_text'] + '\n')

                    post_count += 1
                else:
                    logging.debug("Post does not contain 'text' field: %s", post)
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
        finally:
            logging.info(f"Finished scraping. Total posts written: {post_count}")

# File path to write the scraped data
output_file = 'facebook_group_posts.txt'

# Run the function to scrape posts
scrape_group_posts(test_group_id, pages_to_scrape, output_file)