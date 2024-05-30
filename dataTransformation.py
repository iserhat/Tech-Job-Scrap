import csv
import re
from job import Job
import pandas as pd



role = []



# csvfile="dataAnalyst.csv"
# FILE = 'transformed_dataAnalyst.csv'
# jobTitle = 'Data Analsyt'

# csvfile="dataScientist.csv"
# FILE = 'transformed_dataScientist.csv'
# jobTitle = 'Data Scientist'

csvfile="developer.csv"
FILE = 'transformed_developer.csv'
jobTitle = 'Software Developer'


with open(file=csvfile, mode='r') as file:
    reader = csv.reader(file)
    jobs = list(reader)
    for job in jobs:
        salary = job[4]
        print(salary)
        salary = salary.replace(',','')
        fixed = re.findall('\d+', salary)
        print(fixed)
        control = len(fixed)
        minSalary = 0
        maxSalary = 0
        if control == 1:
            if int(fixed[0])>9000:
                minSalary = maxSalary = int(fixed[0])
        elif control == 2:
            if int(fixed[1])>int(fixed[0]):
                minSalary = int(fixed[0])
                maxSalary = int(fixed[1])
            else:
                minSalary = maxSalary = int(fixed[0])
        elif control == 4:
            minSalary = int(fixed[0])
            maxSalary = int(fixed[2])
        role.append([job[1], job[2], job[3], minSalary, maxSalary, jobTitle])

    
df = pd.DataFrame(role)
df.to_csv(FILE)