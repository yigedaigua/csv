import streamlit as st
import pandas as pd
from datastr import dataprocessing,Screening_time
import altair as alt
from datetime import time, datetime
accepted_file_types = ["csv"]
uploaded_files = st.file_uploader(
    label="请选择一个CSV文件",
    accept_multiple_files=False,
    type=accepted_file_types
)

@st.cache_data
def get_data(uploaded_files):
    st.write("正在处理数据！")
    linedict = dict()
    linename = str(data.iloc[11,0]).split(";")
    count = 0
    number = int(100 / len(linename))
    progressnumber = 0
    my_bar = st.progress(progressnumber, "正在处理")
    # linename是数据的列，值为94
    for l in linename:
        progressnumber += number
        my_bar.progress(progressnumber, f"正在处理第{count}列数据，共有{len(linename)}列数据！")
        datalist = list()
        for i in range(12, data.shape[0]):
            res = str(data.iloc[i, 0]).split(";")
            datalist.append(dataprocessing(res[count]))
        linedict[l] = datalist
        count += 1
    my_bar.progress(100, "处理完成！")
    return linedict

if uploaded_files is not None:
    if st.checkbox('查看数据转换表'):
        Iszh = False
        data = pd.read_csv(uploaded_files, encoding="utf-16")
        # 此变量判断导入的数据是中文还是英文
        for i in range(10):
            res = str(data.iloc[i, 0])
            st.write(res)
            if "zh" in res:
                Iszh = True
                continue
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

            if Iszh:
                chart = dict()
                selectcolname = st.selectbox('请选择需要查看的数据列',
                                             ['默认-空', '压力', '流量', '加热+电流', '调节', ])
                if selectcolname == '压力':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["温度额定值 (当前)", "出水 (始流)", "回流", "调节比率", "流量",
                                              "系统压力额定值", "系统压力", "泵压力差"])
                elif selectcolname == '流量':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["温度额定值 (当前)", "出水 (始流)", "回流", "调节比率", "流量",
                                              "系统压力", "始流压力", "泵压力差", "过滤的流速错误率"])

                elif selectcolname == '加热+电流':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["温度额定值 (当前)", "出水 (始流)", "回流", "调节比率", "流量",
                                              "加热电流 L1", "加热电流 L2", "加热电流 L3", "L1 相位加热电压",
                                              "L2 相位加热电压"])
                elif selectcolname == '调节':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["温度额定值 (当前)", "出水 (始流)", "回流", "调节比率", "流量",
                                              "冷却1调节行程", "冷却2调节行程"])
                else:
                    options = st.multiselect('请选择需要查看的数据列', optionslist, [])
                appointment = st.slider(
                    "请选择要查看的数据的时间范围",
                    value=(time(0, 0), time(23, 59)))

                if options:
                    if st.button("确定查看图表"):
                        my_bar1 = st.progress(0, "正在处理")
                        chart = {key: data[key] for key in options}
                        Timedata = list(data["时间"])
                        years = Timedata
                        data_list = []
                        my_bar1.progress(10,"分析数据中")
                        for category, revenues in chart.items():
                            for year, revenue in zip(years, revenues):
                                my_bar1.progress(50, "分析数据中")
                                if Screening_time(appointment,year):
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
                                y=alt.Y('Revenue', title='温度', scale=alt.Scale()),
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
                else:
                    st.error('请选择要查看的数据列！')
            else:
                chart = dict()
                selectcolname = st.selectbox('请选择需要查看的数据列',
                                             ['默认-空', 'Pressure', 'Flow', 'Heating+Current', 'Regulation', ])
                if selectcolname == 'Pressure':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["Set temperature (current)", "Main line", "Return line",
                                              "Regulation ratio", "Flow rate",
                                              "Set value system pressure", "System pressure",
                                              "Pump pressure differential"])
                elif selectcolname == 'Flow':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["Set temperature (current)", "Main line", "Return line",
                                              "Regulation ratio", "Flow rate",
                                              "System pressure", "Main line pressure", "Pump pressure differential",
                                              "Error rate flow rate filtered"])

                elif selectcolname == 'Heating+Current':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["Set temperature (current)", "Main line", "Return line",
                                              "Regulation ratio",
                                              "Flow rate",
                                              "Heating current L1", "Heating current L2", "Heating current L3",
                                              "L1 phase heating voltage", "L2 phase heating voltage"])
                elif selectcolname == 'Regulation':
                    options = st.multiselect('请选择需要查看的数据列', optionslist,
                                             ["Set temperature (current)", "Main line", "Return line",
                                              "Regulation ratio",
                                              "Flow rate",
                                              "Position cooling valve 1", "Position cooling valve 2"])
                else:
                    options = st.multiselect('请选择需要查看的数据列', optionslist, [])
                appointment = st.slider(
                    "请选择要查看的数据的时间范围",
                    value=(time(0, 0), time(23, 59)))
                if options:
                    if st.button("确定查看图表"):
                        my_bar1 = st.progress(0,"正在处理")
                        chart = {key: data[key] for key in options}
                        Timedata = list(data["Time"])
                        years = Timedata
                        data_list = []
                        my_bar1.progress(10,"分析数据中")
                        for category, revenues in chart.items():
                            for year, revenue in zip(years, revenues):
                                my_bar1.progress(50, "分析数据中")
                                if Screening_time(appointment, year):
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
                                y=alt.Y('Revenue', title='温度', scale=alt.Scale()),
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
                else:
                    st.error('请选择要查看的数据列！')
