"""
PNR Status Checker for Indian Railways
Uses Selenium for web automation and OpenAI API for CAPTCHA solving
"""

import time
import base64
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import openai
import os
from dotenv import load_dotenv
from email_notifier import EmailNotifier
import json

# Load environment variables from .env file
load_dotenv()


class PNRChecker:
    def __init__(self, api_key):
        """Initialize the PNR checker with OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        options = webdriver.ChromeOptions()
        # Comment out headless mode for debugging
        # options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def solve_captcha_with_openai(self, image_base64):
        """
        Solve math CAPTCHA using OpenAI Vision API
        Returns the calculated answer
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",  # or gpt-4-vision-preview
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "This is a CAPTCHA image containing a simple math equation. Please solve it and return ONLY the numeric answer, nothing else."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=50
            )
            
            answer = response.choices[0].message.content.strip()
            # Extract only numeric value
            answer = ''.join(filter(str.isdigit, answer))
            print(f"CAPTCHA solved: {answer}")
            return answer
            
        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
            return None
    
    def capture_captcha_image(self):
        """Capture CAPTCHA image and convert to base64"""
        try:
            # Wait for CAPTCHA image to load
            captcha_img = self.wait.until(
                EC.presence_of_element_located((By.ID, "CaptchaImgID"))
            )
            
            # Get image source (base64 or URL)
            img_src = captcha_img.get_attribute('src')
            
            # Take screenshot of the element
            img_bytes = captcha_img.screenshot_as_png
            
            # Convert to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            print(f"Error capturing CAPTCHA: {e}")
            return None
    
    def parse_journey_table(self, table_element):
        """Parse the journey details table"""
        try:
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            
            # Get data from tbody
            data_row = table_element.find_element(By.TAG_NAME, "tbody").find_element(By.TAG_NAME, "tr")
            cells = data_row.find_elements(By.TAG_NAME, "td")
            
            journey_details = {
                'train_number': cells[0].text,
                'train_name': cells[1].text,
                'boarding_date': cells[2].text,
                'from': cells[3].text,
                'to': cells[4].text,
                'reserved_upto': cells[5].text,
                'boarding_point': cells[6].text,
                'class': cells[7].text
            }
            
            return journey_details
            
        except Exception as e:
            print(f"Error parsing journey table: {e}")
            return None
    
    def parse_passenger_table(self, table_element):
        """Parse the passenger details table"""
        try:
            tbody = table_element.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            passengers = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                passenger = {
                    'passenger_no': cells[0].text,
                    'booking_status': cells[1].text,
                    'current_status': cells[2].text,
                    'coach_position': cells[3].text if len(cells) > 3 else ''
                }
                passengers.append(passenger)
            
            return passengers
            
        except Exception as e:
            print(f"Error parsing passenger table: {e}")
            return None
    
    def display_results(self, journey_data, passenger_data):
        """Display the extracted results in a formatted way"""
        print("\n" + "="*80)
        print(" "*30 + "PNR STATUS RESULTS")
        print("="*80)
        
        if journey_data:
            print("\n📅 JOURNEY DETAILS:")
            print("-" * 80)
            print(f"Train Number      : {journey_data['train_number']}")
            print(f"Train Name        : {journey_data['train_name']}")
            print(f"Boarding Date     : {journey_data['boarding_date']}")
            print(f"From              : {journey_data['from']}")
            print(f"To                : {journey_data['to']}")
            print(f"Reserved Upto     : {journey_data['reserved_upto']}")
            print(f"Boarding Point    : {journey_data['boarding_point']}")
            print(f"Class             : {journey_data['class']}")
        
        if passenger_data:
            print("\n👥 PASSENGER DETAILS:")
            print("-" * 80)
            for passenger in passenger_data:
                print(f"\n{passenger['passenger_no']}:")
                print(f"  Booking Status  : {passenger['booking_status']}")
                print(f"  Current Status  : {passenger['current_status']}")
                if passenger['coach_position']:
                    print(f"  Coach Position  : {passenger['coach_position']}")
        
        print("\n" + "="*80 + "\n")
    
    def check_pnr(self, pnr_number, max_retries=3):
        """
        Main method to check PNR status
        Returns the PNR status information
        """
        try:
            print(f"Checking PNR: {pnr_number}")
            
            # Setup driver
            self.setup_driver()
            
            # Navigate to the website
            url = "https://www.indianrail.gov.in/enquiry/PNR/PnrEnquiry.html?locale=en"
            print(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Step 1: Enter PNR number
            print("Entering PNR number...")
            pnr_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "inputPnrNo"))
            )
            pnr_input.clear()
            pnr_input.send_keys(pnr_number)
            print(f"PNR {pnr_number} entered")
            
            # Step 2: Click first submit button
            print("Clicking submit button...")
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "modal1"))
            )
            submit_btn.click()
            
            # Step 3: Wait for modal to appear
            print("Waiting for CAPTCHA modal...")
            modal = self.wait.until(
                EC.visibility_of_element_located((By.ID, "firstCaptcha"))
            )
            print("Modal appeared")
            
            # Step 4: Capture and solve CAPTCHA
            retry_count = 0
            captcha_solved = False
            
            while retry_count < max_retries and not captcha_solved:
                print(f"Attempt {retry_count + 1} to solve CAPTCHA...")
                
                # Capture CAPTCHA image
                time.sleep(1)  # Wait for image to fully load
                captcha_base64 = self.capture_captcha_image()
                
                if not captcha_base64:
                    print("Failed to capture CAPTCHA image")
                    retry_count += 1
                    continue
                
                # Solve CAPTCHA using OpenAI
                answer = self.solve_captcha_with_openai(captcha_base64)
                
                if not answer:
                    print("Failed to solve CAPTCHA")
                    retry_count += 1
                    continue
                
                # Step 5: Enter CAPTCHA answer
                print(f"Entering CAPTCHA answer: {answer}")
                captcha_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "inputCaptcha"))
                )
                captcha_input.clear()
                captcha_input.send_keys(answer)
                
                # Step 6: Click final submit button
                print("Clicking final submit button...")
                final_submit = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "submitPnrNo"))
                )
                final_submit.click()
                
                # Wait a bit to see if CAPTCHA was correct
                time.sleep(3)
                
                # Check if modal is still visible (means wrong CAPTCHA)
                try:
                    modal_still_visible = self.driver.find_element(By.ID, "firstCaptcha").is_displayed()
                    if modal_still_visible:
                        print("CAPTCHA was incorrect, retrying...")
                        retry_count += 1
                        # Clear the input for next attempt
                        captcha_input.clear()
                    else:
                        captcha_solved = True
                        print("CAPTCHA solved successfully!")
                except:
                    # Modal not visible means success
                    captcha_solved = True
                    print("CAPTCHA solved successfully!")
            
            if not captcha_solved:
                print("Failed to solve CAPTCHA after maximum retries")
                return None
            
            # Step 7: Extract results
            print("Extracting PNR status...")
            time.sleep(3)  # Wait for results to load
            
            # Try to find the results section
            try:
                # Extract Journey Details Table
                journey_table = self.wait.until(
                    EC.presence_of_element_located((By.ID, "journeyDetailsTable"))
                )
                
                # Extract Passenger Details Table
                passenger_table = self.wait.until(
                    EC.presence_of_element_located((By.ID, "psgnDetailsTable"))
                )
                
                # Parse the tables
                journey_data = self.parse_journey_table(journey_table)
                passenger_data = self.parse_passenger_table(passenger_table)
                
                # Display the results
                self.display_results(journey_data, passenger_data)
                
                return {
                    'journey_details': journey_data,
                    'passenger_details': passenger_data
                }
                
            except Exception as e:
                print(f"Error extracting results: {e}")
                # Take a screenshot for debugging
                self.driver.save_screenshot("result_screenshot.png")
                print("Screenshot saved as result_screenshot.png")
                
                # Return page source for manual parsing
                return None
            
        except Exception as e:
            print(f"Error during PNR check: {e}")
            if self.driver:
                self.driver.save_screenshot("error_screenshot.png")
                print("Error screenshot saved")
            return None
            
        finally:
            # Cleanup
            if self.driver:
                print("Closing browser...")
                time.sleep(2)  # Give time to see results
                self.driver.quit()


def main():
    """Main function to run the PNR checker"""
    
    # Get OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("ERROR: Please set OPENAI_API_KEY environment variable")
        print("You can set it by running: $env:OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Check if running in automation mode (send emails)
    send_email = os.getenv('SEND_EMAIL', 'false').lower() == 'true'
    
    # Load PNR numbers from config or use default
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            pnr_numbers = config.get('pnr_numbers', ["2244293725"])
    else:
        pnr_numbers = ["2244293725"]
    
    # Create checker instance
    checker = PNRChecker(api_key)
    
    # Create email notifier if needed
    if send_email:
        notifier = EmailNotifier()
    
    # Check each PNR
    for pnr_number in pnr_numbers:
        print(f"\n{'='*80}")
        print(f"Processing PNR: {pnr_number}")
        print(f"{'='*80}")
        
        try:
            # Check PNR status
            result = checker.check_pnr(pnr_number)
            
            if result:
                print("\n✅ PNR check completed successfully!")
                
                # Send email notification if enabled
                if send_email:
                    print("\nSending email notification...")
                    email_sent = notifier.send_pnr_status(
                        pnr_number,
                        result.get('journey_details'),
                        result.get('passenger_details')
                    )
                    if email_sent:
                        print("✅ Email notification sent!")
                    else:
                        print("❌ Failed to send email notification")
            else:
                print("\n❌ PNR check failed!")
                
                # Send error notification if email is enabled
                if send_email:
                    notifier.send_error_notification(
                        pnr_number,
                        "Failed to retrieve PNR status. The system will retry on the next scheduled run."
                    )
        
        except Exception as e:
            print(f"\n❌ Error processing PNR {pnr_number}: {e}")
            
            # Send error notification if email is enabled
            if send_email:
                notifier.send_error_notification(pnr_number, str(e))
    
    print(f"\n{'='*80}")
    print("All PNR checks completed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
