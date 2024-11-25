import streamlit as st
import pandas as pd
from datastr import dataprocessing
accepted_file_types = ["csv"]
uploaded_files = st.file_uploader(
    label="请选择一个CSV文件",
    accept_multiple_files=False,
    type=accepted_file_types
)

if uploaded_files is not None:
    linedict = dict()

    if st.button('查看数据转换表'):

        data = pd.read_csv(uploaded_files, encoding="utf-16", skiprows=12)
        linename = str(data.iloc[0, 0]).split(";")
        count = 0

        number = int(100/len(linename))
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
    df = pd.DataFrame(linedict)
    st.write(df)







