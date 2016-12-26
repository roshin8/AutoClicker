from selenium import webdriver
from selenium.webdriver.common.proxy import *
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import random
import os
import re
import argparse
import gspread

GOOGLE_CREDENTIAL = "Auto Clicker-2717f5630d01.json"
HOME = os.environ['HOME']

FIREFOX_PROFILE = {
    "PS": "x73fnv5a.ps",
    "MUD": "79vlchet.mud"
}

WEBSITE_XPATH = {
    "SHORTE_ST": ".//*[@id='skip_button']",
    "LINKSHRINK": ".//*[@id='skip']/div/a",
    "P_PW": './/*[contains(text(), "Skip Ad")]',
    "LINKBUCKS": ".//*[@id='skiplink']",
    "ADMYLINK": ".//*[@id='btnContinue']",
    "ITY_IM": "html/body/header/div/div[3]/a/img",
    "YSEARCH": ".//*[@id='NextVideo']"
}


WEBSITE_LINKS = {
    "SHORTE_ST": ["http://viid.me/qqRiyw",
                  "http://viid.me/qw9fyo"
                  ],

    "ADMYLINK": ["http://admy.link/d6d24e",
                 "http://admy.link/87c452",
                 "http://admy.link/8524d9",
                 "http://admy.link/170efb",
                 "http://admy.link/ee3299",
                 "http://admy.link/1705a2",
                 "http://admy.link/1b158a",
                 "http://admy.link/dd287d",
                 "http://admy.link/2cb85a",
                 "http://admy.link/bfbaf8",
                 "http://admy.link/1dad19",  # 10
                 "http://admy.link/898768",
                 "http://admy.link/962e7e",
                 "http://admy.link/37be1f",
                 "http://admy.link/f31c5a"
                 ],

    "YSEARCH": ["http://ysear.ch/a39ddv",
                "http://ysear.ch/i656hq",
                "http://ysear.ch/dvmmch",
                "http://ysear.ch/ogapoj",
                "http://ysear.ch/s8oon5",
                "http://ysear.ch/shugxe",
                "http://ysear.ch/7kwiis",
                "http://ysear.ch/tzzoba",  # 7
                "http://ysear.ch/8d1pvy",
                "http://ysear.ch/kwkdon",
                "http://ysear.ch/ngt1gm"
                ]
}

WEBSITE_TEXT = {
    "ADHYPE": "Skip"
}

PROXY_PROFILE = {
    "PS": "proxy_list_ps.txt",
    "MUD": "proxy_list_mud.txt"
}


class Auto_Clicker:
    def __init__(self):
        self.args_setup()

    def args_setup(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--website', type=str, help='Specify which Website', required=True)
        parser.add_argument('--profile', type=str, help='Specify which Profile', required=True)

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--random', help='Specify if random', action='store_true')
        group.add_argument('--link', type=int, help='Specify link index to hit')

        self.args = parser.parse_args()

    def change_proxy(self, proxy_host, proxy_port):
        profile = webdriver.FirefoxProfile(HOME + "/.mozilla/firefox/" + FIREFOX_PROFILE[self.args.profile])
        profile.set_preference("network.proxy.type", 1)
        # HTTP
        profile.set_preference("network.proxy.http", proxy_host)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        # SOCKS
        profile.set_preference("network.proxy.socks", proxy_host)
        profile.set_preference("network.proxy.socks_port", int(proxy_port))
        profile.set_preference("network.proxy.socks_version", 5)
        # SSL
        profile.set_preference("network.proxy.ssl", proxy_host)
        profile.set_preference("network.proxy.ssl_port", int(proxy_port))
        # FTP
        profile.set_preference("network.proxy.ftp", proxy_host)
        profile.set_preference("network.proxy.ftp_port", int(proxy_port))
        profile.update_preferences()
        return webdriver.Firefox(firefox_profile=profile)

    def click_element_by_xpath(self, element_xpath, chosen_url):
        while True:
            time.sleep(5)
            try:
                is_element = self.driver.find_element_by_xpath(element_xpath)
                if is_element.is_displayed():
                    is_element.click()
            except:
                if self.driver.current_url != chosen_url:
                    break

    def click_element_by_link_text(self, element_text):
        while True:
            time.sleep(5)
            try:
                is_element = self.driver.find_element_by_link_text(element_text)
                if is_element.is_displayed():
                    is_element.click()
            except:
                if self.driver.current_url != chosen_url:
                    break

    def get_google_sheet(self, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds',  # Used to Open Spreadsheets
                 'https://www.googleapis.com/auth/drive'  # Used to Create Spreadsheets
                 ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIAL, scope)
        google_cred = gspread.authorize(credentials)
        try:
            spreadsheet = google_cred.open(sheet_name).sheet1
        except:
            spreadsheet = google_cred.create(sheet_name)
            spreadsheet.share('roshinrulz28@gmail.com', perm_type='user', role='writer')
            spreadsheet = google_cred.open(sheet_name).sheet1
        return spreadsheet

    def get_used_proxy_list_and_count(self, chosen_url):
        index_of_link = WEBSITE_LINKS[self.args.website].index(chosen_url)
        used_proxy_list = self.worksheet.col_values(index_of_link + 1)
        # filter is used because the list obtained will have empty strings
        # Eg: ['IP:PORT', 'IP:PORT', '', '', '']
        # This count is used to continue appending the proxy list to the column
        # and prevent from overwriting.
        count = len(filter(None, used_proxy_list)) + 1
        return (index_of_link, used_proxy_list, count)

    def truncate_sheet(self):
        date_sheet = self.get_google_sheet("DATE")
        old_date = date_sheet.cell(1, 1).value
        current_date = datetime.now().strftime("%d-%m-%Y")
        if old_date != current_date:
            # Truncate sheet if next day
            date_sheet.update_cell(1, 1, current_date)
            cell_list = self.worksheet.findall(re.compile(r':'))
            for cell in cell_list:
                cell.value = ''
            self.worksheet.update_cells(cell_list)

    def start(self):
        with open(PROXY_PROFILE[self.args.profile], 'r') as f:
            proxy_list = f.read().splitlines()

        random.shuffle(proxy_list)

        self.worksheet = self.get_google_sheet('USED_PROXY_LIST_FOR_' + self.args.website)
        self.truncate_sheet()

        if not self.args.random:
            chosen_url = WEBSITE_LINKS[self.args.website][self.args.link]
            (index_of_link, used_proxy_list, count) = self.get_used_proxy_list_and_count(chosen_url)

        for proxy in proxy_list:
            if proxy in used_proxy_list:
                continue

            if self.args.random:
                chosen_url = random.choice(WEBSITE_LINKS[self.args.website])
                (index_of_link, used_proxy_list, count) = self.get_used_proxy_list_and_count(chosen_url)

            line = proxy.split(":")
            proxy_host = line[0]
            proxy_port = line[1]
            self.driver = self.change_proxy(proxy_host, proxy_port)

            try:
                self.driver.set_page_load_timeout(180)
                self.driver.get(chosen_url)
                self.click_element_by_xpath(WEBSITE_XPATH[self.args.website], chosen_url)
                # Updates the cell based on cordinates. (1, 3), (2, 3)..
                self.worksheet.update_cell(count, index_of_link + 1, proxy)
                print "Clicked: ", count
                time.sleep(15)
            except:
                print "Proxy took too long to load. Skipping it."
                try:
                    self.worksheet.update_cell(count, index_of_link + 1, proxy)
                except:
                    # Time out
                    self.worksheet = self.get_google_sheet('USED_PROXY_LIST_FOR_' + self.args.website)
                    self.worksheet.update_cell(count, index_of_link + 1, proxy)
            count += 1
            self.driver.quit()


def main():
    clicker = Auto_Clicker()
    clicker.start()


if __name__ == "__main__":
    main()
    sys.exit(0)
