import math
import Handle_number
import P3_3

"""
一元文法分词
"""

def dic_for_uni(file_path,writo_path,encoding):
    """
    生成含词频的词典txt文件
    :param file_path: 用于生成词典的训练文本
    :param writo_path: 将词典写入的文件路径
    :param encoding: 训练文本文件的编码方式
    :return: 无
    """
    txt_file = open(file_path,'r',encoding=encoding)  # todo encoding
    word_dic = {}
    max_length = 0  # 词长度最大值
    for line in txt_file:
        for word in line.split():
            if word[0] == '[':  # 去除专有名词中夹杂的'['符号
                word = word[1:word.index('/')]
            else:
                word = word[0:word.index('/')]
            word_length = len(word)
            if word_length > max_length:  # 更新最大长度
                max_length = word_length
            if word in word_dic.keys():
                word_dic[word] += 1
            else:
                word_dic[word] = 1

    # 转化为列表 更容易
    word_list = list(word_dic.keys())
    word_list.sort()
    dic_to_write = ''
    for key_word in word_list:
        dic_to_write = dic_to_write + key_word + ' ' + str(word_dic[key_word]) + '\n'
    dic_to_write = dic_to_write[:-1]  # 去掉最后一个换行符
    dic = open(writo_path,'w',encoding='utf-8')
    dic.write(dic_to_write)
    dic.close()
    return



def gene_pref_dic(dic_path):
    """
    通过含词频的词典生成前缀词典
    :return:
    """
    pref_dic = {}  # 关于(词，词频)的前缀词典
    total_num = 0  # 总词数
    file = open(dic_path,'r')  # TODO encoding?
    for line in file:
        this_word,this_freq = line.split()[0:2]
        this_freq = int(this_freq)
        pref_dic[this_word] = this_freq
        total_num += this_freq
        for pre_len in range(len(this_word)):
            pref = this_word[0:pre_len+1]
            if pref not in pref_dic.keys():
                pref_dic[pref] = 0
    file.close()
    return pref_dic, total_num


def gene_DAG(this_senten,pre_dic):
    """
    给定前缀词典和该句子,生成该句子的有向无环图
    :param this_senten:用于生成DAG的句子
    :param pre_dic:前缀词典
    :return:
    """
    DAG = {}
    leng = len(this_senten)
    for i in range(leng):
        temp_l = []
        frag = this_senten[i]  # 句子中的第i个字
        j = i
        while j < leng and frag in pre_dic:
            if pre_dic[frag] > 0:
                temp_l.append(j)
            j += 1
            frag = this_senten[i:j+1]
        if not temp_l:
            temp_l.append(i)
        DAG[i] = temp_l
    return DAG


def calc_route(sentence,pre_dic,total_num):
    DAG = gene_DAG(sentence,pre_dic=pre_dic)
    leng = len(sentence)
    log_total = math.log(total_num)  # 总词频的对数
    route = {leng: (0,0)}
    for index in range(leng -1,-1,-1):
        route[index] = max((math.log( pre_dic.get(sentence[index:x+1],0) or 1) - math.log(total_num) + route[x+1][0],x) for x in DAG[index] )
        # 存储的是序对 （概率的对数值,结束位置）
    return route

def uni_gram(txt_path,dic_path,write_tpa,encoding='utf-8'):
    """
    输入含词频词典文件的路径，利用其对给定文本进行分词并写入给定文件
    :param txt_path: 需要被分词的文本
    :param dic_path: 词典文件路径
    :return: 无
    """
    text = open(txt_path, 'r',encoding=encoding).readlines()
    dic, total_num = gene_pref_dic(dic_path)  # 由给定词典生成前缀词典并计算词频
    writo_file  = open(write_tpa,'w',encoding='utf-8')
    leng = len(text)
    index = 0
    for line in text:
        index += 1
        sentence = line[:-1]
        senten_route = calc_route(sentence,dic,total_num)
        sentence_seg = ''  # 用于存储分词结果
        fr_index = 0
        while fr_index < len(sentence):
            to_index = senten_route[fr_index][1] + 1
            sentence_seg += sentence[fr_index:to_index] + '/ '
            fr_index = to_index
        writo_file.write(Handle_number.handle_specond(sentence_seg)+('\n' if index != leng else ''))
    return


def get_score(writo_path = 'Scores/uni_score.txt', std_encoding='utf-8', model_encoding='utf-8'):
        total_pre, total_recall, total_F = 0, 0, 0
        for i in range(1, 11):
            train_path = 'TrainFiles/train_' + str(i) + '.txt'
            std_path = 'TestFiles/std_' + str(i) + '.txt'  # 标准切分文件
            toseg_path = 'TestFiles/test_' + str(i) + '.txt'
            uni_file = 'Uniresults/uni_result_' + str(i) + '.txt'  # 将切分结果写入的文件
            dic_path = 'Unidics/uni_dic_' + str(i) + '.txt'
            dic_for_uni(train_path, dic_path, encoding='utf-8')
            uni_gram(toseg_path, dic_path, uni_file)
            precision, recall, F = P3_3.calc_score(std_path, uni_file, std_encoding, model_encoding)  # FMM
            total_pre += precision
            total_recall += recall
            total_F += F
        score = ''
        score += 'uni_gram:\n'
        score += ' 准确率： ' + str(total_pre * 10) + '%\n' + ' 召回率： ' + str(total_recall * 10) + '%\n' + ' F值：' + str(
            total_F * 10) + '%\n\n'
        open(writo_path, 'w', encoding='UTF-8').write(score)


# 客户端
# get_score(std_encoding='utf-8', model_encoding='utf-8')

# 如果进行最后一部分的分词性能评估请取消下面几行注释
# dic_path = 'Unidics/uni_dic.txt'
# toseg_path = input('请输入测试文件路径')
# encod = input('请输入待切分文件编码方式')
# uni_file = 'seg_LM.txt'
# dic_for_uni('199801_seg&pos.txt', dic_path, encoding='utf-8')
# uni_gram(toseg_path, dic_path, uni_file,encoding=encod)