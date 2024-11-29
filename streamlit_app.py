import streamlit as st
import pandas as pd
from datastr import dataprocessing
import altair as alt
accepted_file_types = ["csv"]
uploaded_files = st.file_uploader(
    label="请选择一个CSV文件",
    accept_multiple_files=False,
    type=accepted_file_types
)
@st.cache_data
def get_data(uploaded_files):
    linedict = dict()
    data = pd.read_csv(uploaded_files, encoding="utf-16", skiprows=12)
    linename = str(data.iloc[0, 0]).split(";")
    count = 0
    number = int(100 / len(linename))
    progressnumber = 0
    my_bar = st.progress(progressnumber, "正在处理")
    for l in linename:
        progressnumber += number
        my_bar.progress(progressnumber, f"正在处理第{count}列数据，共有{len(linename)}列数据！")
        datalist = list()
        for i in range(1, data.shape[0]):
            res = str(data.iloc[i, 0]).split(";")
            datalist.append(dataprocessing(res[count]))
        linedict[l] = datalist
        count += 1
    my_bar.progress(100, "处理完成！")
    return linedict
if uploaded_files is not None:
    if st.checkbox('查看数据转换表'):
        data = get_data(uploaded_files)
        df = pd.DataFrame(data)
        st.dataframe(df)
    if st.checkbox("查看折线图"):
        data = get_data(uploaded_files)
        optionslist = list()
        for key in data.keys():
            optionslist.append(key)
        optionslist.pop(0)
        optionslist.pop(0)
        options = st.multiselect(
            '请选择需要查看的数据列',
            optionslist,[])
        # print(options)
        chart = dict()
        if st.button("确定查看"):
            my_bar1 = st.progress(0, "正在处理")
            if options:
                chart = {key: data[key] for key in options}
                Timedata = list(data["Time"])
                years = Timedata
                data_list = []
                my_bar1.progress(10,"分析数据中")
                for category, revenues in chart.items():
                    for year, revenue in zip(years, revenues):
                        my_bar1.progress(50, "分析数据中")
                        data_list.append({'Time': year, 'Revenue': revenue, 'Category': category})
                df = pd.DataFrame(data_list)
                my_bar1.progress(60, "分析数据完成")
                # 创建基础图表
                base = alt.Chart(df).encode(
                    x=alt.X('Time', title='时间')
                )
                my_bar1.progress(80, "创建数据图表")
                # 创建多个折线图
                lines = []
                for category in df['Category'].unique():
                    line = base.transform_filter(
                        alt.datum.Category == category
                    ).mark_line().encode(
                        y=alt.Y('Revenue', title='温度', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Category', legend=alt.Legend(title='类别'))
                    )
                    lines.append(line)
                # 合并图表
                final_chart = alt.layer(*lines).properties(
                    title='数据变化趋势',
                    width=600,
                    height=400
                )
                # 显示图表
                st.altair_chart(final_chart, use_container_width=True)
                my_bar1.progress(100, "数据分析完成，请查看图表")


