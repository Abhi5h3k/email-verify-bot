# verify_email.py
import os
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from rich.console import Console
from rich.progress import Progress

class VerifyEmail:
    def __init__(
        self,
        domain_key: str,
        input_file_name: str,
        headless: bool = True,
        sleep: int = 5,
        skip_other_domain: bool = False,
    ):
        self.console = Console()
        self.options = Options()

        if headless:
            self.options.add_argument("--headless=new")

        self.sleep = sleep
        self.domain_key = domain_key
        self.input_file_name = input_file_name
        self.skip_other_domain = str(skip_other_domain)

        self.output_dir = "./output/"
        os.makedirs(self.output_dir, exist_ok=True)

        domain_names = {
            "1": "aol.com",
            "2": "yahoo.com",
            "3": "comcast.net",
        }

        domain_names_config = {
            "1": "aol.json",
            "2": "yahoo.json",
            "3": "comcast.json",
        }

        self.domain = domain_names[self.domain_key]
        self.config_json = json.load(open(f"./config_json/{domain_names_config[self.domain_key]}", "r"))

        with open(self.input_file_name) as f:
            self.data_list = [line.strip() for line in f if line.strip()]

        if not self.data_list:
            self.console.print(f"[red]No emails found in {self.input_file_name}")
            return

        self.console.print(f"[cyan]Running for domain: {self.domain}")

        if self.domain_key == "1":
            self.aol_runner()
        elif self.domain_key == "2":
            self.yahoo_runner()
        elif self.domain_key == "3":
            self.comcast_runner()

    def write_to_file(self, email, f_name):
        timestr = time.strftime("%Y%m%d")
        filepath = os.path.join(self.output_dir, f"{f_name}_{timestr}_.txt")
        with open(filepath, "a") as fp:
            fp.write(f"{email}\n")
        self.console.print(f"[green]Written to file: {f_name}")

    def aol_runner(self):
        url = self.config_json["url"]
        email_xpath = self.config_json["email_xpath"]
        error_xpath = self.config_json["email_error_xpath"]
        error_texts = [
            self.config_json.get("on_error_text1", ""),
            self.config_json.get("on_error_text2", ""),
        ]

        driver = webdriver.Chrome(options=self.options)
        driver.get(url)
        wait = WebDriverWait(driver, self.sleep)

        with Progress() as progress:
            task = progress.add_task("[red]Checking emails...", total=len(self.data_list))
            for index, email in enumerate(self.data_list):
                progress.update(task, advance=1)
                uname, domain = email.split("@")

                if self.skip_other_domain == "True" and domain != "aol.com":
                    self.console.print(f"[yellow]Skipping {email} (not aol.com)")
                    continue

                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, email_xpath)))
                    email_field = driver.find_element(By.XPATH, email_xpath)
                    email_field.clear()
                    email_field.send_keys(uname)
                    time.sleep(1)
                    error_field = driver.find_element(By.XPATH, error_xpath)

                    if error_field.text.strip() in error_texts:
                        self.console.print(f"{email} [green]PASS")
                        self.write_to_file(email, "aol_email_pass")
                    else:
                        self.console.print(f"{email} [red]FAIL")
                        self.write_to_file(email, "aol_email_fail")

                except Exception as e:
                    self.console.print(f"[red]Error checking {email}: {str(e)}")

        driver.quit()

    def yahoo_runner(self):
        log = logging.getLogger("my_logger")
        try:
            print("Running for yahoo:")
            url = self.config_json["url"]

            driver = webdriver.Chrome(options=self.options)

            driver.get(url)

            wait = WebDriverWait(driver, self.sleep)

            email_pass = []
            email_fail = []
            with Progress() as progress:
                task1 = progress.add_task("[red]Working...", total=len(self.data_list))

                for index, email in enumerate(self.data_list):

                    progress.update(task1, advance=1)

                    uname = email.split("@")[0]
                    uname_domain = email.split("@")[1]

                    if self.skip_other_domain == "True":
                        if uname_domain != "yahoo.com":
                            print(f"\n===skip check for domain : {uname_domain}===")
                            continue

                    print(f"{index} check : {uname}")
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//input[@name='userId']")
                        )
                    )
                    uemail_field = driver.find_element(
                        "xpath", "//input[@name='userId']"
                    )
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//input[@name='firstName']")
                        )
                    )
                    firstName_field = driver.find_element(
                        "xpath", "//input[@name='firstName']"
                    )
                    uemail_field.clear()
                    uemail_field.send_keys(uname)
                    firstName_field.click()
                    time.sleep(self.sleep)
                    error_field = driver.find_element(
                        "xpath", "//*[@id='reg-error-userId']"
                    )
                    if (
                        error_field.text == self.config_json["on_error_text1"]
                        or error_field.text == self.config_json["on_error_text2"]
                    ):
                        # print(error_field.text)
                        self.console.print(f"\n{email} [green1]PASS")
                        email_pass.append(email)
                        self.write_to_file(email, "yahoo_email_pass")
                    else:
                        self.console.print(f"\n{email} [deep_pink4]FAIL")
                        email_fail.append(email)
                        self.write_to_file(email, "yahoo_email_fail")

            print(f"Total Email Pass : {len(email_pass)}")
            print(f"Total Email Fail : {len(email_fail)}")
            log.info(f"Total Email Pass : {len(email_pass)}")
            log.info(f"Total Email Fail : {len(email_fail)}")

            driver.quit()

        except Exception as e:
            print(e)
            log.error(e)

    def comcast_runner(self):
        log = logging.getLogger("my_logger")
        try:
            print("Running for comcast:")
            url = self.config_json["url"]
            email_xpath = self.config_json["email_xpath"]
            submit_btn_xpath = self.config_json["submit_btn_xpath"]
            error_field_xpath = self.config_json["error_field_xpath"]


            driver = webdriver.Chrome(options=self.options)

            driver.get(url)

            wait = WebDriverWait(driver, self.sleep)

            email_pass = []
            email_fail = []

            with Progress() as progress:
                task1 = progress.add_task("[red]Working...", total=len(self.data_list))

                for index, email in enumerate(self.data_list):
                    try:
                        progress.update(task1, advance=1)

                        uname = email.split("@")[0]
                        uname_domain = email.split("@")[1]

                        if self.skip_other_domain == "True":
                            if uname_domain != "comcast.net":
                                print(f"\n===skip check for domain : {uname_domain}===")
                                continue

                        print(f"{index} check : {uname}")
                        wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, email_xpath)
                            )
                        )
                        uemail_field = driver.find_element(
                            "xpath", email_xpath
                        )

                        password_field = driver.find_element(By.XPATH, submit_btn_xpath)

                        

                        uemail_field.clear()
                        uemail_field.send_keys(uname)


                        # Ensure visible and scroll into view
                        driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
                        wait.until(EC.visibility_of(password_field))

                        # Try normal click, fallback to JS
                        try:
                            password_field.click()
                        except ElementClickInterceptedException:
                            print("[yellow]Click intercepted, using JS fallback...")
                            driver.execute_script("arguments[0].click();", password_field)
 
                        time.sleep(self.sleep)

                        try:
                            error_field = driver.find_element(
                                "xpath",
                                error_field_xpath,
                            )
                            if error_field.text == self.config_json["on_error_text"]:
                                self.console.print(f"\n{email} [deep_pink4]FAIL")
                                email_fail.append(email)
                                self.write_to_file(email, "comcast_email_fail")

                        except NoSuchElementException:
                            print(f"1 : {NoSuchElementException}")
                            self.console.print(f"\n{email} [green1]PASS")
                            email_pass.append(email)
                            self.write_to_file(email, "comcast_email_pass")
                            # time.sleep(self.sleep)
                            # try:
                            #     reload_field = driver.find_element(
                            #             "xpath", "/html/body/main/div[2]/prism-box/form/prism-button[3]/a/prism-text")
                            #     reload_field.click()
                            # except NoSuchElementException:
                            #     print(f'2 : {NoSuchElementException}')
                            # if self.config_json["compromised"] in driver.current_url:
                            #     print("\nemail compromised")
                            driver.back()
                            driver.refresh()

                        except ElementClickInterceptedException:
                            print(ElementClickInterceptedException)
                            log.error(f"{email} : {ElementClickInterceptedException}")
                        except TimeoutException:
                            print(f"{email} :{TimeoutException}")
                            log.error(f"{email} :{TimeoutException}")

                        except Exception as e:
                            print(e)
                            log.error(e)

                    except TimeoutException:
                        print(f"{email} [continue] :{TimeoutException}")
                        log.error(f"{email} [continue] :{TimeoutException}")
                        driver.back()
                        driver.refresh()
                        print("continue sleep..5")
                        time.sleep(5)
                        continue

            print(f"Total Email Pass : {len(email_pass)}")
            print(f"Total Email Fail : {len(email_fail)}")
            log.info(f"Total Email Pass : {len(email_pass)}")
            log.info(f"Total Email Fail : {len(email_fail)}")
            driver.quit()
        except ElementClickInterceptedException:
            print(ElementClickInterceptedException)
            log.error(ElementClickInterceptedException)
        except TimeoutException:
            print(f"{email} :{TimeoutException}")
            log.error(f"{email} :{TimeoutException}")
        except Exception as e:
            print(e)
            log.error(e)
