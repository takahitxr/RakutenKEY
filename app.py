import pandas as pd
from soupsieve import select
from sqlalchemy import null, true
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import gspread
import time
import datetime
from datetime import timedelta
import altair as alt
import unicodedata

tstr = "2022-06-20"
tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')
dt = datetime.datetime.today() 



clicked = st.button("キャッシュクリア")
if clicked:
    st.legacy_caching.clear_cache()

st.title("キーワード解析アプリ")
choice = st.sidebar.radio("""
メニューを選択してください。
"""
,["楽天キーワード検索", "楽天キーワード閲覧", "楽天急上昇ワード", "価格ドットコムキーワード", "価格ドットコム急上昇","お問い合わせ"]
)



@st.cache
def get_data():

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('angular-spider-312007-557058f7d529.json', scope)
    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = '1DNx5LcmrJyoxLKJM6qhasfM4CxlWOG9Yn1xmMUe2aDo'
    sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート1')
    sheet3 = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート3')
    sheet4 = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート4')
    data = sheet.get_all_values()
    data3 = sheet3.get_all_values()
    data4 = sheet4.get_all_values()


    df = pd.DataFrame(data[1:], columns=data[0])
    df3 = pd.DataFrame(data3[1:], columns=data[0])
    df4 = pd.DataFrame(data4[1:], columns=data[0])
    df = df.set_index("Date")
    df3 = df3.set_index("Date")
    df4 = df4.set_index("Date")
    return df, df3, df4

df, df3, df4 = get_data()



if choice == "楽天キーワード閲覧":
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

        with st.container():
            col1,col2,col3,col4,col5 = st.columns(5)
            with col1:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[0]}</span>', unsafe_allow_html=True)
            with col2:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[1]}</span>', unsafe_allow_html=True)
            with col3:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[2]}</span>', unsafe_allow_html=True)
            with col4:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[3]}</span>', unsafe_allow_html=True)
            with col5:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[4]}</span>', unsafe_allow_html=True)


elif choice == "楽天キーワード検索":

    
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
            addkey = st.text_input("比較1したいキーワードを入力してください")
            if addkey:
                testlist = []
                for searchday in df2:
                    alist = df2[df2[searchday].str.contains(addkey)].index
                    for a in alist:
                        testlist.append(df2[searchday][int(a)-1])
                li_uniq2 = list(set(testlist))
                choice2 = st.selectbox("比較1するキーワードを選択してください。", li_uniq2)

                choice3 = []

                addkey2 = st.text_input("比較2したいキーワードを入力してください")
                if addkey2:
                    testlist = []
                    for searchday in df2:
                        alist = df2[df2[searchday].str.contains(addkey2)].index
                        for a in alist:
                            testlist.append(df2[searchday][int(a)-1])
                    li_uniq3 = list(set(testlist))
                    choice3 = st.selectbox("比較2するキーワードを選択してください。", li_uniq3)

                    choice4 = []

                    addkey3 = st.text_input("比較3したいキーワードを入力してください")
                    if addkey3:
                        testlist = []
                        for searchday in df2:
                            alist = df2[df2[searchday].str.contains(addkey3)].index
                            for a in alist:
                                testlist.append(df2[searchday][int(a)-1])
                        li_uniq4 = list(set(testlist))
                        choice4 = st.selectbox("比較3するキーワードを選択してください。", li_uniq4)

                        choice5 = []

                        addkey4 = st.text_input("比較4したいキーワードを入力してください")
                        if addkey4:
                            testlist = []
                            for searchday in df2:
                                alist = df2[df2[searchday].str.contains(addkey4)].index
                                for a in alist:
                                    testlist.append(df2[searchday][int(a)-1])
                            li_uniq5 = list(set(testlist))
                            choice5 = st.selectbox("比較4するキーワードを選択してください。", li_uniq5)


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


                        if choice3:
                            ranklist2 = []
                            for searchday in df2:
                                if len(df2[df2[searchday] == f"{choice3}"].index) > 0:
                                    i = df2[df2[searchday] == f"{choice3}"].index[0]
                                    ranklist2.append(i)
                                else:
                                    ranklist2.append(0)

                            if not ranklist2:
                                st.error("そのキーワードは存在しません。")
                            else:                      
                                date_str_list = pd.date_range(selected_date[0], selected_date[1])
                                ranklist2 = []
                                for i in date_str_list.strftime('%Y/%m/%d'):
                                    if len(df.columns[df.loc[i] == f"{choice3}"]) > 0:
                                        ranklist2.append(df.columns[df.loc[i] == f"{choice3}"][0])
                                    else:
                                        ranklist2.append("1001")
                                        

                                minrank = min(ranklist2)
                                maxrank = max(ranklist2)

                                selection = alt.selection_multi(fields=['symbol'], bind='legend')
                                chart_data = pd.DataFrame(df.loc[date_str_list.strftime('%Y/%m/%d')])        
                                data1 = pd.DataFrame(ranklist2, columns=["ランキング"])
                                data2 = pd.DataFrame(date_str_list.strftime('%Y/%m/%d'), columns=["日付"])
                                data4 = pd.concat([data1,data2], axis=1)
                                data4["key"] = str(choice3)
                                data3 = pd.concat([data3,data4])

                                
                                if choice4:
                                    ranklist2 = []
                                    for searchday in df2:
                                        if len(df2[df2[searchday] == f"{choice4}"].index) > 0:
                                            i = df2[df2[searchday] == f"{choice4}"].index[0]
                                            ranklist2.append(i)
                                        else:
                                            ranklist2.append(0)

                                    if not ranklist2:
                                        st.error("そのキーワードは存在しません。")
                                    else:                      
                                        date_str_list = pd.date_range(selected_date[0], selected_date[1])
                                        ranklist2 = []
                                        for i in date_str_list.strftime('%Y/%m/%d'):
                                            if len(df.columns[df.loc[i] == f"{choice4}"]) > 0:
                                                ranklist2.append(df.columns[df.loc[i] == f"{choice4}"][0])
                                            else:
                                                ranklist2.append("1001")
                                                

                                        minrank = min(ranklist2)
                                        maxrank = max(ranklist2)

                                        selection = alt.selection_multi(fields=['symbol'], bind='legend')
                                        chart_data = pd.DataFrame(df.loc[date_str_list.strftime('%Y/%m/%d')])        
                                        data1 = pd.DataFrame(ranklist2, columns=["ランキング"])
                                        data2 = pd.DataFrame(date_str_list.strftime('%Y/%m/%d'), columns=["日付"])
                                        data4 = pd.concat([data1,data2], axis=1)
                                        data4["key"] = str(choice4)
                                        data3 = pd.concat([data3,data4])
                                        

                                        if choice5:
                                            ranklist2 = []
                                            for searchday in df2:
                                                if len(df2[df2[searchday] == f"{choice5}"].index) > 0:
                                                    i = df2[df2[searchday] == f"{choice5}"].index[0]
                                                    ranklist2.append(i)
                                                else:
                                                    ranklist2.append(0)

                                            if not ranklist2:
                                                st.error("そのキーワードは存在しません。")
                                            else:                      
                                                date_str_list = pd.date_range(selected_date[0], selected_date[1])
                                                ranklist2 = []
                                                for i in date_str_list.strftime('%Y/%m/%d'):
                                                    if len(df.columns[df.loc[i] == f"{choice5}"]) > 0:
                                                        ranklist2.append(df.columns[df.loc[i] == f"{choice5}"][0])
                                                    else:
                                                        ranklist2.append("1001")
                                                        

                                                minrank = min(ranklist2)
                                                maxrank = max(ranklist2)

                                                selection = alt.selection_multi(fields=['symbol'], bind='legend')
                                                chart_data = pd.DataFrame(df.loc[date_str_list.strftime('%Y/%m/%d')])        
                                                data1 = pd.DataFrame(ranklist2, columns=["ランキング"])
                                                data2 = pd.DataFrame(date_str_list.strftime('%Y/%m/%d'), columns=["日付"])
                                                data4 = pd.concat([data1,data2], axis=1)
                                                data4["key"] = str(choice5)
                                                data3 = pd.concat([data3,data4])


        chart = alt.Chart(data3).mark_line().encode(
            x="日付:T",
#            y="ランキング:Q",
            y=alt.Y("ランキング:Q", sort="descending"),
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

elif choice == "楽天急上昇ワード":

    df, df3, df4 = get_data()
    df2 = df.T
    selectday = st.date_input("日付を選択してください", max_value=dt, min_value=tdatetime)
    st.write("前日と比較してランキングが200位以上上がったキーワードを抽出します。")
    selectday = str(selectday).replace("-", "/")
    ysday = datetime.datetime.strptime(selectday.replace("/", ""), '%Y%m%d') - timedelta(1)
    ysday = ysday.strftime('%Y/%m/%d')  

    for a, item in enumerate(df2[selectday]):
        num = df2[ysday].loc[df2[ysday] == item].index
        if len(num) > 0:
            ysnum = int(num[0])
            if ysnum - int(a) + 1 > 200:
                itemplus = item.replace(" ", "+")
                itemlink = f"[{item}]({'https://search.rakuten.co.jp/search/mall/' + itemplus})"
                st.write(f'<span style="font-size: 1.2em;letter-spacing:2px">{itemlink}のランキングが{ysnum}位から{int(a) + 1}位に上昇しました。</span>', unsafe_allow_html=True)

elif choice == "価格ドットコムキーワード":
    selectday = st.date_input("日付を選択してください", max_value=dt, min_value=tdatetime)
    selectday = str(selectday).replace("-", "/")

    col1,col2,col3,col4,col5 = st.columns(5)
    dftoday = df3.loc[[selectday]].values[0]



    for idx in range(len(df3.columns) // 5):
        urls = []
        links = []
        texts = []

        for i in range(5):
            urls.append(dftoday[idx * 5 + i].replace(" ", "+"))
            links.append(f"[{dftoday[idx * 5 + i]}]({'https://search.rakuten.co.jp/search/mall/' + urls[i]})")
            texts.append(f"{idx * 5 + i + 1}位 {links[i]}")

        with st.container():
            col1,col2,col3,col4,col5 = st.columns(5)
            with col1:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[0]}</span>', unsafe_allow_html=True)
            with col2:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[1]}</span>', unsafe_allow_html=True)
            with col3:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[2]}</span>', unsafe_allow_html=True)
            with col4:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[3]}</span>', unsafe_allow_html=True)
            with col5:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[4]}</span>', unsafe_allow_html=True)


elif choice == "価格ドットコム急上昇":

    selectday = st.date_input("日付を選択してください", max_value=dt, min_value=tdatetime)
    selectday = str(selectday).replace("-", "/")

    col1,col2,col3,col4,col5 = st.columns(5)
    dftoday = df4.loc[[selectday]].values[0]

    for idx in range(len(df4.columns) // 5):
        urls = []
        links = []
        texts = []

        for i in range(5):
            urls.append(dftoday[idx * 5 + i].replace(" ", "+"))
            links.append(f"[{dftoday[idx * 5 + i]}]({'https://search.rakuten.co.jp/search/mall/' + urls[i]})")
            texts.append(f"{idx * 5 + i + 1}位 {links[i]}")

        with st.container():
            col1,col2,col3,col4,col5 = st.columns(5)
            with col1:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[0]}</span>', unsafe_allow_html=True)
            with col2:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[1]}</span>', unsafe_allow_html=True)
            with col3:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[2]}</span>', unsafe_allow_html=True)
            with col4:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[3]}</span>', unsafe_allow_html=True)
            with col5:
                st.write(f'<span style="font-size: 0.8em;letter-spacing:2px">{texts[4]}</span>', unsafe_allow_html=True)

elif choice == "お問い合わせ":
    st.write("ツールの不具合等があった際は、下記のURLにアクセスしていただきご記入ください。")

    st.write(f'<span style="font-size: 1.4em;letter-spacing:2px">[お問い合わせ](https://docs.google.com/forms/d/e/1FAIpQLSdgRvJNzOgBHSdem3CbElkrDAbDAe4--NEnxJyIasXGbBHwsg/viewform)</span>', unsafe_allow_html=True)
