import pandas as pd
import re


def find_word(sstr, wword):
    if '_' in wword:
        return sstr.find(wword[1:])
    else:
        return sstr.find(wword)


def words_rule(wordss, dfcol):
    word_sp_col = dfcol.split('-')
    word_sp_find = [find_word(wordss, i) for i in word_sp_col]

    nn = -1
    for wor, posi in zip(word_sp_col, word_sp_find):
        if ('_' in wor) and (posi != -1):
            return 0
        elif '_' not in wor:
            if nn < posi:
                nn = posi
            else:
                return 0
    return 1


def new_find_word(wword):
    if '_' in wword:
        return wword[1:]
    else:
        return wword


def new_words_rule(txt, kword):
    kword = str(kword)
    if ('-' in kword) and ('_' in kword):  # '_不-好'
        re_pattern = '.*'.join([new_find_word(i) for i in kword.split('-')])
        re_result = re.search(re_pattern, txt)
        if re_result:
            return 0

        re_pattern = '.*'.join([i for i in kword.split('-') if '_' not in i])
        re_result = re.search(re_pattern, txt)
        if re_result:
            return 1

        return 0

    elif ('-' in kword) and ('_' not in kword):  # '不-好'
        re_pattern = '.*'.join([i for i in kword.split('-')])
        re_result = re.search(re_pattern, txt)
        if re_result:
            return 1
        else:
            return 0

    elif ('-' not in kword) and ('_' not in kword):  # '不好'
        re_result = re.search(kword, txt)
        if re_result:
            return 1
        else:
            return 0

    elif ('-' not in kword) and ('_' in kword):
        return 0.0001
        raise TypeError('单独_模式不可用')


def keyword_columns(df2, dfcol):
    df = df2.copy()
    if dfcol in df.columns:
        return df
    else:
        count_num = len(df)
        series_col = df[df.columns[0]].map(lambda x: new_words_rule(x, dfcol))
        df[dfcol] = series_col
        return df


def readfile(*args, **kwargs):
    try:
        with open(args[0], 'r') as f:
            df = pd.read_csv(f)
            return df
    except:
        print('cant read')

    try:
        with open(args[0], 'r', encoding='gb18030') as f:
            df = pd.read_csv(f)
            return df
    except:
        print('cant read')

    try:
        df = pd.read_csv(*args, **kwargs)
        return df
    except:
        print('cant read')

    try:
        df = pd.read_csv(*args, **kwargs, encoding='gb18030')
        return df
    except:
        print('cant read')

    try:
        df = pd.read_excel(*args, **kwargs)
        return df
    except:
        print('cant read')

    try:
        df = pd.read_excel(*args, **kwargs, encoding='gb18030')
        return df
    except:
        print('cant read')

if __name__ == '__main__':
    print(new_words_rule('美白', '_美白-_完美-美-_美白-_完美'))
