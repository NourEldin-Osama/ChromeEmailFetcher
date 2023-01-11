import getpass
import re

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By


class ChromeEmailFetcher:
    def __init__(self):
        """
        Initialize the Chrome browser and set up the Chrome options,
        user profile and start the Chrome browser.
        """
        # Get the current username
        self.username = getpass.getuser()
        # Create the path to the chrome user profile folder
        self.user_profile_path = Fr'C:\Users\{self.username}\AppData\Local\Google\Chrome\User Data'

        # Initialize Chrome options
        self.options = ChromeOptions()
        # Add options
        self.options.add_argument('no-sandbox')  # run chrome without no-sandbox can cause crash
        # self.options.add_argument('headless')  # starts the browser in headless mode
        self.options.add_argument(F"user-data-dir={self.user_profile_path}")
        self.options.add_argument('profile-directory=Default')
        self.options.add_experimental_option("detach", True)  # prevent browser from closing
        self.options.add_argument('disable-gpu')  # Disable the GPU
        self.options.add_argument('disable-extensions')  # Disable the extensions
        # Disable the automation prompt bar
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])

        # to match all emails
        self.email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

        # start the browser
        self.driver = Chrome(options=self.options)
        self.driver.implicitly_wait(2)

    def run(self, save_to_file=False):
        """
        Open chrome with default profile and interact with the browser
        if save_to_file is True, it will save the emails to a file named FetchedEmails.txt
        """
        user_emails = []

        # Open chrome://settings/passwords
        self.driver.get("chrome://settings/passwords")
        # Find the saved accounts
        info_element = self.driver.find_element(By.TAG_NAME, 'body').text
        user_emails += re.findall(self.email_pattern, info_element)
        # Go to google page
        self.driver.get("https://accounts.google.com/SignOutOptions")
        # Find the logged-in accounts
        info_element = self.driver.find_element(By.TAG_NAME, 'body').text
        user_emails += re.findall(self.email_pattern, info_element)

        # Remove duplicate emails
        user_emails = list(set(user_emails))

        print(F"{len(user_emails)} emails found")
        print(user_emails)

        if save_to_file:
            # join emails with newline character and write it to file
            with open("FetchedEmails.txt", "a", encoding="utf-8") as file:
                file.write("\n".join(user_emails))

            print("Fetched emails have been saved to FetchedEmails.txt")

    def close(self):
        """
        Close the browser
        """
        self.driver.quit()


if __name__ == "__main__":
    chrome_email_fetcher = ChromeEmailFetcher()
    chrome_email_fetcher.run(save_to_file=True)
    chrome_email_fetcher.close()
