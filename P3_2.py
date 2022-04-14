import CalcScore
import Handle_number
from time import time
"""给定dict,利用FMM算法对输入文本文件进行分词，
格式参照分词语料 “词/_词/_......”) * 这里的_代表空格
"""


def init(test_file = '199801_sent.txt'):
    """
    为fmm或bmm读取词典以及测试集中的必要信息，包括词典中的词、最大词长
    :return:
    """
    with open('dic.txt', 'r', encoding='utf-8') as file_dic:
        dic = file_dic.read().split('\n')
    with open(test_file, 'r', encoding='gbk') as file_sent:
        texts = file_sent.readlines()
    max_len = 0
    for word in dic:
        if len(word) > max_len:
            max_len = len(word)
    return texts,max_len,dic


def fmm(texts,max_len,dic):
    with open('seg_FMM.txt', 'w', encoding='utf-8') as fmm_file:
        line_num = len(texts)
        for index,text in enumerate(texts):
            text_write, text_len ='', len(text)  # 当前行文本长度    5  0-4
            while text_len > 0:
                find_word = text[0:max_len if max_len < text_len else text_len]
                for j in range(len(find_word), 0, -1):
                    if find_word[0: j] in dic or j == 1:
                        text_write += find_word[0:j] + "/ "
                        text = text[j:]
                        break
                text_len = len(text)
            fmm_file.write(Handle_number.handle_specond(text_write)+ ('\n' if index != line_num -1 else ''))

def bmm(texts,max_len,dic):
    with open('seg_BMM.txt', 'w', encoding='utf-8') as bmm_file:
        line_num = len(texts)
        for index,text in enumerate(texts):
            text_write, text_len = '', len(text)  # 当前行文本长度    5  0-4
            while text_len > 0:
                find_word = text[-1*(max_len if max_len < text_len else text_len):]
                for j in range(len(find_word)):
                    if find_word[j:] in dic or j == (len(find_word) -1):
                        text_write = find_word[j:] + "/ "+text_write
                        text = text[:-(len(find_word)-j)]
                        break
                text_len = len(text)
            bmm_file.write(Handle_number.handle_specond(text_write) + ('\n' if index != line_num -1 else ''))

def fmm_time(texts,max_len,dic):
    """
    用于part4计算时间,将结果写入3.txt
    """
    with open('3.txt', 'w', encoding='utf-8') as fmm_file:
        line_num = len(texts)
        start_t = time()
        for index,text in enumerate(texts):
            if index % 70 == 0:
                text_write, text_len ='', len(text)  # 当前行文本长度    5  0-4
                while text_len > 0:
                    find_word = text[0:max_len if max_len < text_len else text_len]
                    for j in range(len(find_word), 0, -1):
                        if find_word[0: j] in dic or j == 1:
                            text_write += find_word[0:j] + "/ "
                            text = text[j:]
                            break
                    text_len = len(text)
                fmm_file.write(Handle_number.handle_specond(text_write)+ ('\n' if index != line_num -1 else ''))
        end_t = time()
    return (end_t - start_t) * 70

def bmm_time(texts,max_len,dic):
    """
    用于part4计算时间,将结果写入4.txt
    """
    with open('4.txt', 'w', encoding='utf-8') as bmm_file:
        line_num = len(texts)
        start_t = time()
        for index,text in enumerate(texts):
            if index % 70 ==0:
                text_write, text_len = '', len(text)  # 当前行文本长度    5  0-4
                while text_len > 0:
                    find_word = text[-1*(max_len if max_len < text_len else text_len):]
                    for j in range(len(find_word)):
                        if find_word[j:] in dic or j == (len(find_word) -1):
                            text_write = find_word[j:] + "/ "+text_write
                            text = text[:-(len(find_word)-j)]
                            break
                    text_len = len(text)
                bmm_file.write(Handle_number.handle_specond(text_write) + ('\n' if index != line_num -1 else ''))
        end_t = time()
    return (end_t - start_t) * 70

# 客户端
# texts,max_len,dic = init()  # 初始化传入参数  如检查请取消该行注释
# bmm(texts,max_len,dic)  # bmm算法 若想使用fmm，请注释掉该行，并未下一行取消注释
# fmm(texts,max_len,dic)  # 如检查请取消该行注释
