# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta

# URL of the web page to scrape
URL = "https://www.ctd.northwestern.edu/courses?grade_level=471,472,473,474&sort=alpha"
root = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(root.text, 'html.parser')

# Find the main container holding the course information
holders = soup.find('div', class_='ceResultsWrapper js-ceResultsWrapper')
container = holders.find_all('div', class_='ceCourse ceCourseWrapper js-ceCourse')

# Lists to store the scraped data
NW_Programs = []
grades = []

# Loop through each course component
for component in holders.find_all('div', {'class': 'ceCourse ceCourseWrapper js-ceCourse'}):
    # Extract the grade levels for the course
    grade_level = component.get('data-grade-levels')
    if '471' in grade_level or '472' in grade_level or '473' in grade_level or '474' in grade_level:
        
        # Extract course details
        name = component.find('h3', class_='ceCourse-title').text
        grade_temp = component.find('div', class_='ceCourse-gradeLevel').text
        grade = grade_temp[12:]
        grades.append(grade)

        location_temp = component.find('div', class_='ceCourse-meta u-hideWhenInCourseDetail').text
        state = ''
        city = ''
        if ',' in location_temp:
            state = location_temp[len(location_temp) - 2:]
            city = location_temp[:len(location_temp) - 4]
        else:
            state = "Remote"
            city = "Remote"

        time = component.find_all('div', class_='ceCourse-meta u-hideWhenInCourseDetail')[2].text
        char_loc = time.rfind('-')
        end_date = time[char_loc + 2:]
        start_date = time[:char_loc]

        # Format the dates
        start_original_date = datetime.strptime(start_date.strip(), "%B %d, %Y")
        start_formatted_date = start_original_date.strftime("%m/%d/%Y")
        end_original_date = datetime.strptime(end_date.strip(), "%B %d, %Y")
        end_formatted_date = end_original_date.strftime("%m/%d/%Y")

        # Extract course description
        course_des_temp = component.find('div', class_='ceCourse-description u-hideWhenInCourseTeaser')
        course_des_temp2 = course_des_temp.find_all('p')
        description = course_des_temp2[0].text + course_des_temp2[1].text

        # Extract credit information
        credit = ''
        credit_judge = ''
        for i in course_des_temp2:
            if i.text.startswith('HIGH'):
                credit_judge = i.text
                if any(char.isdigit() for char in credit_judge):
                    credit = "Yes"
                else:
                    credit = "No"
            if credit == '':
                credit = "No"

        # Extract eligibility requirements
        eligibility_temp = component.find('div', class_='ceCourse-accordionToggleArea')
        eligibility_temp2 = eligibility_temp.find('ul')
        eligibility = ''
        if eligibility_temp2 is not None:
            eligibility = eligibility_temp2.text
        else:
            eligibility = ''
        
        # Extract category
        category = component.find_all('div', class_='ceCourse-meta u-hideWhenInCourseDetail')[5].text

        # Extract fees
        fees = component.find_all('div', class_='ceCourse-tagValue')
        tuition = fees[3].text
        other_fee = ''
        if len(fees) >= 5:
            other_fee = fees[4].text
        if len(fees) >= 6:
            other_fee += ' ' + fees[5].text

        # Calculate application date
        original_date = datetime.strptime(start_date.strip(), "%B %d, %Y")
        new_date = original_date - timedelta(days=5)
        app_date = new_date.strftime("%m/%d/%Y")

        # Extract the course link
        idNum = component.get('data-direct-link-id')
        url = 'https://www.ctd.northwestern.edu/courses?grade_level=471,472,473,474&sort=alpha#' + idNum

        # Append the course details to the NW_Programs list
        NW_Programs.append(["Northwestern University", "Center for Talent Development", name, 
                            category, description, city, state, 
                            "", "United States", "No", "Yes", "Yes", "Yes", "No", "No", "Yes", 
                            "0", app_date, "0", other_fee, credit, tuition, start_formatted_date, 
                            end_formatted_date, eligibility, "9-12", url])
    
# Create a DataFrame to store the scraped data and save it to a CSV file
df = pd.DataFrame(NW_Programs, columns=["college", "program_name", "course_title", "program_category",
                                        "course_description", "city", "state", "zip_code", "country", "residential", 
                                        "application", "transcript", "letter_of_recommendation", "counselor_report",
                                        "test_scores", "toefl_or_english_exam", "app_fee", "app_date", 
                                        "enrollment_fee", "fees", "credit_offerred", "tuition", "start_date", 
                                        "end_date", "eligibility_requirements", "grades", "link"])
df.to_csv('NW_Programs_renewed.csv')
