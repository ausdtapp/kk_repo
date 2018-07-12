import KK_v2 as kk
import google_sheet_access as gs
import smtplib as sp

#Generic message for each kk member
def kk_message(member, match):
    message = 'hello ' + member + ' your kk is ' + match
    return message

#Email set up
print('Email password?')
password = input()
mail = sp.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
#Insert email here
mail.login('placeholder@gmail.com', password)

#Retrieves the information from the Google Sheet
#
API_KEY = 'api key here'
gs.create_google_api()
unparsed_list = gs.retrieve_sheet_info(API_KEY)

#creates list of family members
family_list = []
family = []
family_number = 0
for memb in unparsed_list:
    if not memb:
        family_list.append(family)
        family = []
        family_number = family_number + 1
        continue
    name = memb[0]
    email = memb[2]
    family.append(kk.Fmemb(name, family_number, email))
family_list.append(family)

pairs_dictionary = kk.match_members(family_list)

for i,j in pairs_dictionary.items():
    #(email, reciever, message)
    mail.sendmail('placeholder@gmail.com', i.email, kk_message(i.name, j.name))
mail.close()

