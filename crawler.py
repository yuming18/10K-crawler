from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import json
import logging


def crawl(params, cik):
    """
    Crawl the 10-K reports of each company.

    Arguments:
    params -- input arguments, including: sec url and file type of target reports
    cik -- cik index for the company

    Returns:
    company_dict -- python dict of crawling result. Including: company_name and reports' url.
    """
    
    # options prevent crawler opening the website, 
    # which is faster for crawler.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(params.url)

    driver.find_element_by_id("cik").click()
    driver.find_element_by_id("cik").clear()
    driver.find_element_by_id("cik").send_keys(cik)
    driver.find_element_by_id("cik_find").click()
    driver.refresh()
    driver.find_element_by_id("type").click()
    driver.find_element_by_id("type").clear()
    driver.find_element_by_id("type").send_keys(params.file_type)
    driver.find_element_by_xpath("//input[@value='Search']").click()
    driver.refresh()

    rows = driver.find_elements_by_xpath('//*[@id="seriesDiv"]/table/tbody//tr')

    company_dict = dict()
    report_list = list()

    company_name = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/span').text

    company_dict["company_name"] = company_name

    logging.info("I am crawling {}({}). Please wait...".format(company_name, cik))

    if len(rows) == 1:
        logging.info("{}({}) has no 10-K report.".format(company_name, cik))
    else:
        for i in range(len(rows) - 1):

            try:
                report_dict = dict()
                driver.refresh()
                cols = driver.find_elements_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[{}]/td'.format(i+2))

                file_type = cols[0].text
                document_button = cols[1]
                date = cols[3].text

                if file_type == "10-K":
                    document_button.find_element_by_id("documentsbutton").click()
                    driver.refresh()
                    target = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a').click()
                    driver.refresh()
                    target_url = driver.current_url

                    driver.refresh()
                    driver.back()
                    driver.refresh()
                    driver.back()

                    report_dict["file_type"] = file_type
                    report_dict["date"] = date
                    report_dict["url"] = target_url
                    report_list.append(report_dict)
            except:
                pass
        logging.info("{}({}) is done.".format(company_name, cik))

    driver.close()
    driver.quit()

    company_dict["report"] = report_list

    return company_dict

def crawl_all(params, cik_list, save_dir):
    """
    Crawl all the 10-K report of every companies from cik list

    Arguments:
    params -- input arguments, including: sec url and file type of target reports
    cik_list -- list of all companies' cik index
    save_dir -- dir to save result files
    """

    logger = logging.getLogger()
    logging.info("----- Start crawling -----")

    for cik in cik_list:
        company_dict = crawl(params, cik)
        with open(save_dir + cik + ".json", "w") as out:
            json.dump(company_dict, out, sort_keys = True, indent = 4)

    logging.info("----- Crawling over -----")
