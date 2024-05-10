from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd

opt = webdriver.ChromeOptions()
opt.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=opt)
driver.delete_all_cookies()

url = 'https://www.indeed.com/'
driver.get(url=url)



job_title = driver.find_element(By.NAME, value="q")
job_title.send_keys("Tech", Keys.ENTER)
time.sleep(0.5)
driver.get(url=driver.current_url)
location = driver.find_element(By.NAME, value="l")
location.send_keys(Keys.CONTROL + "a")
location.send_keys('New Jersey', Keys.ENTER)
time.sleep(0.5)


job_count = driver.find_element(By.CSS_SELECTOR, '.jobsearch-JobCountAndSortPane-jobCount span').text
job_count = job_count.replace(',','')
count = re.match('([0-9]*)', job_count)
number_of_job = int(count[0])
JOBS_PER_PAGE = 15
num_of_page = int(number_of_job/JOBS_PER_PAGE)

jobs = []

def get_list():
    results = driver.find_elements(By.CLASS_NAME, value='resultContent')
    for result in results:
        infos = []
        title = result.find_element(By.XPATH, ".//span").text     
        childs = result.find_elements(By.XPATH, ".//*")
        #specs = {}
        
        #specs['title'] = title
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
        #specs['info'] = infos
        #jobs.append(specs)
        jobs.append(infos)

get_list()

for i in range(10):
    pages = driver.find_elements(By.CSS_SELECTOR, 'nav ul li a')
    new_url = pages[-1].get_attribute('href')
    driver.get(url=new_url)
    time.sleep(2)
    get_list()
df = pd.DataFrame(jobs, columns=['jobTitle','company','location','salary','shift','workTime'])

df.to_csv('techJobs.csv')
    

