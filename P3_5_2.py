import math
from P3_5_1 import *
import Handle_number

bi_dic = {}

def gene_bi_dic(txt_path,writo_path,encoding='utf-8'):
    """
    从给定文本中生成二元模型适用的词典
    :param txt_path: 给定的用于生成词典的文本
    :param writo_path: 生成词典后将词典写入的路径
    :return: 二元文法使用的词典bi_dic,格式为{former_word:{latterword:freq},...}
    """
    global bi_dic
    txt_file = open(txt_path, 'r',encoding=encoding)  # 读取先前生成的训练文件
    word_dic = {}
    for line in txt_file:
        if line == '\n':
            continue
        words = line[:-1].split()  # 该行文本切分为词序列
        words.append('EOS/ ')
        words.insert(0,'BOS')
        for index in range(1,len(words)):
            words[index] = words[index][1 if words[index][0] == '[' else 0:words[index].index('/')]
            if words[index -1] not in word_dic.keys():
                word_dic[ words[index -1] ] = {}  # 为前一个词创建一个字典映射
            if words[index] not in word_dic[words[index-1]].keys():
                word_dic[words[index -1]][words[index]] = 0
            word_dic[words[index - 1]][words[index]] += 1
    writo_file = open(writo_path,'w',encoding='utf-8')
    for key_word in word_dic:
        for latter_word in word_dic[key_word]:
            writo_file.write(key_word+' '+latter_word+' '+ str(word_dic[key_word][latter_word]) + '\n')
    return


def get_bidic(dic_path):
    """
    从二元词典中把信息读取出来
    :param dic_path: 二元词典
    :return: 生成的在线词典
    """""
    global bi_dic
    dic_file = open(dic_path,'r',encoding='utf-8')  # encoding
    for this_bgr in dic_file:
        former_w,latter_w,freq = this_bgr.split()[0:3]
        if latter_w not in bi_dic.keys():
            bi_dic[latter_w] = {}
        bi_dic[latter_w][former_w] = int(freq)
    return bi_dic

def calc_log_p(former_w,latter_w,pref_dic,bi_dic):
    """
    计算组合概率并取对数
    :param former_w:前面的词
    :param latter_w:第二个词
    :param pref_dic: 由part 5-1生成的前缀词典 其中含有词频
    :param bi_dic:前面生成的二元词典
    :return:组合概率的对数值
    """
    latter_set = bi_dic.get(former_w,{})
    ftol_freq = latter_set.get(latter_w,0)
    former_freq = pref_dic.get(former_w,0)  # 前一个词的总出现次数
    leng = len(pref_dic.keys())
    return math.log(ftol_freq + 1) - math.log(former_freq + leng)


def calc_route(sentence,DAG,pre_dic,bi_dic):
    """
    利用该句生成的DAG，计算路径
    :param sentence:
    :param DAG:该句对应的DAG
    :return:
    """

    final_index = len(sentence) - 3  # 减去<EOS>的长度
    start_index = 3  # 跳过<BOS>从第一个字开始
    pre_graph = {'BOS': {}}  # 关键字为前词，值为对应的词和对数概率
    word_graph = {}  # 每个词节点存有上一个相连词的词图
    for x in DAG[3]:  # 初始化前词为BOS的情况
        pre_graph['BOS'][(3, x + 1)] = calc_log_p('BOS', sentence[3:x + 1],pre_dic,bi_dic)
    while start_index < final_index:  # 对每一个字可能的词生成下一个词的词典
        for index in DAG[start_index]:  # 遍历dag[start]中的每一个结束节点
            pre_word = sentence[start_index:index + 1]  # 这个词是前一个词比如，'去北京'中的去
            temp = {}
            for next_end in DAG[index + 1]:
                last_word = sentence[index + 1:next_end + 1]
                if sentence[index + 1:next_end + 3] == 'EOS':  # 判断是否到达末尾
                    temp['EOS'] = calc_log_p(pre_word, 'EOS',pre_dic,bi_dic)
                else:
                    temp[(index + 1, next_end + 1)] = calc_log_p(pre_word, last_word,pre_dic,bi_dic)
            pre_graph[(start_index, index + 1)] = temp  # 每一个以start开始的词都建立一个关于下一个词的词典
        start_index += 1
    pre_words = list(pre_graph.keys())  # 表示所有的前面的一个词
    for pre_word in pre_words:  # word_graph表示关键字对应的值为关键字的前词列表
        for word in pre_graph[pre_word].keys():  # 遍历pre_word词的后一个词word
            word_graph[word] = word_graph.get(word, list())
            word_graph[word].append(pre_word)
    pre_words.append('EOS')
    route = {}
    for word in pre_words:
        if word == 'BOS':
            route[word] = (0.0, 'BOS')
        else:
            pre_list = word_graph.get(word, list())  # 取得该词对应的前词列表
            route[word] = (-65507, 'BOS') if not pre_list else max(
                (pre_graph[pre][word] + route[pre][0], pre) for pre in pre_list)
    return route


def bi_gram(file_path,writo_path,unidic_path,bidic_path,encoding):
    """

    :param file_path:
    :param writo_path:
    :param dic_path: 带词频词典的路径
    :return:
    """
    file = open(file_path,'r',encoding=encoding).readlines() # todo encoding
    writo_file = open(writo_path,'w',encoding='utf-8')
    pre_dic ,total_num = gene_pref_dic(unidic_path)
    bi_dic = get_bidic(bidic_path)
    for line in file:
        line = 'BOS' + line[:-1] + 'EOS'
        DAG = gene_DAG(line,pre_dic)
        route = calc_route(line,DAG,pre_dic,bi_dic)
        seg_line = ''
        position = 'EOS'
        while True:
            position = route[position][1]
            if position == 'BOS':
                break
            seg_line = line[position[0]:position[1]] + '/ ' + seg_line
        writo_file.write(Handle_number.handle_specond(seg_line) + '\n')  # 写入分词文件中
    return


def get_score(writo_path='Scores/bi_score.txt', std_encoding='utf-8', model_encoding='utf-8'):

    # score = ''
    # score += 'bi_gram:\n'
    # score += ' 准确率： ' + str(precision * 100) + '%\n' + ' 召回率： ' + str(recall * 100) + '%\n' + ' F值：' + str(
    #     F * 100) + '%\n\n'
    # open(writo_path, 'w', encoding='UTF-8').write(score)

    total_pre, total_recall, total_F = 0, 0, 0
    for i in range(1, 11):
        train_path = 'TrainFiles/train_' + str(i) + '.txt'
        std_path = 'TestFiles/std_' + str(i) + '.txt'  # 标准切分文件
        toseg_path = 'TestFiles/test_' + str(i) + '.txt'  # 待切分文件
        uni_dic_path = 'Unidics/uni_dic_' + str(i) + '.txt'  # 词频词典
        bi_file = 'Biresults/bi_result_' + str(i) + '.txt'  # 将切分结果写入的文件
        dic_path = 'Bidics/bi_dic_' + str(i) + '.txt'  # 二元文法词典
        gene_bi_dic(train_path,dic_path)  # 获取二元文法词典

        bi_gram(toseg_path, bi_file, uni_dic_path, dic_path, encoding='utf-8')
        precision, recall, F = P3_3.calc_score(std_path, bi_file, std_encoding,
                                               model_encoding)  # FMM
        total_pre += precision
        total_recall += recall
        total_F += F
    score = ''
    score += 'bi_gram:\n'
    score += ' 准确率： ' + str(total_pre * 10) + '%\n' + ' 召回率： ' + str(total_recall * 10) + '%\n' + ' F值：' + str(
        total_F * 10) + '%\n\n'
    open(writo_path, 'w', encoding='UTF-8').write(score)
    return

get_score()



