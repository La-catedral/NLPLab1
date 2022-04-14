import P3_4
import P3_1


def calc_score(std_seg_path, my_seg_path, std_seg_encoding, my_seg_encoding, k=1):
    std_seg_num, model_seg_num, right_num  = 0, 0, 0
    standard_lines = readseg_tList(std_seg_path, std_seg_encoding)
    my_lines = readseg_tList(my_seg_path, my_seg_encoding)
    for index, this_line in enumerate(standard_lines):
        line_words = this_line.split('/ ')[:-1]  # 取出标准的分词文本中每行的词语
        my_line_words = my_lines[index].split('/ ')[:-1]  # 取对比文本中每行的词语
        std_this_num = len(line_words)   # 该行标准切分词数
        model_this_num = len(my_line_words)   # 该行模型切分词数
        std_seg_num += std_this_num  # 总标准切分数中加入该行的标准切分数
        model_seg_num += model_this_num  # 总模型切分数中加入该行的模型切分数
        i = j = 0
        std_char_num, model_char_num = len(line_words[0]), len(my_line_words[0])
        while i < std_this_num and j < model_this_num:
            if std_char_num == model_char_num:
                right_num += 1
                if i == std_this_num - 1 or j == model_this_num - 1:
                    break
                i += 1
                j += 1
                std_char_num += len(line_words[i])
                model_char_num += len(my_line_words[j])
            else:
                while True:
                    if std_char_num < model_char_num:
                        i += 1
                        std_char_num += len(line_words[i])
                    elif std_char_num > model_char_num:
                        j += 1
                        model_char_num += len(my_line_words[j])
                    else:
                        if i < std_this_num - 1 and j < model_this_num -1:
                            std_char_num += len(line_words[i + 1])
                            model_char_num += len(my_line_words[j + 1])
                        i += 1
                        j += 1
                        break
    precision = right_num / float(model_seg_num)
    recall = right_num / float(std_seg_num)
    f_value = (k * k + 1) * precision * recall / (k * k * precision + recall)
    return precision, recall, f_value


def readseg_tList(seg_path, encoding='utf-8'):
    """
    从给定路径中用给定编码，将所有非空行处理后读入返回的list中
    :param seg_path: 路径
    :param encoding: 编码方式
    :return: 非空行处理后形成的list
    """
    result_list = []  # 保存结果
    with open(seg_path, 'r', encoding=encoding) as file:
        for line in file:
            if line == '\n':
                continue
            handled_line = ''  # 保存处理过后的一行
            for word in line.split():
                handled_line += word[1 if word[0] == '[' else 0:word.index('/')] + '/ '
            result_list.append(handled_line)
    return result_list

def write_ave_score(writo_path, std_encoding='utf-8', model_encoding='utf-8'):

    total_pre, total_recall, total_F = 0, 0, 0
    for i in range(1, 11):
        train_path = 'TrainFiles/train_' + str(i) + '.txt'  # 生成词典的训练样本
        std_path = 'TestFiles/std_' + str(i) + '.txt'  # 标准切分文件
        toseg_path = 'TestFiles/test_' + str(i) + '.txt'  # 待切分文件
        fmm_file = 'fmm_result_' + str(i) + '.txt'  # 将切分结果写入的文件
        dic_path = 'dic_' + str(i) + '.txt'  # 将词典写入的路径
        P3_1.gene_dic(train_path, dic_path, encoding='utf-8')  # 利用该训练集生成词典
        trie_root = P3_4.TrieDic.gene_fmm_trie(dic_path, encoding='utf-8')  # 通过词典生成对应trie树
        P3_4.optimized_fmm(toseg_path, fmm_file, trie_root, encoding='utf-8')  # 获得切分结果
        precision, recall, F = calc_score(std_path, fmm_file, std_encoding, model_encoding)  # FMM
        total_pre += precision
        total_recall += recall
        total_F += F
    score = ''
    score += 'FMM\n'
    # 求均值（*100 /10）
    score += ' 准确率： ' + str(total_pre * 10) + '%\n' + ' 召回率： ' + str(total_recall * 10) + '%\n' + ' F值：' + str(
        total_F * 10) + '%\n\n'

    total_pre, total_recall, total_F = 0, 0, 0
    for i in range(1, 11):
        train_path = 'TrainFiles/train_' + str(i) + '.txt'
        std_path = 'TestFiles/std_' + str(i) + '.txt'  # 标准切分文件
        toseg_path = 'TestFiles/test_' + str(i) + '.txt'
        bmm_file = 'bmm_result_' + str(i) + '.txt'  # 将切分结果写入的文件
        dic_path = 'dic_' + str(i) + '.txt'
        P3_1.gene_dic(train_path, dic_path, encoding='utf-8')  # 利用该训练集生成词典
        trie_root = P3_4.TrieDic.gene_bmm_trie(dic_path, encoding='utf-8')  # 通过词典生成对应trie树
        P3_4.optimized_bmm(toseg_path, bmm_file, trie_root, encoding='utf-8')  # 获得切分结果
        precision, recall, F = calc_score(std_path, bmm_file, std_encoding, model_encoding)  # FMM
        total_pre += precision
        total_recall += recall
        total_F += F
    score += 'BMM\n'
    score += ' 准确率： ' + str(total_pre * 10) + '%\n' + ' 召回率： ' + str(total_recall * 10) + '%\n' + ' F值：' + str(
        total_F * 10) + '%\n\n'
    open(writo_path, 'w', encoding='UTF-8').write(score)

def write_score(std_path = '199801_seg&pos.txt',writo_path='score.txt', std_encoding='gbk', model_encoding='utf-8'):
    precision, recall, F = calc_score(std_path, 'seg_FMM.txt', std_encoding, model_encoding)  # FMM
    score = ''
    score += 'FMM\n'
    # 求均值（*100 /10）
    score += ' 准确率： '+ str(precision*100)+'%\n'+' 召回率： '+str(recall*100)+'%\n'+' F值：'+str(F*100)+'%\n\n'

    precision, recall, F = calc_score(std_path, 'seg_BMM.txt', std_encoding, model_encoding)  # FMM
    score += 'BMM\n'
    score += ' 准确率： '+ str(precision*100)+'%\n'+' 召回率： '+str(recall*100)+'%\n'+' F值：'+str(F*100)+'%\n\n'
    open(writo_path, 'w', encoding='UTF-8').write(score)



#客户端
# write_score()  # 如检查请取消该行注释