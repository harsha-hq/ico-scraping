# -*- coding: utf-8 -*-
import os
from links import *
from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import copy
import time
import datetime
import pandas as pd
#os.getcwd() #get current working directory
# Change current working directory if it is different from above
#os.chdir('C:/Users/hvvel/OneDrive/Documents/RA')
#os.getcwd()

today = date.today()
today = today.strftime("%m/%d/%y")

start = time.time()
DESCRIPTION_HEADER = ['Company_Key','Company', 'Short_Desc', 'Long_Desc', 'Categories','Date']
DESCRIPTION_DF = pd.DataFrame(columns=DESCRIPTION_HEADER)
#DESCRIPTION
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS = SOUP.find_all(class_='ico_information')
    for post in POSTS:
        name = post.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
        shrt_desc = post.find('h2')
        shrt_desc = shrt_desc.get_text()
        shrt_desc = shrt_desc.replace("\n","").replace(",","")
        #print(shrt_desc)
        long_desc = post.find('p')
        long_desc = long_desc.get_text()
        long_desc = long_desc.replace("\n","").replace(",","")
        #print(long_desc)
        categories = post.find(class_='categories')
        tags = []
        for tag in categories:
            tags.append(tag.get_text())
        DESCRIPTION_DF = DESCRIPTION_DF.append({'Company_Key':company_key,
                                                'Company': company_name,
                                                'Short_Desc':  shrt_desc,
                                                'Long_Desc': long_desc,
                                                'Categories': tags,
                                                'Date':today}, ignore_index=True)
DESCRIPTION_DF.to_csv("company_overview.csv", index=False)

#RATINGS

RATINGS_HEADER = ['Company_Key','Company', 'Expert_Rating', 'Expert_Count', 'Benchy_Rating',
                  'Expert_Team_Rating', 'Expert_Vision_Rating', 'Expert_Product_Rating',
                  'KYC_class','Date']
RATINGS_DF = pd.DataFrame(columns=RATINGS_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find_all(class_='rating')
    for post in POSTS:
        #print(post)
        #print(company_name)
        expert_rating_col_name = post.find('a', class_='view_rating')
        if expert_rating_col_name is not None:
            expert_rating_col_name = expert_rating_col_name.find('div')['class']
           #expert_rating_col_name = post.find('a', class_='view_rating').find('div')['class']
            class_name = expert_rating_col_name[0]+" "+expert_rating_col_name[1]
            if class_name == 'rate color4':
                expert_rating = post.find('div', class_='rate color4')
                expert_rating = expert_rating.get_text()
            else:
                expert_rating = post.find('div', class_='rate color5')
                if expert_rating is not None:
                    expert_rating = expert_rating.get_text()
            #expert_rating = float(expert_rating)
            #print(expert_rating)
            expert_count = post.find('small').get_text()
            expert_count = expert_count[:1]
            #print(expert_count[:1])
            ratings = post.find('div', class_='distribution').findChildren(recursive=False)
            #benchy rating
            benchy_rating = ratings[0].find('span', class_='label_top notranslate').next_sibling.string.strip()
            #print(benchy_rating)
            #Experts Ratings
            expert_ratings_list = ratings[1].find('div', class_='columns').findChildren(class_='col_4 col_3')
            expert_team_rating = expert_ratings_list[0].find(text=True, recursive=False).strip()
            expert_vision_rating = expert_ratings_list[1].find(text=True, recursive=False).strip()
            expert_product_rating = expert_ratings_list[2].find(text=True, recursive=False).strip()
            #expert_team_rating = expert_team_rating.replace("-","")
            #expert_vision_rating = expert_vision_rating.replace("-","")
            #expert_product_rating = expert_product_rating.replace("-","")
            #expert_team_rating = float(expert_team_rating)
            #expert_vision_rating = float(expert_vision_rating)
            #expert_product_rating = float(expert_product_rating)
            #print(expert_team_rating)
            #print(expert_vision_rating)
            #print(expert_product_rating)
            #KYC Information
            kyc_class = post.find('a', class_='view_kyc').find('i')['class'][0]
            #print(kyc_class)
            RATINGS_DF = RATINGS_DF.append({'Company_Key':company_key,
                                            'Company': company_name,
                                            'Expert_Rating':  expert_rating,
                                            'Expert_Count': expert_count,
                                            'Benchy_Rating': benchy_rating,
                                            'Expert_Team_Rating':expert_team_rating,
                                            'Expert_Vision_Rating': expert_vision_rating,
                                            'Expert_Product_Rating': expert_product_rating,
                                            'KYC_class': kyc_class,
                                            'Date':today}, ignore_index=True)
RATINGS_DF.to_csv("company_ratings.csv", index=False,encoding='utf-8-sig')


#FINANCIAL DATA
HEADER = []
LISTDICT = []
fin_data = {}
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find_all(class_='financial_data')
    #for post in POSTS:
    for post in POSTS:
        status_col_name = post.find('div', class_='row').find('div')['class']
        if len(status_col_name) > 1:
            status_col_name = status_col_name[0]+" "+status_col_name[1]
        else:
            status_col_name = status_col_name[0]
        if status_col_name == 'col_2 expand':
            statuses = post.findAll('div', class_='col_2 expand')
            #print(statuses)
            PreICO_Time = statuses[0].find('div', class_='number')
            if PreICO_Time is not None:
                PreICO_Time = PreICO_Time.get_text()
                #print(PreICO_Time)
                fin_data['PreICO_Time'] = PreICO_Time
            PreICO_Period = statuses[0].find('small')
            if PreICO_Period is not None:
                PreICO_Period = PreICO_Period.get_text()
                fin_data['PreICO_Period'] = PreICO_Period
                #print(PreICO_Period)
            if len(statuses) > 1:
                ICO_Time = statuses[1].find('div', class_='number')
                if ICO_Time is not None:
                    ICO_Time = ICO_Time.get_text()
                    fin_data['ICO_Time'] = ICO_Time
                    #print(ICO_Time)
                ICO_Period = statuses[1].find('small')
                if ICO_Period is not None:
                    ICO_Period = ICO_Period.get_text()
                    fin_data['ICO_Period'] = ICO_Period
                    #print(ICO_Period)
        else:
            statuses = post.find('div', class_='row', recursive=False)
            #print(statuses)
            status = statuses.find('div', class_='number').get_text()
            #print(status)
    financial_data = post.find_all('div', class_='data_row')
    for data in financial_data:
        tokens = data.findChildren()
        key = tokens[0].get_text().strip()
        value = tokens[1].get_text().strip().replace("\n","").replace(",","")
        fin_data[key] = value
    fin_data['Company'] = company_name
    fin_data['Company_Key'] = company_key
    fin_data['Date'] = today
    LISTDICT.append(fin_data)
    #fin_data = copy.deepcopy(fin_data)
    if len(HEADER) > 0:
        HEADER = list(set(HEADER+list(fin_data.keys())))
    else:
        HEADER = list(fin_data.keys())
    fin_data = {}
    COMPANY_OVERVIEW_DF = pd.DataFrame(columns=HEADER)
    for dictItem in LISTDICT:
       COMPANY_OVERVIEW_DF = COMPANY_OVERVIEW_DF.append(dictItem, ignore_index=True)
COMPANY_OVERVIEW_DF.to_csv("company_financials.csv", index=False,encoding='utf-8-sig')

#ABOUT

ABOUT_HEADER = ['Company_Key','Company', 'About','Date']
ABOUT_DF = pd.DataFrame(columns=ABOUT_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        print(company_name)
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
    POSTS = SOUP.find(class_='tab_content', id="about")
    if POSTS is not None:
        about = POSTS.get_text().strip()
        about = about.replace("\n","").replace(",","")
    #print(POSTS.get_text())
    ABOUT_DF = ABOUT_DF.append({'Company_Key':company_key,
                                'Company': company_name,
                                'About': about,
                                'Date':today}, ignore_index=True)
ABOUT_DF.to_csv("about_company.csv", index=False,encoding='utf-8-sig')


#TEAM

TEAM_HEADER = ['Company_Key','Company', 'Member_Name', 'Member_Role', 'Member_Country',
               'Member_Social_Media', 'Scoial_Media_Link','Date']
TEAM_DF = pd.DataFrame(columns=TEAM_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find(class_='tab_content', id="team")
    if POSTS is not None:
        team_details = POSTS.find_all('div', class_='col_3')
        if team_details is not None:
            for every in team_details:
                #print(every)
                if every is not None:
                    name = every.find('h3', class_="notranslate").get_text()
                #print(name)
                role = every.find('h4', class_="notranslate")
                if role is not None:
                    role = role.get_text()
                #print(role)
                country = every.find('div', class_='country')
                if country is not None:
                     memeber_country = every.find('div', class_='country').find('span')['data-badge-top']
                else:
                    memeber_country = ""
                #print(memeber_country)
                social = every.find('div', class_='socials')
                if social is not None:
                    social_media = social.get_text()
                    #print(social_media)
                    profile_link = social.find('a')['href']
                else:
                    social_media = ""
                    #print(social_media)
                    profile_link = ""
                TEAM_DF = TEAM_DF.append({'Company_Key':company_key,
                                          'Company': company_name,
                                          'Member_Name': name,
                                          'Member_Role': role,
                                          'Member_Country' : memeber_country,
                                          'Member_Social_Media' : social_media,
                                          'Scoial_Media_Link' : profile_link,
                                          'Date':today}, ignore_index=True)
TEAM_DF.to_csv("company_team.csv", index=False,encoding='utf-8-sig')
   
#MILESTONES

MILESTONE_HEADER = ['Company_Key','Company', 'Number', 'Quarter', 'Milestone_Desc','Date']
MILESTONE_DF = pd.DataFrame(columns=MILESTONE_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find(class_='tab_content', id="milestones")
    if POSTS is not None:
        milestones = POSTS.find('div', class_='box')
    for every in milestones.findChildren(recursive=False):
        #print(every)
        number = every.find('div', class_="number").get_text()
        #print(number)
        quarter = every.find('div', class_="condition").get_text()
        #print(quarter)
        milestone_desc = every.find('p').get_text()
        milestone_desc = milestone_desc.replace("\n"," ").replace(","," ").replace("=","")
        #print(milestone_desc)
        MILESTONE_DF = MILESTONE_DF.append({'Company_Key':company_key,
                                            'Company': company_name,
                                            'Number': number,
                                            'Quarter': quarter,
                                            'Milestone_Desc' : milestone_desc,
                                            'Date':today}, ignore_index=True)
MILESTONE_DF.to_csv("company_milestone.csv", index=False,encoding='utf-8-sig')  

  
#FINANCIAL_Detailed
DETAIL_FINANCIALS_HEADER = []
FINAN_DICT = []
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find(class_='tab_content', id="financial")
    if POSTS is not None:
        financials = POSTS.find('div', class_='box')
    box_left = {}
    for_box_left = financials.find('div', class_='box_left')
    #print(for_box_left)
    #print('-----------')
    for token in for_box_left.findChildren('div', class_='row'):
        key = token.find('div', class_='label')
        if key is not None:
            key = key.get_text()
            value = token.find('div', class_='value').get_text()
        #print(key,':',value)
            box_left[key] = value
        bonus = token.find('div', class_="bonus_text")
        if bonus is not None:
            bonus = bonus.get_text().replace('\n\n', " ")
            #print(bonus)
            box_left['Bonus'] = bonus
    #print(box_left)
    #right box
    for_box_right = financials.find('div', class_='box_right')
    #print(for_box_left)
    #print('-----------')
    if for_box_right is not None:
        for token in for_box_right.findChildren('div', class_='row'):
            key = token.find('div', class_='label')
            if key is not  None:
                key = key.get_text().strip()
                value = token.find('div', class_='value').get_text().strip().replace("\n","").replace(",","")
                box_left[key] = value
    #print(box_left)
    finan_detail_data = {}
    box_left['Company'] = company_name
    box_left['Company_Key'] = company_key
    box_left['Date'] = today
    FINAN_DICT.append(box_left)
    if len(DETAIL_FINANCIALS_HEADER) > 0:
        DETAIL_FINANCIALS_HEADER = list(set(DETAIL_FINANCIALS_HEADER+list(box_left.keys())))
    else:
        DETAIL_FINANCIALS_HEADER = list(box_left.keys())
COMPANY_DEATIL_FINANCIAL_DF = pd.DataFrame(columns=DETAIL_FINANCIALS_HEADER)
for dictItem in FINAN_DICT:
    COMPANY_DEATIL_FINANCIAL_DF = COMPANY_DEATIL_FINANCIAL_DF.append(dictItem, ignore_index=True)
COMPANY_DEATIL_FINANCIAL_DF.to_csv("Company_Detail_Financial.csv", index=False,encoding='utf-8-sig')

   
#KYC Information

KYC_HEADER = ['Company_Key','Company', 'Member','Member_Approval','Date']
KYC_DF = pd.DataFrame(columns=KYC_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find(class_="kyc_information")
    #print(POSTS)
    if POSTS is not None:
        members = POSTS.find('div', class_='subtitle')
        invites = POSTS.find('div', class_='kyc_report')
    members_invited = members.get_text()
    members_invited = members_invited[0]
    invite_status = {}
    if invites is not None:
        for invite in invites.findChildren('div', class_='row'):
            #print(invite)
            report_member = invite.find('div', class_='col_1_2 notranslate').get_text().strip()
            report_status = invite.find('div', class_='col_2_2').get_text().strip()
            invite_status[report_member] = report_status
        #print(invite_status)
            KYC_DF = KYC_DF.append({'Company_Key':company_key,
                                    'Company': company_name,
                                    'Member': report_member,
                                    'Member_Approval': report_status,
                                    'Date':today}, ignore_index=True)
KYC_DF.to_csv("company_KYC.csv", index=False,encoding='utf-8-sig')
   
#Ratings
USER_RATING_HEADER = ['Company_Key','Company', 'Reviewer_Name', 'Reviewer_Role', 'Review_Date',
                      'Review_Modified_Date', 'Reviewer_Rating_Team', 
                      'Reviewer_Rating_Vision', 'Reviewer_Rating_Product',
                      'Reviewer_Rating_Weightage', 'Review','Reply_for_review','Replied_by',
                      'Replied_on','Date']
USER_RATING_DF = pd.DataFrame(columns=USER_RATING_HEADER)
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    POSTS_Name = SOUP.find_all(class_='ico_information')
    for post_name in POSTS_Name:
        name = post_name.find('h1', class_='notranslate')
        company_name = name.get_text()
        company_key = re.sub('[^A-Za-z0-9]+', '', company_name)
        company_key = company_key.lower()
        print(company_name)
    POSTS = SOUP.find(class_='tab_content', id="ratings")
    if POSTS is not None:
        ratings = POSTS.find('div', class_='ratings_list')
    for review in ratings.findChildren('div', class_='row'):
        #print(review)
        reviewer_name = review.find('div', class_='data').find('a').get_text()
        #print(reviewer_name)
        reviewer_title = review.find('div', class_='title')
        role_date = reviewer_title.find_all(text=True)
        role = role_date[0]
        role = role.replace("\n"," ").replace(","," ")
        review_date = role_date[1] if len(role_date) >= 2 else 'None'
        if "Rated on" in review_date:
            review_date = review_date.replace("Rated on","").replace("None","")
            #review_date = review_date.replace("None","")
            review_date = datetime.datetime.strptime(review_date[1:],'%b %d, %Y').strftime('%m/%d/%Y')
            #print(review_date) 
        modified_date = role_date[2] if len(role_date) == 3 else 'None'
        if "Modified on" in modified_date:
            modified_date = modified_date.replace("Modified on","").replace("None","")
            #modified_date = modified_date.replace("None","")
            modified_date = datetime.datetime.strptime(modified_date[1:],'%b %d, %Y').strftime('%m/%d/%Y')
            #print(modified_date)  
        reviewer_rating = review.find('div', class_='rate')
        #print(reviewer_rating)
        #for rating in reviewer_rating.find_all(text = True):#'div', class_='col_3'):
            #print(rating)
        if reviewer_name != "Benchy":
            rating = reviewer_rating.findChildren(recursive=False)
            #print(rating)
            team = rating[0].find(text=True, recursive=False)
            #print(team)
            vision = rating[1].find(text=True, recursive=False)
            #print(vision)
            product = rating[2].find(text=True, recursive=False)
        if reviewer_name == "Benchy":
            team = None
            vision = None
            product = None
        weightage = review.find('div', class_='distribution')
        for weights in weightage:
            #print(weights)
            review_weightage = weightage.get_text().strip()
            review_weightage = review_weightage.replace("weight", "")
            #print(review_weightage)
        review_write = review.find('div', class_='review')
        #print(review_write)
        if review_write is not None:
            for reviews in review_write.findChildren('p'):
                review_written = reviews.get_text().replace('\n', "").replace(",","")
        else:
            review_written = ""
        #owners_reply    
        review_reply = review.find('div', class_='owners_reply')
        if review_reply is not None:
            replied_by = review_reply.find('div',class_='title').get_text()
            ico_index = replied_by.find("ICO")
            replied_by_name = replied_by[0:ico_index]
            reply_on = replied_by.find("replied")   
            reply_date = replied_by[reply_on+11:]
            review_reply = review_reply.find('div',class_='reply_message').get_text()
        else: 
            replied_by_name = ''
            review_reply = ''   
            reply_date = ''
        #em tag doesn't show up
        #counts = ratings.find('div',class_='agree_count plus')
        #print(counts.get_text())
        USER_RATING_DF = USER_RATING_DF.append({'Company_Key':company_key,
                                                'Company' : company_name,
                                                'Reviewer_Name' : reviewer_name,
                                                'Reviewer_Role' : role,
                                                'Review_Date' : review_date,
                                                'Review_Modified_Date' : modified_date,
                                                'Reviewer_Rating_Team' : team,
                                                'Reviewer_Rating_Vision' : vision,
                                                'Reviewer_Rating_Product' : product,
                                                'Reviewer_Rating_Weightage' : review_weightage,
                                                'Review' : review_written,
                                                'Reply_for_review':review_reply,
                                                'Replied_by':replied_by_name,
                                                'Replied_on':reply_date,                                                             
                                                'Date':today}, ignore_index=True)
USER_RATING_DF.to_csv("reviews_by_users.csv", index=False,encoding='utf-8-sig')