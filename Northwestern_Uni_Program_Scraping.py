from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://www.ctd.northwestern.edu/grade-9-grade-12-online"
root = requests.get(URL, headers = {'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(root.text, 'html.parser')
urls = []
container = soup.find('div', attrs = {'class', 'field field--name-field-cards field--type-entity-reference-revisions field--label-hidden field__items'})
for link in container.find_all('a'):
    l1= link.get('href')
    l2 = "https://www.ctd.northwestern.edu"
    l3 = l2 + l1
    urls.append(l3)

NW_Program = []
names = []
descriptions = []
tuitions = []
dates = []
eligibility = []
tuitions = []



for url in urls[0:]:
    each_program = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    program_soup = BeautifulSoup(each_program.text, 'html.parser')
    program_name = program_soup.find('h1').text
    names.append(program_name)

    program_summary = program_soup.find('div', {'class', 'field field--name-field-top-overview-content field--type-text-long field--label-hidden field__item'})
    program_summary_description = program_summary.select('p')
    program_description = program_summary_description[0].text + " " + program_summary_description[1].text
    descriptions.append(program_description)

    program_eli = program_soup.find('div', {'class', 'field field--name-field-accordion-body field--type-text-long field--label-hidden field__item'})
    program_eli2 = program_eli.select('p')
    program_eligibility = ""
    for i in program_eli2:
        program_eligibility += i.text + " "
    eligibility.append(program_eligibility)

    program_des =  program_soup.find('div', {'class', 'field field--name-field-program-detail-hero-widget field--type-entity-reference-revisions field--label-hidden field--item-count-4 field__items'})
    program_des2 = program_des.select('p')
    program_tuition_credit1 = program_des2[7].text
    program_tuition_credit2 = program_des2[8].text
    program_tuition = program_tuition_credit1 + program_tuition_credit2
    tuitions.append(program_tuition)
    

    program_date = program_des2[5].text
    program_start_date = program_des2[6].text

    NW_Program.append(["Northwestern University", "Grade 9 - Grade 12 Online", program_name, 
                    "Arts & Social Science", program_description, "Remote", "Remote", 
                    "000", "United States", "No", "Yes", "Yes", "Yes", "No", "No", "Yes", 
                    "0", program_start_date, "0", "Yes", program_tuition, program_start_date, program_eligibility, "9-12", url ])
    

df = pd.DataFrame(NW_Program, columns=["college", "program_name", "course_title", "program_category",
                                        "course_description", "city", "state", "zip_code", "country", "residential", 
                                        "application", "transcript", "letter_of_recommendation", "counselor_report",
                                        "test_scores", "toefl_or_english_exam", "app_fee", "app_date", 
                                        "enrollment_fee", "credit_offerred", "tuition", "start_date", "eligibility_requirements",
                                        "grades", "link"])
df.to_csv('NW_Programs.csv')