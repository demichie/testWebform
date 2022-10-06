import pandas as pd
import streamlit as st
import os.path

from github import Github
from github import InputGitTreeElement
from datetime import datetime


input_dir = 'DATA' 
csv_file = 'questionnaire.csv'

# this can be 'seed' or 'target'
quest_type = 'target'

idx_list = [1,2,3,4,5]

# select 'github' or 'local'
datarepo = 'github'

# user = 'username'
# github_token = "token"

pctls = [5, 50, 95]


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def pushToGithub(df_new, input_dir, csv_file, quest_type):

    df2 = df_new.to_csv(sep=',', index=False)

    g = Github(st.secrets["github_token"])
    # g = Github(user,github_token)
    repo = g.get_user().get_repo('createWebform')

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    # Upload to github
    git_prefix = input_dir + '/' + quest_type + '/'

    git_file = git_prefix + csv_file.replace('.csv',
                                             '_') + dt_string + '_Output.csv'

    repo.create_file(git_file, "committing files", df2, branch="main")
    st.write(git_file + ' CREATED')

    return


def saveAnswer(df_new, input_dir, csv_file, quest_type):

    output_dir = input_dir + '/' + quest_type
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

    save_file = save_prefix + csv_file.replace('.csv',
                                               '_') + dt_string + '_Output.csv'
    # save_file = csv_file.replace('.csv','_')+dt_string+'_Output.csv'

    df_new.to_csv(save_file, sep=',', index=False)

    st.write(save_file + ' SAVED')

    return


def check_form(qst, idxs, ans, units, minVals, maxVals, idx_list):

    n_qst = int((len(qst) - 2) / 3)

    check_flag = True

    for i in range(n_qst):

        if idxs[i] in idx_list:

            idx = 2 + i * 3

            try:
                float(ans[idx])
            except ValueError:
                st.write('Non numeric answer')
                st.write(qst[idx], ans[idx])
                check_flag = False

            try:
                float(ans[idx + 1])
            except ValueError:
                st.write('Non numeric answer')
                st.write(qst[idx + 1], ans[idx + 1])
                check_flag = False

            try:
                float(ans[idx + 2])
            except ValueError:
                st.write('Non numeric answer')
                st.write(qst[idx + 2], ans[idx + 2])
                check_flag = False

            if check_flag:

                if float(ans[idx]) >= float(ans[idx + 1]):

                    st.write('Error. ' + qst[idx] + ' >= ' + qst[idx + 1])
                    check_flag = False

                if float(ans[idx + 1]) >= float(ans[idx + 2]):

                    st.write('Error. ' + qst[idx + 1] + ' >= ' + qst[idx + 2])
                    check_flag = False

                if float(ans[idx]) <= minVals[i] or float(
                        ans[idx]) >= maxVals[i]:

                    st.write('Error. ' + qst[idx] + ':' + str(ans[idx]))
                    st.write('The answer must be a value >' + str(minVals[i]) +
                             ' and  <' + str(maxVals[i]))
                    check_flag = False

                if float(ans[idx + 1]) <= minVals[i] or float(
                        ans[idx + 1]) >= maxVals[i]:

                    st.write('Error. ' + qst[idx + 1] + ':' +
                             str(ans[idx + 1]))
                    st.write('The answer must be a value  >' + str(minVal) +
                             ' and <' + str(maxVal))
                    check_flag = False

                if float(ans[idx + 2]) <= minVals[i] or float(
                        ans[idx + 2]) >= maxVals[i]:

                    st.write('Error. ' + qst[idx + 2] + ':' +
                             str(ans[idx + 2]))
                    st.write('The answer must be a value >' + str(minVals[i]) +
                             ' and <' + str(maxVals[i]))
                    check_flag = False

    return check_flag


def main():

    st.title("Elicitation form")

    df = pd.read_csv('./' + input_dir + '/' + csv_file, header=0, index_col=0)

    print(df)

    data_top = df.head()

    langs = []

    for head in data_top:

        if 'LONG Q' in head:

            string = head.replace('LONG Q', '')
            string2 = string.replace('_', '')

            langs.append(string2)

    print('langs', langs)

    if (len(langs) > 1):

        options = langs
        lang_index = st.selectbox("Language",
                                  range(len(options)),
                                  format_func=lambda x: options[x])
        print('lang_index', lang_index)
        language = options[lang_index]
        index_list = [0, 1, lang_index + 2] + list(
            range(len(langs) + 2,
                  len(langs) + 9))

    else:

        lang_index = 0
        language = ''
        index_list = list(range(0, 10))

    print('language', language)

    print('index_list', index_list)

    output_file = csv_file.replace('.csv', '_NEW.csv')

    pctls = [5, 50, 95]

    form2 = st.form(key='form2')

    qst = ["First Name"]
    ans = []

    ans.append(form2.text_input(qst[-1]))

    qst.append("Last Name")
    ans.append(form2.text_input(qst[-1]))

    idxs = []
    units = []
    minVals = []
    maxVals = []

    for i in df.itertuples():

        idx, shortQ, longQ, unit, scale, minVal, maxVal, realization, question, image = [
            i[j] for j in index_list
        ]
        print(idx, question, question == quest_type)
        minVal = float(minVal)
        maxVal = float(maxVal)

        if (question == quest_type):

            units.append(unit)
            idxs.append(idx)

            if minVal.is_integer():

                minVal = int(minVal)

            if maxVal.is_integer():

                maxVal = int(maxVal)

            minVals.append(minVal)
            maxVals.append(maxVal)

            print('idx', idx, idx in idx_list)

            if (idx in idx_list):

                form2.markdown("""___""")
                # print(idx,qst,unit,scale)
                form2.header('Q' + str(idx) + '. ' + shortQ)

                if (not pd.isnull(image)):
                    imagefile = './' + input_dir + '/images/' + str(image)
                    if os.path.exists(imagefile):
                        form2.image('./' + input_dir + '/images/' + str(image))

                form2.markdown(longQ)

            j = 0
            for pct in pctls:
                j += 1

                qst.append(shortQ + ' - ' + str(int(pct)) + '% (' +
                           str(minVal) + ';' + str(maxVal) + ')' + ' [' +
                           unit + ']')

                if (idx in idx_list):

                    ans.append(form2.text_input(qst[-1]))

                else:

                    ans.append('')

    submit_button2 = form2.form_submit_button("Submit")

    zip_iterator = zip(qst, ans)
    data = dict(zip_iterator)
    df_download = pd.DataFrame([ans], columns=qst)
    csv = convert_df(df_download)

    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H:%M:%S")

    file_download = 'myans_' + dt_string + '.csv'

    st.download_button(
        label="Download answers as CSV",
        data=csv,
        file_name=file_download,
        mime='text/csv',
    )

    if submit_button2:

        check_flag = check_form(qst, idxs, ans, units, minVals, maxVals,
                                idx_list)

        if check_flag:

            st.write('Thank you ' + ans[0] + ' ' + ans[1])

            zip_iterator = zip(qst, ans)
            data = dict(zip_iterator)
            df_new = pd.DataFrame([ans], columns=qst)

            if datarepo == 'github':

                pushToGithub(df_new, input_dir, csv_file, quest_type)

            else:

                saveAnswer(df_new, input_dir, csv_file, quest_type)


if __name__ == '__main__':
    main()
