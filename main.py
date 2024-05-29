from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
from job import Job


job = Job("Analsyt", "New Jersey", "dataAnalyst.csv")
JOB_ROLE = job.role
STATE = job.state
FILE = job.file
JOBS_PER_PAGE = 15

opt = webdriver.ChromeOptions()
opt.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=opt)
driver.delete_all_cookies()

#Getting the indeed index page and searching specified job and location
url = 'https://www.indeed.com/'
driver.get(url=url)
job_title = driver.find_element(By.NAME, value="q")
job_title.send_keys(JOB_ROLE, Keys.ENTER)
time.sleep(0.5)
driver.get(url=driver.current_url)
location = driver.find_element(By.NAME, value="l")
location.send_keys(Keys.CONTROL + "a")
location.send_keys(STATE, Keys.ENTER)
time.sleep(0.5)

#Calculating the number of pages for specified job and location
#The num_of_page can be used for getting all search results
job_count = driver.find_element(By.CSS_SELECTOR, '.jobsearch-JobCountAndSortPane-jobCount span').text
job_count = job_count.replace(',','')
count = re.match('([0-9]*)', job_count)
number_of_job = int(count[0])
num_of_page = int(number_of_job/JOBS_PER_PAGE)
jobs = []

def get_list():
    results = driver.find_elements(By.CLASS_NAME, value='resultContent')
    for result in results:
        infos = []
        title = result.find_element(By.XPATH, ".//span").text     
        childs = result.find_elements(By.XPATH, ".//*")
        infos.append(title)
        for child in childs:
            name = child.get_attribute('data-testid')
            if name == 'company-name':
                #specs['company_name'] = child.text
                infos.append(child.text)
            elif name == 'text-location':
                #specs['location'] = child.text
                infos.append(child.text)
            elif name == 'attribute_snippet_testid':
                infos.append(child.text)
            else:
                continue
        jobs.append(infos)

get_list()


# the range of the "for loop" choosed as 5 for testing purpose. num_of_page can be used for getting all search results 
for i in range(8):
    pages = driver.find_elements(By.CSS_SELECTOR, 'nav ul li a')
    new_url = pages[-1].get_attribute('href')
    driver.get(url=new_url)
    time.sleep(2)
    get_list()

df = pd.DataFrame(jobs)
df.to_csv(FILE)
    


