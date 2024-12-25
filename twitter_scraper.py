from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from pymongo import MongoClient
import time
import datetime
import uuid

# Configuration
PROXY = "your_proxy_here"  # Replace with your ProxyMesh or other proxy details
PROXY_USER = "your_proxy_username"
PROXY_PASSWORD = "your_proxy_password"
EDGE_DRIVER_PATH = "C:/WebDriver/msedgedriver.exe" 

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection details
db = client["twitter_trends"]
collection = db["trends"]

def fetch_trending_topics():
    # Edge WebDriver setup
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")  # Run in headless mode for stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    edge_service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=edge_service, options=options)
    
    try:
        # Login to Twitter
        driver.get("https://x.com/login")
        time.sleep(5)  # Allow page to load
        
        # Replace with your login workflow
        username = driver.find_element(By.NAME, "text")
        username.send_keys("your_username_here")
        username.send_keys(Keys.RETURN)
        time.sleep(3)

        password = driver.find_element(By.NAME, "password")
        password.send_keys("your_password_here")
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        # Fetch trending topics
        trends = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] div span")[:5]
        trending_topics = [trend.text for trend in trends]

        # Get IP address
        driver.get("https://api.ipify.org?format=text")
        ip_address = driver.find_element(By.TAG_NAME, "body").text

        # Create a record
        unique_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "_id": unique_id,
            "trend1": trending_topics[0],
            "trend2": trending_topics[1],
            "trend3": trending_topics[2],
            "trend4": trending_topics[3],
            "trend5": trending_topics[4],
            "timestamp": timestamp,
            "ip_address": ip_address
        }

        # Store in MongoDB
        collection.insert_one(record)
        return record

    finally:
        driver.quit()

# Run script for testing
if __name__ == "__main__":
    result = fetch_trending_topics()
    print("Data fetched and stored in MongoDB:", result)
