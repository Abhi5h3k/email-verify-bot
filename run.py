from turtle import st
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# import undetected_chromedriver.v2 as uc
import time
import yaml
import json

import logging

from rich.progress import track
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

import os

import threading
import multiprocessing
from selenium.webdriver.chrome.options import Options


# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


class VerifyEmail:
    def __init__(self):
        log = logging.getLogger("my_logger")
        try:
            os.makedirs(os.path.dirname("./output/"), exist_ok=True)

            self.console = Console()
            self.options = Options()

            headless = input("Run headless (default True): ") or "True"
            if headless != "True" and headless != "False":
                self.options.headless = True
            elif headless == "True":
                self.options.headless = True
            elif headless == "False":
                self.options.headless = False

            self.sleep = int(input("Enter delay in sec (default 5): ") or 5)
            print(f"Delay : {self.sleep}")

            # select domain to work on
            domain_names = {
                "1": "aol.com",
                "2": "yahoo.com",
                "3": "xfinity.com (comcast)",
            }
            print("\nSelect Domain to work on:")
            print(yaml.dump(domain_names, default_flow_style=False))
            self.domain = input("Select Domain: ")

            print(f"\nWorking on domain : {domain_names[self.domain]}")
            self.skip_other_domain = (
                input("Skip other Domain [default False]: ") or "False"
            )

            if self.skip_other_domain != "True" and self.skip_other_domain != "False":
                self.skip_other_domain = "False"
            print(f"skip_other_domain = {self.skip_other_domain}")

            # input data file name
            self.input_file_name = input("\nEnter input text filename with extension: ")
            print(f"\nRead data from : {self.input_file_name}")

            # read file data into list
            with open(self.input_file_name) as f:
                self.data_list = [line.rstrip() for line in f if line.rstrip()]
            print(f"\nTotal records in file : {len(self.data_list)}")

            if len(self.data_list):
                # if we have data
                domain_names_config = {
                    "1": "aol.json",
                    "2": "yahoo.json",
                    "3": "comcast.json",
                }
                config_json = open(f"./config_json/{domain_names_config[self.domain]}")
                self.config_json = json.load(config_json)

                if self.domain == "1":
                    # aol
                    self.aol_runner(self.data_list)

                elif self.domain == "2":
                    # yahoo
                    self.yahoo_runner(self.data_list)

                elif self.domain == "3":
                    # comcast
                    self.comcast_runner(self.data_list)

            else:
                # if file is empty
                print(f"{len(self.data_list)} records in {self.input_file_name}")

        except Exception as e:
            print(e)
            log.error(e)

    def split(self, list_a, chunk_size):
        for i in range(0, len(list_a), chunk_size):
            yield list_a[i : i + chunk_size]

    def aol_runner(self, data_list):
        log = logging.getLogger("my_logger")
        try:
            print("Running for aol:")

            url = self.config_json["url"]

            driver = uc.Chrome(
                executable_path="./driver/chromedriver.exe",
                use_subprocess=True,
                options=self.options,
            )
            driver.get(url)

            wait = WebDriverWait(driver, self.sleep + 5)

            email_pass = []
            email_fail = []
            with Progress() as progress:
                task1 = progress.add_task("[red]Working...", total=len(data_list))

                for index, email in enumerate(data_list):

                    progress.update(task1, advance=1)

                    uname = email.split("@")[0]
                    uname_domain = email.split("@")[1]

                    if self.skip_other_domain == "True":
                        if uname_domain != "aol.com":
                            print(f"\n===skip check for domain : {uname_domain}===")
                            continue

                    print(f"{index} check : {uname}")
                    wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@name='yid']"))
                    )
                    uemail_field = driver.find_element("xpath", "//input[@name='yid']")
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
                    time.sleep(5)
                    error_field = driver.find_element(
                        "xpath", "//*[@id='reg-error-yid']"
                    )

                    if (
                        error_field.text == self.config_json["on_error_text1"]
                        or error_field.text == self.config_json["on_error_text2"]
                    ):
                        # print(error_field.text)
                        self.console.print(f"\n{email} [green1]PASS")
                        email_pass.append(email)
                        self.write_to_file(email, "aol_email_pass")
                    else:
                        self.console.print(f"\n{email} [deep_pink4]FAIL")
                        email_fail.append(email)
                        self.write_to_file(email, "aol_email_fail")

            print(f"Total Email Pass : {len(email_pass)}")
            print(f"Total Email Fail : {len(email_fail)}")
            log.info(f"Total Email Pass : {len(email_pass)}")
            log.info(f"Total Email Fail : {len(email_fail)}")

            driver.quit()

        except Exception as e:
            print(e)
            log.error(e)

    def yahoo_runner(self, data_list):
        log = logging.getLogger("my_logger")
        try:
            print("Running for yahoo:")
            url = self.config_json["url"]

            driver = uc.Chrome(
                executable_path="./driver/chromedriver.exe",
                use_subprocess=True,
                options=self.options,
            )
            driver.get(url)

            wait = WebDriverWait(driver, self.sleep)

            email_pass = []
            email_fail = []
            with Progress() as progress:
                task1 = progress.add_task("[red]Working...", total=len(data_list))

                for index, email in enumerate(data_list):

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

    def comcast_runner(self, data_list):
        log = logging.getLogger("my_logger")
        try:
            print("Running for comcast:")
            url = self.config_json["url"]

            driver = uc.Chrome(
                executable_path="./driver/chromedriver.exe",
                use_subprocess=True,
                options=self.options,
            )
            driver.get(url)

            wait = WebDriverWait(driver, self.sleep)

            email_pass = []
            email_fail = []

            with Progress() as progress:
                task1 = progress.add_task("[red]Working...", total=len(data_list))

                for index, email in enumerate(data_list):
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
                                (By.XPATH, "//input[@name='user']")
                            )
                        )
                        uemail_field = driver.find_element(
                            "xpath", "//input[@name='user']"
                        )

                        wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[@type='submit']")
                            )
                        )
                        password_field = driver.find_element(
                            "xpath", "//button[@type='submit']"
                        )

                        uemail_field.clear()
                        uemail_field.send_keys(uname)
                        password_field.click()

                        time.sleep(self.sleep)

                        try:
                            error_field = driver.find_element(
                                "xpath",
                                "/html/body/main/div[2]/prism-box/form/prism-input/span[2]/prism-text",
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

    def write_to_file(self, result_list, f_name):
        log = logging.getLogger("my_logger")
        try:
            import time

            timestr = time.strftime("%Y%m%d")
            with open(f"./output/{f_name}_{timestr}_.txt", "a") as fp:
                # for item in result_list:
                #         # write each item on a new line
                #     fp.write("%s\n" % item)
                fp.write(f"{result_list}\n")

            print(f"\nWritten to File : \033[32;1m{f_name}\033[0m")

        except Exception as e:
            log.error(e)


def print_author(msg):
    print("\n" * 5)
    print("*=" * 20)
    print()
    print("GitHub : https://github.com/Abhi5h3k")
    print()
    print(msg)
    print()
    print("*=" * 20)
    print("\n" * 5)


if __name__ == "__main__":
    from logger import Logger

    Logger()
    print_author("Verify email for multiple domains (yahoo, aol , comcast...)")
    VerifyEmail()
