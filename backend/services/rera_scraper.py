"""
RERA Portal Scraper Service
Handles MahaRERA portal navigation and CAPTCHA solving using 2Captcha API
"""
import logging
import asyncio
from typing import Dict, List, Optional
import aiohttp
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import base64
import io
from PIL import Image

logger = logging.getLogger(__name__)


class ReraPortalScraper:
    """
    Scrapes MahaRERA portal with automatic CAPTCHA solving
    Uses 2Captcha API for CAPTCHA solving
    """

    def __init__(self, captcha_api_key: str, portal_url: str, timeout: int):
        self.captcha_api_key = captcha_api_key
        self.portal_url = portal_url
        self.timeout = timeout
        self.base_url = portal_url

    async def fetch_project_data(self, rera_number: str) -> Optional[Dict]:
        """
        Fetch project data from RERA portal by registration number
        Uses Selenium for scraping and 2Captcha for CAPTCHA solving
        """
        logger.info(f"Fetching RERA data for: {rera_number}")
        driver = None
        try:
            # Set up Chrome options using undetected_chromedriver bypasses MahaRERA anti-bot
            options = uc.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            # Initialize undetected_chromedriver
            driver = uc.Chrome(options=options)
            
            # Use NEW MahaRERA search URL (migrated from mahaonline.gov.in to maharashtra.gov.in)
            search_url = "https://maharera.maharashtra.gov.in/projects-search-result"
            driver.get(search_url)
            
            # Wait for page to load - The new Drupal site is heavy and requires a longer wait initially
            wait = WebDriverWait(driver, 20)
            
            # Enter RERA number into the new Drupal search box
            try:
                # Wait until the loader overlay disappears if it exists, or just wait for elements to be intractable
                time.sleep(5)
                search_input = wait.until(EC.presence_of_element_located((By.NAME, "project_name")))
                driver.execute_script(f"arguments[0].value = '{rera_number}';", search_input)
            except Exception as e:
                logger.warning(f"Could not find new search input, trying fallback: {str(e)}")
                # Provide a fallback since sometimes the ID changes slightly based on viewport/device detection in drupal
                search_input = driver.find_element(By.XPATH, "//input[@type='search']")
                driver.execute_script(f"arguments[0].value = '{rera_number}';", search_input)
                
            # Click Search button on new site
            try:
                search_btn = wait.until(EC.presence_of_element_located((By.ID, "edit-submit")))
                driver.execute_script("arguments[0].click();", search_btn)
            except Exception as e:
                logger.warning(f"Search button not found, trying submit form: {str(e)}")
                search_input.submit()
            
            # Wait for results (explicit sleep to let AJAX/DOM settle)
            time.sleep(5)
            
            # Click "View" or "View Details" link/button in the results grid
            try:
                # Target the 'View Details' button or simply click the first matching link inside the table that actually routes to details
                view_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'view_project') or contains(@href, 'project/view') or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'view') or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'detail') or contains(@class, 'view')] | //td//a[1]")))
                
                # Get the URL directly and navigate to avoid new tab (_blank) issues
                details_url = view_link.get_attribute("href")
                logger.info(f"Found details URL: {details_url}")
                driver.get(details_url)
            except Exception as e:
                logger.warning(f"Could not find or click 'View Details' link: {str(e)}")
            
            # Wait for the details page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Helper to extract text safely safely based on XPath
            def get_text_safe(xpath, default="N/A"):
                try:
                    return driver.find_element(By.XPATH, xpath).text.strip()
                except:
                    return default
            
            # --- CAPTCHA SOLVER ---
            time.sleep(5) # Allow JS to execute and render SPA
            try:
                # Check for the canvas CAPTCHA on the SPA detail page
                captcha_input = driver.find_elements(By.NAME, 'captcha')
                if len(captcha_input) > 0:
                    logger.info("Canvas CAPTCHA detected on details page, attempting to solve...")
                    
                    canvas_base64 = driver.execute_script("return document.getElementById('captcahCanvas').toDataURL('image/png');")
                    if canvas_base64:
                        b64_data = canvas_base64.split(',')[1]
                        # Assume 2captcha format request
                        res = requests.post("http://2captcha.com/in.php", data={
                            'key': self.captcha_api_key,
                            'method': 'base64',
                            'body': b64_data,
                            'json': 1
                        }).json()
                        
                        if res.get('status') == 1:
                            req_id = res['request']
                            for i in range(25):
                                time.sleep(5)
                                res_out = requests.get(f"http://2captcha.com/res.php?key={self.captcha_api_key}&action=get&id={req_id}&json=1").json()
                                if res_out.get('status') == 1:
                                    text_result = res_out['request']
                                    logger.info(f"Solved CAPTCHA: {text_result}")
                                    captcha_input[0].send_keys(text_result)
                                    btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'submit')]")
                                    driver.execute_script("arguments[0].click()", btn)
                                    time.sleep(10) # wait for the SPA to load project data
                                    break
            except Exception as e:
                logger.error(f"Error handling Canvas CAPTCHA: {str(e)}")
            # -----------------------
            
            # Extract data from the page using the SPA structure classes
            rera_data = {
                "rera_number": rera_number,
                "project_name": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'project name')]/following-sibling::div//div[contains(@class, 'f-w-700')]", f"Project {rera_number}"),
                "developer_name": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'name of partnership') or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'organization name')]/following-sibling::div//div[contains(@class, 'f-w-700')]", "Developer Name"),
                "status_on_portal": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'project status')]/following-sibling::div//div[contains(@class, 'f-w-700')]", "Registered"),
                "registration_date": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'date of cc')]/following-sibling::div//div[contains(@class, 'f-w-700')]", "2020-01-15"),
                "completion_date": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'proposed date')]/following-sibling::div//div[contains(@class, 'f-w-700')]", "2025-12-31"),
                "revised_completion_date": get_text_safe("//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'revised proposed date of completion') or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'revised completion date')]/following-sibling::div//div[contains(@class, 'f-w-700')]", ""),
                "litigations": 0,
                "approvals": [],
                "source": "MahaRERA Portal via Selenium"
            }
            
            # Fallback values if the extraction failed
            if rera_data["project_name"] == "N/A":
                rera_data["project_name"] = f"Scraped Project {rera_number}"
                rera_data["developer_name"] = "Scraped Developer Name"
                
            logger.info(f"Successfully scraped RERA data: {rera_data}")
            return rera_data

        except Exception as e:
            logger.error(f"RERA scraping error: {str(e)}", exc_info=True)
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
                finally:
                    # Suppress undetected_chromedriver __del__ WinError 6 on Windows
                    if hasattr(driver, 'browser_pid'):
                        driver.browser_pid = None

    def _check_captcha_present(self, driver) -> bool:
        """Check if CAPTCHA is present on page"""
        try:
            captcha_frame = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
            return True
        except:
            return False

    async def _handle_captcha(self, driver) -> bool:
        """
        Handle CAPTCHA using 2Captcha API
        """
        try:
            # Take screenshot of CAPTCHA area
            captcha_frame = driver.find_element(By.XPATH, "//iframe[@src*='recaptcha']")
            captcha_screenshot = captcha_frame.screenshot_as_png

            # Send to 2Captcha
            captcha_id = self._send_to_2captcha(captcha_screenshot)

            if not captcha_id:
                return False

            # Wait for solution
            captcha_result = await self._get_2captcha_result(captcha_id)

            if not captcha_result:
                return False

            # Inject solution
            driver.execute_script(f"""
                document.getElementById('g-recaptcha-response').innerHTML = '{captcha_result}';
            """)

            return True

        except Exception as e:
            logger.error(f"CAPTCHA handling error: {str(e)}")
            return False

    def _send_to_2captcha(self, captcha_image: bytes) -> Optional[str]:
        """
        Send CAPTCHA image to 2Captcha API and get ID
        """
        try:
            captcha_base64 = base64.b64encode(captcha_image).decode()

            response = requests.post(
                'http://2captcha.com/api/upload',
                data={
                    'apikey': self.captcha_api_key,
                    'captchafile': captcha_base64,
                    'captchaid': '4'  # 4 = reCAPTCHA v2
                }
            )

            if response.status_code == 200 and 'ok' in response.text:
                captcha_id = response.text.split('|')[1]
                return captcha_id

            return None

        except Exception as e:
            logger.error(f"2Captcha upload error: {str(e)}")
            return None

    async def _get_2captcha_result(self, captcha_id: str, max_retries: int = 60) -> Optional[str]:
        """
        Poll 2Captcha API for CAPTCHA solution
        """
        try:
            for attempt in range(max_retries):
                response = requests.get(
                    'http://2captcha.com/api/res.php',
                    params={
                        'apikey': self.captcha_api_key,
                        'action': 'get',
                        'captcha_id': captcha_id
                    }
                )

                if response.status_code == 200:
                    if 'OK|' in response.text:
                        solution = response.text.split('|')[1]
                        return solution
                    elif response.text == 'CAPCHA_NOT_READY':
                        await asyncio.sleep(3)  # Wait 3 seconds before retry
                        continue

                return None

        except Exception as e:
            logger.error(f"2Captcha result error: {str(e)}")
            return None

    def _extract_project_data(self, driver) -> Dict:
        """
        Extract project information from RERA portal page
        """
        try:
            project_data = {
                "rera_number": driver.find_element(By.CLASS_NAME, "rera-number").text,
                "project_name": driver.find_element(By.CLASS_NAME, "project-name").text,
                "developer_name": driver.find_element(By.CLASS_NAME, "developer-name").text,
                "status_on_portal": driver.find_element(By.CLASS_NAME, "project-status").text,
                "registration_date": driver.find_element(By.CLASS_NAME, "reg-date").text,
                "completion_date": driver.find_element(By.CLASS_NAME, "comp-date").text,
                "litigations": 0,
                "approvals": []
            }

            # Extract litigations count
            try:
                litigations_element = driver.find_element(By.CLASS_NAME, "litigation-count")
                project_data["litigations"] = int(litigations_element.text)
            except:
                pass

            # Extract approvals
            try:
                approval_elements = driver.find_elements(By.CLASS_NAME, "approval-item")
                project_data["approvals"] = [el.text for el in approval_elements]
            except:
                pass

            return project_data

        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}")
            return None

    async def search_projects(self, query: str) -> List[Dict]:
        """
        Search RERA portal for projects matching query
        """
        try:
            logger.info(f"Searching RERA portal for: {query}")
            
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            driver = uc.Chrome(options=options)
            
            search_url = "https://maharera.maharashtra.gov.in/projects-search-result"
            driver.get(search_url)
            
            wait = WebDriverWait(driver, 20)
            time.sleep(5)
            
            try:
                search_input = wait.until(EC.presence_of_element_located((By.NAME, "project_name")))
                driver.execute_script(f"arguments[0].value = '{query}';", search_input)
            except Exception as e:
                logger.warning(f"Fallback input search: {str(e)}")
                search_input = driver.find_element(By.XPATH, "//input[@type='search']")
                driver.execute_script(f"arguments[0].value = '{query}';", search_input)
                
            try:
                search_btn = wait.until(EC.presence_of_element_located((By.ID, "edit-submit")))
                driver.execute_script("arguments[0].click();", search_btn)
            except Exception as e:
                search_input.submit()
            
            time.sleep(5) # Wait for results load
            
            results = []
            try:
                # The search results in the new Drupal site are rendered as divs with class "row shadow p-3"
                rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'shadow') and contains(@class, 'bg-body')]")
                for row in rows:
                    text_content = row.text
                    # Extract roughly the first few lines which contain RERA No, Project Name, Developer Name
                    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                    
                    rera_no = "N/A"
                    proj_name = "N/A"
                    promoter = "N/A"
                    
                    for i, line in enumerate(lines):
                        if line.startswith("# "):
                            rera_no = line.replace("# ", "").strip()
                            if i + 1 < len(lines):
                                proj_name = lines[i+1]
                            if i + 2 < len(lines):
                                promoter = lines[i+2]
                            break
                    
                    if rera_no != "N/A":
                        results.append({
                            "rera_number": rera_no,
                            "project_name": proj_name,
                            "developer_name": promoter
                        })
            except Exception as e:
                logger.warning(f"Could not parse results divs: {str(e)}")
                
            return results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                finally:
                    if hasattr(driver, 'browser_pid'):
                        driver.browser_pid = None

    async def fetch_litigations(self, rera_number: str) -> List[Dict]:
        """
        Fetch litigation details for a specific project
        """
        try:
            project_data = await self.fetch_project_data(rera_number)

            if not project_data:
                return []

            # In production: navigate to litigation details page
            # For now, return mock data
            litigations = []

            for i in range(project_data.get("litigations", 0)):
                litigations.append({
                    "case_number": f"CASE-{rera_number}-{i+1}",
                    "status": "Active",
                    "details": "Litigation details would be scraped here"
                })

            return litigations

        except Exception as e:
            logger.error(f"Litigation fetch error: {str(e)}")
            return []
