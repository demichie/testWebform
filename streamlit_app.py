import pandas as pd
import streamlit as st
import os.path

from github import Github
from github import InputGitTreeElement
from datetime import datetime

csv_file = 'SEED.csv'

def pushToGithub(df_new,csv_file):

    df2 = df_new.to_csv(sep=',', index=False)

    g = Github(github_token)
    repo = g.get_user().get_repo('createWebform')

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Upload to github
    git_prefix = 'DATA/'
    git_file = git_prefix +csv_file.replace('.csv','_')+dt_string+'_Output.csv'

    repo.create_file(git_file, "committing files", df2, branch="main")
    st.write(git_file + ' CREATED')
    
    return

def check_form(qst,ans,units):

    n_qst = int((len(qst)-2)/3)
    
    check_flag = True

    for i in range(n_qst):
    
        idx = 2+i*3
    
        if not ans[idx].isdecimal():
        
            st.write('Non numeric answer')
            st.write(qst[idx],ans[idx])
            check_flag = False
            
        if not ans[idx+1].isdecimal():
        
            st.write('Non numeric answer')
            st.write(qst[idx+1],ans[idx+1])
            check_flag = False
            
        if not ans[idx+2].isdecimal():
        
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
            
            if units[i] == '%':
            
                if float(ans[idx])<= 0.0 or float(ans[idx])>= 100.0:
                
                    st.write('Error. '+qst[idx])
                    st.write('The answer must be a percentage value (0<x<100)')
                    check_flag = False
            
                if float(ans[idx+1])<= 0.0 or float(ans[idx+1])>= 100.0:
                
                    st.write('Error. '+qst[idx+1])
                    st.write('The answer must be a percentage value (0<x<100)')
                    check_flag = False
            
                if float(ans[idx+2])<= 0.0 or float(ans[idx+2])>= 100.0:
                
                    st.write('Error. '+qst[idx+2])
                    st.write('The answer must be a percentage value (0<x<100)')
                    check_flag = False

    return check_flag       

def main():

    st.title("Elicitation form")
	
    df = pd.read_csv(csv_file,header=0)
    
    output_file = csv_file.replace('.csv','_NEW.csv')

    pctls = [5,50,95]

    form2 = st.form(key='form2')
    
    qst = ["First Name"]
    ans = []
    
    ans.append(form2.text_input(qst[-1]))
    
    qst.append("Last Name")
    ans.append(form2.text_input(qst[-1]))
    
    units = []
    for i in df.itertuples():
        idx,shortQ,longQ,unit,scale = i
        units.append(unit)
        # print(idx,qst,unit,scale)
        form2.header(shortQ)
        form2.markdown(longQ)
        j=0
        for pct in pctls:
            j+=1
            
            qst.append(shortQ+' - '+str(int(pct))+'% ['+unit+']')
    
            ans.append(form2.text_input(qst[-1]))
            
    submit_button2 = form2.form_submit_button("Submit")
    
    if submit_button2:
    
        check_flag = check_form(qst,ans,units)
        
        if check_flag:
    
            st.write('Thank you '+ans[0]+' '+ans[1] )
        
            zip_iterator = zip(qst,ans)
            data = dict(zip_iterator)
            df_new = pd.DataFrame([ans],columns=qst)
            
            pushToGithub(df_new,csv_file)
        
if __name__ == '__main__':
	main()            
