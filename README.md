# createWebform

GITHUB

1) Fork the repository
2) Upload the csv file with your questions in the DATA folder (see the questionnaire.csv file for an example of the format)
3) Edit the file createWebformDict.py by changing the name of the csv file and save the changes
4) Set the quest_type variable to "seed" of "target"
5) Click on the top-right (on your github user icon), and from the menu click on "Settings"
6) At the bottom of the left panel, click on "Developer settings"
7) On the left, click on "Personal access tokens"
8) Click on "Generate new token"
9) Give a name and copy your token
10) Select scope "Repo"


STREAMLIT

1) login with github account
2) Open the drop-down menu next to "New app"
3) Select "From existing repo"
4) Select the github repository for the webform
5) Click on "Advanced settings"
6) Select Python version 3.7
7) In the Secrets textbox write
   
   github_token = "insert_here_your_token"

8) Click on "Save"
9) Click on "Deploy"


You can share this link for the form:

https://share.streamlit.io/YOUR_GITHUB_PAGE/createwebform/main

