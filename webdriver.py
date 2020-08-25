from selenium import webdriver
import os
import time 
import json

def login():
    driver.find_element_by_id('uname').send_keys("Enter registration number")
    driver.find_element_by_id('passwd').send_keys('Enter password')
    driver.find_element_by_tag_name('button').click()
    input('Enter the captcha and press enter here')
    
def coursepage():
    if driver.find_element_by_xpath('//*[@id="wrapper"]').get_attribute('class') != 'menuDisplayed':
        driver.find_element_by_id('menu-toggle').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="accordian0"]/div[4]/div[1]/h4/a').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="ACD0045"]').click()
    
    find_course = input('Enter the course code to search for: ') 
    right_sem = right_course = ''
    flag = 0
    
    for semester in driver.find_element_by_xpath('//*[@id="semesterSubId"]').find_elements_by_tag_name('option'):
        #print(semester.text)
        semester.click()
        time.sleep(0.2)
        #courses = [course for course in driver.find_element_by_xpath('//*[@id="courseCode"]').find_elements_by_tag_name('option')]
        for course in driver.find_element_by_xpath('//*[@id="courseCode"]').find_elements_by_tag_name('option'):
            #print(course.text)
            if find_course in course.text:
                right_course = course
                right_sem = semester
                flag = 1
                break
        if flag == 1:
            break
    right_sem.click()
    time.sleep(0.2)
    right_course.click()
    
    faculty_name = input("Enter the name of faculty: ")
    slot_input = input('Enter slot: ')
    rows = driver.find_elements_by_xpath('//*[@id="StudentCoursePage"]/div[5]/div/table/tbody/tr')
    for i in range(1, len(rows)):
        name = driver.find_element_by_xpath('//*[@id="StudentCoursePage"]/div[5]/div/table/tbody/tr[' + str(i) + ']/td[7]')
        slot = driver.find_element_by_xpath('//*[@id="StudentCoursePage"]/div[5]/div/table/tbody/tr[' + str(i) + ']/td[6]')
        if slot == slot_input and faculty_name == name:
            driver.find_element_by_xpath('//*[@id="StudentCoursePage"]/div[5]/div/table/tbody/tr[' + str(i) + ']/td[9]/button').click()
            time.sleep(0.2)
            break
    
    rows = driver.find_elements_by_xpath('//*[@id="CoursePageLectureDetail"]/div[3]/div[2]/div/table/tbody/tr')
    for i in range(1, len(rows)):
        p = driver.find_element_by_xpath('//*[@id="CoursePageLectureDetail"]/div[3]/div[2]/div/table/tbody/tr[' + str(i) + ']/td[5]')
        a = p.find_elements_by_tag_name('a')
        for materials in a:
            if 'Reference Material' in a.text:
                materials.click()
                
def newmarks():
    if driver.find_element_by_xpath('//*[@id="wrapper"]').get_attribute('class') != 'menuDisplayed':
        driver.find_element_by_id('menu-toggle').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="accordian0"]/div[6]/div[1]/h4/a').click()
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="EXM0011"]').click()
    marks = {}
    time.sleep(0.2)
    semesters = [semester for semester in driver.find_element_by_xpath('//*[@id="semesterSubId"]').find_elements_by_tag_name('option')]
    for sem_no in range(1, len(semesters) + 1):
        driver.find_element_by_xpath('//*[@id="semesterSubId"]/option[' + str(sem_no) + ']').click()
        time.sleep(1)
        #print(driver.find_element_by_xpath('//*[@id="semesterSubId"]/option[' + str(sem_no) + ']').text)
        #print(driver.find_element_by_xpath('//*[@id="studentMarkView"]/div/div/span[2]').text)
        if driver.find_element_by_xpath('//*[@id="studentMarkView"]/div/div/span[2]').text != 'No data Found':
            time.sleep(0.2)
            exam = mark = subject = ''
            rows = driver.find_elements_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr')
            #print(len(rows))
            for i in range(1, len(rows)):
                #print(driver.find_element_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td').get_attribute('colspan'))
                if driver.find_element_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td').get_attribute('colspan') == '9':
                    for mark_row in range(2, len(driver.find_elements_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td/table/tbody/tr')) + 1):
                        exam = driver.find_element_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td/table/tbody/tr[' + str(mark_row) + ']/td[2]/output')
                        mark = driver.find_element_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td/table/tbody/tr[' + str(mark_row) + ']/td[6]/output')
                        marks[subject].append([exam.text,mark.text])
                        #print("\t" + str((exam.text, mark.text)))
                else:
                    subject = driver.find_element_by_xpath('//*[@id="fixedTableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td[3]').text
                    #print(subject)
                    marks[subject] = []
            #print(str(marks))
    with open('marks.json', 'w+') as mark_file:
        if os.stat('marks.json').st_size != 0:
            flag = 0
            details = json.load(mark_file)
            for subject in marks:
                if marks[subject] != details.get(subject, " "):
                    for mark_list in marks[subject]:
                        if mark_list not in details[subject]:
                            print(subject + '\t' + mark_list[0] + ":" + mark_list[1])
                            details[subject].append(mark_list)
                            flag = 1
            if flag == 0:
                print('No change in marks')
            else:
                json.dump(details, mark_file, indent = 4)
        else:
            for subject, mark_list in marks.items():
                print(subject)
                for mark in mark_list:
                    print('\t' + mark[0] + ' : ' + mark[1])
            json.dump(marks, mark_file, indent = 4)

    
def attendance():
    if driver.find_element_by_xpath('//*[@id="wrapper"]').get_attribute('class') != 'menuDisplayed':
        driver.find_element_by_id('menu-toggle').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="accordian0"]/div[4]/div[1]/h4/a').click()
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="ACD0042"]').click()
    time.sleep(0.2)
    sem_name = input('Enter the semester name: ')
    for semester in driver.find_elements_by_tag_name('option'):
        if sem_name.lower() in semester.text.lower():
            semester.click()
            driver.find_element_by_xpath('//*[@id="viewStudentAttendance"]/div[2]/div/button').click()
            time.sleep(0.2)
            for row_no in range(1, len(driver.find_elements_by_xpath('//*[@id="getStudentDetails"]/div/table/tbody/tr'))):
                cols = driver.find_elements_by_xpath('//*[@id="getStudentDetails"]/div/table/tbody/tr[' + str(row_no) + ']/td')
                subject = cols[1].text + "-" + cols[2].text + "-" + cols[3].text
                percent = cols[11].text
                print(subject + ' : ' + percent)
            break
                
                
driver = webdriver.Chrome(os.getcwd() + '/chromedriver')

driver.get('https://vtop.vit.ac.in')
driver.find_element_by_tag_name('button').click()
time.sleep(2)
login()
while True:
    print('Enter 1 to download materials')
    print('Enter 2 to sync the dates')
    print('Enter 3 to check if new marks have come')
    print('Enter 4 to check your attendance')
    print('Enter 5 to quit')
    choice = input('Enter your choice: ')
    if choice == '1':
        coursepage()
        driver.refresh()
    elif choice == '3':
        newmarks()
        driver.refresh()
    elif choice == '4':
        attendance()
        driver.refresh()
    elif choice == '5':
        driver.close()
        break