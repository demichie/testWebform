import pandas as pd
import streamlit as st
import os.path

from github import Github
from github import InputGitTreeElement
from datetime import datetime

from createWebformDict import *


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def pushToGithub(df_new,input_dir,csv_file,quest_type):

    df2 = df_new.to_csv(sep=',', index=False)

    g = Github(st.secrets["github_token"])
    # g = Github(user,github_token)
    repo = g.get_user().get_repo('createWebform')

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Upload to github
    git_prefix = input_dir+'/'+ quest_type+'/'
    
    git_file = git_prefix +csv_file.replace('.csv','_')+dt_string+'_Output.csv'

    repo.create_file(git_file, "committing files", df2, branch="main")
    st.write(git_file + ' CREATED')
    
    return

def saveAnswer(df_new,input_dir,csv_file,quest_type):

    output_dir = input_dir+'/'+ quest_type
    # Check whether the specified output path exists or not
    isExist = os.path.exists(output_dir)

    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs(output_dir)
        print('The new directory ' + output_dir + ' is created!')
    
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Upload to github
    save_prefix = output_dir + '/'
    
    save_file = save_prefix +csv_file.replace('.csv','_')+dt_string+'_Output.csv'
    # save_file = csv_file.replace('.csv','_')+dt_string+'_Output.csv'

    df_new.to_csv(save_file,sep=',', index=False)

    st.write(save_file + ' SAVED')
    
    return

def check_form(qst,idxs,ans,units,minVals,maxVals,idx_list,idxMins,idxMaxs,sum50s):

    n_qst = int((len(qst)-2)/3)
    
    check_flag = True

    for i in range(n_qst):
    
        if idxs[i] in idx_list:
        
            print('idxMin,idxMax',idxMins[i],idxMaxs[i]) 
    
            idx = 3+i*3
        
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
                    st.write('The answer must be a value >'+str(minVals[i])+' and  <'+str(maxVals[i]))
                    check_flag = False
            
                if float(ans[idx+1])<= minVals[i] or float(ans[idx+1])>= maxVals[i]:
                
                    st.write('Error. '+qst[idx+1]+':'+str(ans[idx+1]))
                    st.write('The answer must be a value  >'+str(minVal)+' and <'+str(maxVal))
                    check_flag = False
            
                if float(ans[idx+2])<= minVals[i] or float(ans[idx+2])>= maxVals[i]:
                    
                    st.write('Error. '+qst[idx+2]+':'+str(ans[idx+2]))
                    st.write('The answer must be a value >'+str(minVals[i])+' and <'+str(maxVals[i]) )
                    check_flag = False
                    
                if (idxMins[i] < idxMaxs[i]):
                
                    sum50check = 0.0
                    
                    for ii in range(idxMins[i]-1,idxMaxs[i]):
                    
                        sum50check += float(ans[4+ii*3])
                        
                    if float(sum50s[i] != sum50check):  
                      
                        st.write('Error in sum of 50%iles for questions from ',str(idxMins[i]),' to ',str(idxMaxs[i]))
                        st.write('The sum should be '+str(sum50s[i]))
                        check_flag = False
                    
                    

    return check_flag       

def main():

    st.title("Elicitation form")
    
    # check if the pdf supporting file is defined and if it exists
    if companion_document in locals:
  
        pdf_doc = input_dir+'/'+ companion_document
        # Check whether the specified output path exists or not
        isExists = os.path.exists(pdf_doc)

    else:
    
        isExists = False
  
    if isExists:  
    
        with open(pdf_doc, "rb") as pdf_file:
        
            PDFbyte = pdf_file.read()

        st.download_button(label="Download PDF Questionnaire", 
            data=PDFbyte,
            file_name=companion_document,
            mime='application/octet-stream')
    
    # read the questionnaire to a pandas dataframe	
    df = pd.read_csv('./'+input_dir+'/'+csv_file,header=0,index_col=0)
        
    try:
    
        from createWebformDict import idx_list
        print('idx_list read',idx_list)
    
    except ImportError:
    
        print('ImportError')    
        idx_list = list(df.index)
            
    if len(idx_list) == 0:
    
        idx_list = list(df.index)
            
    print('idx_list',idx_list)
        
    data_top = df.head()
    
    langs = []
    
    for head in data_top:
    
        if 'LONG Q' in head:
        
            string = head.replace('LONG Q','')
            string2 = string.replace('_','')
            
            langs.append(string2)
            
    print('langs',langs)        
             
    if (len(langs)>1):
    
        options = langs
        lang_index = st.selectbox("Language", range(len(options)), format_func=lambda x: options[x])
        print('lang_index',lang_index)
        language = options[lang_index]
        index_list = [0,1,lang_index+2]+list(range(len(langs)+2,len(langs)+12))
    
        
    else:
     
        lang_index = 0
        language = ''
        index_list = list(range(0,13))
        
    print('language',language)    
    
    print('index_list',index_list)    
    
    output_file = csv_file.replace('.csv','_NEW.csv')

    pctls = [5,50,95]

    form2 = st.form(key='form2')
    
    ans = []

    qst = ["First Name"]    
    ans.append(form2.text_input(qst[-1]))
    
    qst.append("Last Name")
    ans.append(form2.text_input(qst[-1]))
    
    qst.append("Email address")
    ans.append(form2.text_input(qst[-1]))

        
    idxs = []
    units = []
    minVals = []
    maxVals = []
    
    idxMins = []
    idxMaxs = []
    sum50s = []
        
    for i in df.itertuples():
    
        idx,shortQ,longQ,unit,scale,minVal,maxVal,realization,question,idxMin,idxMax,sum50,image = [i[j] for j in index_list]
        # print(idx,question,question == quest_type)
        minVal = float(minVal)
        maxVal = float(maxVal)
        
        if ( question == quest_type):

            units.append(unit)
            idxs.append(idx)
            
            if minVal.is_integer():
            
                minVal = int(minVal)
                    
            if maxVal.is_integer():
            
                maxVal = int(maxVal)

            minVals.append(minVal)
            maxVals.append(maxVal)
            
            sum50 = float(sum50)     
                
            idxMins.append(idxMin)
            idxMaxs.append(idxMax)
            sum50s.append(sum50)
            
            # print('idx',idx,idx in idx_list)
            
            if (idx in idx_list):
            
                form2.markdown("""___""")
                # print(idx,qst,unit,scale)
                if quest_type == 'target':
                
                    form2.header('TQ'+str(idx)+'. '+shortQ)
                    
                else:

                    form2.header('SQ'+str(idx)+'. '+shortQ)
            
                if (not pd.isnull(image)):
                    imagefile = './'+input_dir+'/images/'+str(image)
                    if os.path.exists(imagefile):  
                        form2.image('./'+input_dir+'/images/'+str(image))
                        
                if idxMin<idxMax:
                
                    longQ_NB = "**N.B.** *The sum of 50%iles for questions "+str(idxMin)+"-"+str(idxMax)+" have to sum to "+str(sum50)+".*"        
                    form2.markdown(longQ)
                    form2.markdown(longQ_NB)
                
                else:    
        
                    form2.markdown(longQ)
        
            j=0
            for pct in pctls:
                j+=1
            
                qst.append(shortQ+' - '+str(int(pct))+'%ile ('+str(minVal)+';'+str(maxVal)+')'+' ['+unit+']')
    
                if (idx in idx_list):
                
                    ans.append(form2.text_input(qst[-1]))
                    
                else:
                
                    ans.append('')
            
    submit_button2 = form2.form_submit_button("Submit")
    
    
    zip_iterator = zip(qst,ans)
    data = dict(zip_iterator)
    df_download = pd.DataFrame([ans],columns=qst)
    csv = convert_df(df_download)

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    file_download = 'myans_'+dt_string+'.csv'

    st.download_button(
        label="Download answers as CSV",
        data=csv,
        file_name=file_download,
        mime='text/csv',
    )
    
    if submit_button2:
    
        check_flag = check_form(qst,idxs,ans,units,minVals,maxVals,idx_list,idxMins,idxMaxs,sum50s)
        
        if check_flag:
    
            st.write('Thank you '+ans[0]+' '+ans[1] )
        
            zip_iterator = zip(qst,ans)
            data = dict(zip_iterator)
            df_new = pd.DataFrame([ans],columns=qst)
            
            if datarepo == 'github':

                pushToGithub(df_new,input_dir,csv_file,quest_type)
                
            else:
            
                saveAnswer(df_new,input_dir,csv_file,quest_type)
        
if __name__ == '__main__':
	main()            
