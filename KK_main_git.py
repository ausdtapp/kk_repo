import KK_v2 as kk_v2
import google_sheet_access as gs
import smtplib as sp
import csv
import os
import datetime

#Email set up
print('Email password?')
password = input()
mail = sp.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login("EMAIL HERE", password)

#Retrieves the information from the Google Sheet
API_KEY = 'API KEY HERE'
gs.create_google_api()



#Will retrieve previous CSVs for previous year and two years previous to compare to current matches  CONTINUE HERE
def read_csv(name):
    list = []
    with open(name, 'rt', newline='\n') as csvfile:
        prev_year_reader = csv.reader(csvfile, dialect='excel')
        for row in prev_year_reader:
            list.append(row)
    return list

#creates list of family members
#add kid KK stuff
def create_matches():
    unparsed_list = gs.retrieve_sheet_info(API_KEY)
    kid_kk_list = []
    kids = []
    family_list = []
    family = []
    family_number = 0
    for memb in unparsed_list:
        if not memb:
            family_list.append(family)
            family = []
            kid_kk_list.append(kids)
            kids = []
            family_number = family_number + 1
            continue
        if memb[0] and memb[3]:
            name = memb[0]
            email = memb[3]
            kid_num = memb[2]
            family.append(kk_v2.Fmemb(name, family_number, email, kid_num))
        if memb[1]:
            kid_name = memb[1]
            kids.append(kk_v2.kid(kid_name, family_number))
    family_list.append(family)
    kid_kk_list.append(kids)
    members = kk_v2.match_members(family_list)
    kk_v2.match_kids(members, kid_kk_list)
    return members


#Generic message for each kk member
def kk_message(row):
    if row[3]:
        message = 'hello ' + row[0] + ' your kk is ' + row[1] + ', and your kid KK(s) is ' + row[3]
    else:
        message = 'hello ' + row[0] + ' your kk is ' + row[1]
    return message


#sends pairs
def send_current_matches():
    current_matches = read_csv(str(datetime.datetime.now().year) + '_matches.csv')
    for i in current_matches:
        mail.sendmail('EMAIL HERE', i[2], kk_message(i)) #(email, reciever, message)
    mail.close()


#Use to check previous years' CSVs against your current match
def check_matches(matches):
    prev_year = str(datetime.datetime.now().year - 1) + '_matches.csv'
    sec_prev_year = str(datetime.datetime.now().year - 2) + '_matches.csv'
    last_year = read_csv('./previous_matches/' + prev_year)#csv from last year, csv kk_1_year.csv
    two_years_ago = read_csv('./previous_matches/' + sec_prev_year)#csv from two years ago, cwd kk_2_year.csv
    match_usable = True
    for a, b in matches.items():
        if match_usable is False:
            break
        for j in last_year:
            if [a.name, b.name] == [j[0], j[1]]:
                print(a.name + " has same match as last year")
                match_usable = False
                break
            elif len(j) == 4 and bool(set(a.kidKKs) & set(j[3].split(','))):
                print(a.name + ' has at least one similar kid last year')
                match_usable = False
                break
            else:
                continue
        for k in two_years_ago:
            if [a.name, b.name] == [k[0], k[1]]:
                print(a.name + " has same match as two years ago")
                match_usable = False
                break
            elif len(k) == 4 and bool(set(a.kidKKs) & set(k[3].split(','))):
                print(a.name + ' has at least one similar kid two years ago')
            else:
                continue
    if match_usable is False:
        print('current KK list not usable')
        return False
    else:
        print('current KK list usable')
        return True

#Use to write CSVs for of the current list of matches to compare to the others.
def save_current_match(dict):
    if check_matches:
        year = datetime.datetime.now().year
        filename = str(year) + '_matches.csv'
        new_csv = kk_v2.create_csv(dict)
        with open(filename, 'w', newline='\n') as new_file:
            csv_writer = csv.writer(new_file, dialect='excel')
            for i in new_csv:
                csv_writer.writerow(i)
    else:
        print('Did not pass check_matches')


#ONLY run when year is finished to prepare for running again next year
def conclude_year():
    current = str(datetime.datetime.now().year) + '_matches.csv'
    os.rename(current, './previous_matches/' + current)
