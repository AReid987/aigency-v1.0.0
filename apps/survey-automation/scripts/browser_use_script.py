import os
import time
import random
from fake_useragent import UserAgent
from browser_use import Browser

# Function to handle login for fivesurveys.com
def login_fivesurveys(browser, username, password):
    try:
        browser.open('https://www.fivesurveys.com/login')
        time.sleep(random.uniform(1, 3))
        browser.fill('input[name="username"]', username)
        time.sleep(random.uniform(0.5, 1.5))
        browser.fill('input[name="password"]', password)
        time.sleep(random.uniform(0.5, 1.5))
        browser.click('button[type="submit"]')
        time.sleep(random.uniform(2, 4)) # Wait for login to complete with random delay
        print("Successfully logged in to fivesurveys.com")
    except Exception as e:
        print(f"Error logging in to fivesurveys.com: {e}")

# Function to handle surveys.gobranded.com with bot protection
def handle_gobranded_survey(browser, survey_url):
    try:
        browser.open(survey_url)
        time.sleep(random.uniform(5, 8)) # Allow page to load and bot protection to run with random delay

        # Simulate human-like behavior
        browser.js('window.scrollTo(0, document.body.scrollHeight)') # Scroll to the bottom
        time.sleep(random.uniform(1, 3)) # Wait a bit
        browser.js('window.scrollTo(0, 0)') # Scroll back to the top
        time.sleep(random.uniform(1, 3)) # Wait a bit

        # Implement logic to interact with the survey, e.g., clicking buttons, filling forms
        # This might require more sophisticated techniques to bypass bot detection
        print(f"Handling survey at {survey_url}")
    except Exception as e:
        print(f"Error handling survey at {survey_url}: {e}")

# Main function
def main():
    try:
        # Install fake_useragent
        os.system('pip install fake_useragent')

        # Initialize Browser Use
        browser = Browser()

        # Set a random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        ]
        browser.user_agent = random.choice(user_agents)

        # fivesurveys.com automation
        login_fivesurveys(browser, 'your_username', 'your_password') # Replace with your credentials
        time.sleep(random.uniform(2, 4))
        browser.open('https://www.fivesurveys.com/surveys') # Replace with actual survey page
        time.sleep(random.uniform(2, 4))
        # Add logic to find and complete surveys on fivesurveys.com
        print("Completing surveys on fivesurveys.com")

        # surveys.gobranded.com automation
        gobranded_survey_url = 'https://surveys.gobranded.com/survey/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' # Replace with actual survey URL
        handle_gobranded_survey(browser, gobranded_survey_url)
        print("Completing survey on surveys.gobranded.com")

        browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
