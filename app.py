import pandas as pd
from soupsieve import select
from sqlalchemy import null, true
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import gspread
import time
import datetime
import altair as alt
import unicodedata

tstr = "2022-06-20"
tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')

dt = datetime.datetime.today() 
tstr = "2022-06-20"
tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')


st.title("楽天キーワード解析アプリ")
choice = st.sidebar.radio("""
メニューを選択してください。
"""
,["キーワード閲覧", "キーワード検索"]
)


@st.cache
def get_data():

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('angular-spider-312007-557058f7d529.json', scope)
    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = '1DNx5LcmrJyoxLKJM6qhasfM4CxlWOG9Yn1xmMUe2aDo'
    sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート1')

    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.set_index("Date")

    return df

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

clicked = st.button("キャッシュクリア")
if clicked:
    st.legacy_caching.clear_cache()


df= get_data()


if choice == "キーワード閲覧":
    selectday = st.date_input("日付を選択してください", max_value=dt, min_value=tdatetime)
    selectday = str(selectday).replace("-", "/")

    col1,col2,col3,col4,col5 = st.columns(5)
    dftoday = df.loc[[selectday]].values[0]



    for idx in range(len(df.columns) // 5):
        urls = []
        links = []
        texts = []

        for i in range(5):
            urls.append(dftoday[idx * 5 + i].replace(" ", "+"))
            links.append(f"[{dftoday[idx * 5 + i]}]({'https://search.rakuten.co.jp/search/mall/' + urls[i]})")
            texts.append(f"{idx * 5 + i + 1}位 {links[i]}")
            
            if idx < 20:
                if get_east_asian_width_count(dftoday[idx * 5 + i]) <= 12:
                    texts[i] = texts[i] + "<br><br><br>"
                elif get_east_asian_width_count(dftoday[idx * 5 + i]) <= 28 and get_east_asian_width_count(dftoday[idx * 5 + i]) > 12:
                    texts[i] = texts[i] + "<br><br>"
            else:
                if get_east_asian_width_count(dftoday[idx * 5 + i]) <= 11:
                    texts[i] = texts[i] + "<br><br><br>"
                elif get_east_asian_width_count(dftoday[idx * 5 + i]) <= 27 and get_east_asian_width_count(dftoday[idx * 5 + i]) > 11:
                    texts[i] = texts[i] + "<br><br>"


            # if i == 4:
            #     for j in range(5):
            #         if len(dftoday[idx * 5 + j]) < 6:
            #             texts[j] = texts[j] + "<br><br>"

        
        col1.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[0]}</span>', unsafe_allow_html=True)
        col2.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[1]}</span>', unsafe_allow_html=True)
        col3.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[2]}</span>', unsafe_allow_html=True)
        col4.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[3]}</span>', unsafe_allow_html=True)
        col5.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[4]}</span>', unsafe_allow_html=True)



        # url1 = dftoday[idx * 5 + 0].replace(" ", "+")
        # url2 = dftoday[idx * 5 + 1].replace(" ", "+")
        # url3 = dftoday[idx * 5 + 2].replace(" ", "+")
        # url4 = dftoday[idx * 5 + 3].replace(" ", "+")
        # url5 = dftoday[idx * 5 + 4].replace(" ", "+")

        # links = [5]

        # links[0] = f"[{dftoday[idx * 5 + 0]}]({'https://search.rakuten.co.jp/search/mall/' + url1})"
        # links[1] = f"[{dftoday[idx * 5 + 1]}]({'https://search.rakuten.co.jp/search/mall/' + url2})"
        # links[2] = f"[{dftoday[idx * 5 + 2]}]({'https://search.rakuten.co.jp/search/mall/' + url3})"
        # links[3] = f"[{dftoday[idx * 5 + 3]}]({'https://search.rakuten.co.jp/search/mall/' + url4})"
        # links[4] = f"[{dftoday[idx * 5 + 4]}]({'https://search.rakuten.co.jp/search/mall/' + url5})"


        # text1 = f"{idx * 5 + 1}位 {links[0]}"
        # text2 = f"{idx * 5 + 2}位 {links[1]}"
        # text3 = f"{idx * 5 + 3}位 {links[2]}"
        # text4 = f"{idx * 5 + 4}位 {links[3]}"
        # text5 = f"{idx * 5 + 5}位 {links[4]}"
        
        # with st.container():
        #     col1,col2,col3,col4,col5 = st.columns(5)
        #     with col1:
        #         st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{text1}</span>', unsafe_allow_html=True)
        #     with col2:
        #         st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{text2}</span>', unsafe_allow_html=True)
        #     with col3:
        #         st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{text3}</span>', unsafe_allow_html=True)
        #     with col4:
        #         st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{text4}</span>', unsafe_allow_html=True)
        #     with col5:
        #         st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{text5}</span>', unsafe_allow_html=True)




            # if idx % 20 == 0:
            #     col1.write("------------------------------------------------------")
            #     col2.write("------------------------------------------------------")
            #     col3.write("------------------------------------------------------")
            #     col4.write("------------------------------------------------------")
            #     col5.write("------------------------------------------------------")      

else:

    
    keycol1,keycol2 = st.columns(2)
    selectkey = st.text_input("検索したいキーワードを入力してください。")



    if selectkey:
        df2 = df.T
        testlist = []
        for searchday in df2:
            alist = df2[df2[searchday].str.contains(selectkey)].index
            for a in alist:
                testlist.append(df2[searchday][int(a)-1])
        li_uniq = list(set(testlist))
        choice = st.selectbox("キーワードを選択してください。", li_uniq)
        choice2 = []
        
        with st.expander("比較"):
            addkey = st.text_input("比較したいキーワードを入力してください")
            if addkey:
                testlist = []
                for searchday in df2:
                    alist = df2[df2[searchday].str.contains(addkey)].index
                    for a in alist:
                        testlist.append(df2[searchday][int(a)-1])
                li_uniq2 = list(set(testlist))
                choice2 = st.selectbox("比較するキーワードを選択してください。", li_uniq2)

        if choice:
            ranklist = []
            for searchday in df2:
                if len(df2[df2[searchday] == f"{choice}"].index) > 0:
                    i = df2[df2[searchday] == f"{choice}"].index[0]
                    ranklist.append(i)
                else:
                    ranklist.append(0)


            if not ranklist:
                st.error("そのキーワードは存在しません。")
            else:
                if choice != "":
                    selected_date = st.date_input(
                    "日付を選択してください。", [tdatetime, dt], max_value=dt, min_value=tdatetime
                    )

                
                date_str_list = pd.date_range(selected_date[0], selected_date[1])
                rakulist = []
                for i in date_str_list.strftime('%Y/%m/%d'):
                    if len(df.columns[df.loc[i] == f"{choice}"]) > 0:
                        rakulist.append(df.columns[df.loc[i] == f"{choice}"][0])
                    else:
                        rakulist.append("1001")
                        

                minrank = min(rakulist)
                maxrank = max(rakulist)


                selection = alt.selection_multi(fields=['symbol'], bind='legend')
                chart_data = pd.DataFrame(df.loc[date_str_list.strftime('%Y/%m/%d')])        
                data1 = pd.DataFrame(rakulist, columns=["ランキング"])
                data2 = pd.DataFrame(date_str_list.strftime('%Y/%m/%d'), columns=["日付"])
                data3 = pd.concat([data1,data2], axis=1)
                data3["key"] = str(choice)
            
                if choice2:
                    ranklist2 = []
                    for searchday in df2:
                        if len(df2[df2[searchday] == f"{choice2}"].index) > 0:
                            i = df2[df2[searchday] == f"{choice2}"].index[0]
                            ranklist2.append(i)
                        else:
                            ranklist2.append(0)

                    if not ranklist2:
                        st.error("そのキーワードは存在しません。")
                    else:                      
                        date_str_list = pd.date_range(selected_date[0], selected_date[1])
                        ranklist2 = []
                        for i in date_str_list.strftime('%Y/%m/%d'):
                            if len(df.columns[df.loc[i] == f"{choice2}"]) > 0:
                                ranklist2.append(df.columns[df.loc[i] == f"{choice2}"][0])
                            else:
                                ranklist2.append("1001")
                                

                        minrank = min(ranklist2)
                        maxrank = max(ranklist2)

                        selection = alt.selection_multi(fields=['symbol'], bind='legend')
                        chart_data = pd.DataFrame(df.loc[date_str_list.strftime('%Y/%m/%d')])        
                        data1 = pd.DataFrame(ranklist2, columns=["ランキング"])
                        data2 = pd.DataFrame(date_str_list.strftime('%Y/%m/%d'), columns=["日付"])
                        data4 = pd.concat([data1,data2], axis=1)
                        data4["key"] = str(choice2)
                        data3 = pd.concat([data3,data4])

        chart = alt.Chart(data3).mark_line().encode(
            x="日付:T",
            y="ランキング:Q",
            color="key:N",
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
            ).add_selection(
                selection
        )

        hover = alt.selection_single(
            fields=["日付"],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        chart_temp = (
            alt.Chart(data3)
            .encode(
                x="日付:T",
                y="ランキング:Q",
                color="key:N",
                )
        )
        tooltips = (
            alt.Chart(data3)
            .mark_rule()
            .encode(
                x="日付:T",
                y="ランキング:Q",
                color="key:N",
                opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
                tooltip=[
                    alt.Tooltip("日付:T", title="日付"),
                    alt.Tooltip("ランキング:Q", title="ランキング"),
                    alt.Tooltip("key:N", title="キーワード")
                ],
            )
            .add_selection(hover)
        )

        points = chart_temp.transform_filter(hover).mark_circle(size=50)
#                chart = (alt.Chart(data3).mark_line().encode(x="日付:T", y=alt.Y("ランキング:Q",stack=None, scale=alt.Scale(domain=[minrank, maxrank])), color=f"{choice}:N",shape=f"{choice}:N"))
        st.altair_chart((chart + points + tooltips), use_container_width=True)
