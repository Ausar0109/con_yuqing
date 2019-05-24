from .yqcore import readfile, keyword_columns
import shutil
import os
import pandas as pd

data_path = 'C:\\Users\\cheng.lu\\Desktop\\yq_data\\'
mid_path = 'C:\\Users\\cheng.lu\\Desktop\\yq_mid\\'
res_path = 'C:\\Users\\cheng.lu\\Desktop\\yq_res\\'


def clean_all():
    for i in os.listdir(mid_path):
        try:
            shutil.rmtree(mid_path + i)
        except:
            pass

        try:
            os.remove(mid_path + i)
        except:
            pass


def yq_task():
    taskname = os.listdir(mid_path)[0]

    # 解压缩该文件
    shutil.unpack_archive(mid_path + taskname, mid_path)
    # 把 yq_mid 文件夹中的文件【 移动 】 到 yq_data
    shutil.move(mid_path + taskname, data_path + taskname)

    # 找到mid_path中的cibao 和 df
    for i in os.listdir(mid_path):

        if len(readfile(mid_path + i).columns) > 1:
            cibao = readfile(mid_path + i)
            _cibao = pd.DataFrame(
                [['程序补充'] * len(cibao.columns)], columns=cibao.columns)
            cibao = pd.concat([cibao, _cibao])
        elif len(readfile(mid_path + i).columns) == 1:
            # 只有一列
            filename = i.split('.')[0]  # 清洗数据格式
            df = readfile(mid_path + i)
            df.columns = ['【源数据】']
            df['【源数据】'] = df['【源数据】'].map(lambda x: str(x))
            _df = pd.DataFrame(
                [['程序补充'] * len(df.columns)], columns=df.columns)
            df = pd.concat([df, _df])

        os.remove(mid_path + i)

    # 整理cibao 的格式
    for x in cibao.columns:
        for y in range(len(cibao[x])):
            if pd.isnull(cibao[x].iloc[y]):
                cibao[x].iloc[y] = cibao[x].iloc[y - 1]

    # 舆情分析
    rizhipath = res_path + filename + '【分析结果】.xlsx'
    pd.DataFrame([]).to_excel(rizhipath)
    excelWriter = pd.ExcelWriter(rizhipath)

    df.to_excel(excelWriter, sheet_name='原始数据', index=False)

    for x in cibao[cibao.columns[-1]]:
        df = keyword_columns(df, x)

    cdf = df.sum(axis=0)
    cibao['频数'] = cibao[cibao.columns[-1]].map(cdf)

    # 将结果导入 res_path

    res = cibao.groupby(list(cibao.columns[: -2]))[['频数']].sum()
    res['占比'] = (res['频数'] / res['频数'].sum()
                 ).map(lambda x: str(100 * x)[:4] + '%')
    res.sort_values(by='频数', ascending=False)
    res.to_excel(excelWriter, sheet_name='分组结果统计')
    res = res.loc[res.频数 != 0]
    res.sort_values(by='频数', ascending=False)
    res.to_excel(excelWriter, sheet_name='分组结果去零')

    res = cibao.groupby(list(cibao.columns[:-1]))[['频数']].sum()
    res['占比'] = (res['频数'] / res['频数'].sum()
                 ).map(lambda x: str(100 * x)[:4] + '%')
    res.sort_values(by='频数', ascending=False)
    res.to_excel(excelWriter, sheet_name='索引展开统计')
    res = res.loc[res.频数 != 0]
    res.sort_values(by='频数', ascending=False)
    res.to_excel(excelWriter, sheet_name='索引展开去零')

    excelWriter.save()
    excelWriter.close()

    return filename
