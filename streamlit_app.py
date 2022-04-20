import pandas as pd
import streamlit as st
import os.path

from github import Github
from github import InputGitTreeElement
from datetime import datetime

input_dir = 'DATA' 
csv_file = 'questionnaire.csv'
# this can be 'seed' or 'target'
quest_type = 'seed'

pctls = [5,50,95]

def pushToGithub(df_new,input_dir,csv_file,quest_type):

    df2 = df_new.to_csv(sep=',', index=False)

    g = Github(st.secrets["github_token"])
    repo = g.get_user().get_repo('createWebform')

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Upload to github
    git_prefix = input_dir+'/'+ quest_type+'/'
    
    git_file = git_prefix +csv_file.replace('.csv','_')+dt_string+'_Output.csv'

    repo.create_file(git_file, "committing files", df2, branch="main")
    st.write(git_file + ' CREATED')
    
    return

def check_form(qst,ans,units,minVals,maxVals):

    n_qst = int((len(qst)-2)/3)
    
    check_flag = True

    for i in range(n_qst):
    
        idx = 2+i*3
        
        try:
            float(ans[idx])
        except ValueError:
            st.write('Non numeric answer')
            st.write(qst[idx],ans[idx])
            check_flag = False
            
        try:
            float(ans[idx+1])
        except ValueError:
            st.write('Non numeric answer')
            st.write(qst[idx+1],ans[idx+1])
            check_flag = False
            
        try:
            float(ans[idx+2])
        except ValueError:
            st.write('Non numeric answer')
            st.write(qst[idx+2],ans[idx+2])
            check_flag = False
            
        if check_flag:    
            
            if float(ans[idx]) >= float(ans[idx+1]):
        
                st.write('Error. '+qst[idx]+' >= '+qst[idx+1])            
                check_flag = False
            
            if float(ans[idx+1]) >= float(ans[idx+2]):
        
                st.write('Error. '+qst[idx+1]+' >= '+qst[idx+2])            
                check_flag = False
            
            if float(ans[idx])<= minVals[i] or float(ans[idx])>= maxVals[i]:
                
                st.write('Error. '+qst[idx]+':'+str(ans[idx]))
                st.write('The answer must be a value between '+str(minVals[i])+' and '+str(maxVals[i]))
                check_flag = False
            
            if float(ans[idx+1])<= minVals[i] or float(ans[idx+1])>= maxVals[i]:
                
                st.write('Error. '+qst[idx+1]+':'+str(ans[idx+1]))
                st.write('The answer must be a value between '+str(minVal)+' and '+str(maxVal))
                check_flag = False
            
            if float(ans[idx+2])<= minVals[i] or float(ans[idx+2])>= maxVals[i]:
                
                st.write('Error. '+qst[idx+2]+':'+str(ans[idx+2]))
                st.write('The answer must be a value between '+str(minVals[i])+' and '+str(maxVals[i]) )
                check_flag = False

    return check_flag       

def main():

    st.title("Elicitation form")
	
    df = pd.read_csv('./'+input_dir+'/'+csv_file,header=0)
    
    output_file = csv_file.replace('.csv','_NEW.csv')

    pctls = [5,50,95]

    form2 = st.form(key='form2')
    
    qst = ["First Name"]
    ans = []
    
    ans.append(form2.text_input(qst[-1]))
    
    qst.append("Last Name")
    ans.append(form2.text_input(qst[-1]))
    
    units = []
    minVals = []
    maxVals = []
    
    for i in df.itertuples():
    
        idx,shortQ,longQ,unit,scale,minVal,maxVal,realization,question = i[0:9]
        
        if ( question == quest_type):

            units.append(unit)
            
            if minVal.is_integer():
            
                minVal = int(minVal)
                    
            if maxVal.is_integer():
            
                maxVal = int(maxVal)

            minVals.append(minVal)
            maxVals.append(maxVal)
            
            # print(idx,qst,unit,scale)
            form2.header(shortQ)
            form2.markdown(longQ)
        
            j=0
            for pct in pctls:
                j+=1
            
                qst.append(shortQ+' - '+str(int(pct))+'% ('+str(minVal)+';'+str(maxVal)+')'+' ['+unit+']')
    
                ans.append(form2.text_input(qst[-1]))
            
    submit_button2 = form2.form_submit_button("Submit")
    
    if submit_button2:
    
        check_flag = check_form(qst,ans,units,minVals,maxVals)
        
        if check_flag:
    
            st.write('Thank you '+ans[0]+' '+ans[1] )
        
            zip_iterator = zip(qst,ans)
            data = dict(zip_iterator)
            df_new = pd.DataFrame([ans],columns=qst)
            
            pushToGithub(df_new,input_dir,csv_file,quest_type)
        
if __name__ == '__main__':
	main()            
