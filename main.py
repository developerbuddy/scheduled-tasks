# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


from datetime import datetime
import pandas
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

today = datetime.now()
today_tuple = (today.month, today.day)

birthdays_df = pandas.read_csv("birthdays.csv")
birthdays_dict = {}
for _, row in birthdays_df.iterrows():
    key = (row["month"], row["day"])
    if key not in birthdays_dict:
        birthdays_dict[key] = []
    birthdays_dict[key].append(row)
    
if today_tuple in birthdays_dict:
    birthday_people = birthdays_dict[today]
    for birthday_person in birthday_people:
        file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", birthday_person["name"])
    
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=birthday_person["email"],
                msg=f"Subject:Happy Birthday!\n\n{contents}"
            )
