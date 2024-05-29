import csv


csvfile="dataAnalyst.csv"
with open(file=csvfile, mode='r') as file:
    reader = csv.reader(file)
    jobs = list(reader)
    for job in jobs:
        salary = job[4]
        print(salary)