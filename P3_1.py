def get_train_test():
    """
    生成十折交叉验证的十个训练集和对应测试集合
    :return:
    """
    train_one = open('TrainFiles/train_1.txt','w',encoding='utf-8')
    train_two = open('TrainFiles/train_2.txt','w',encoding='utf-8')
    train_thr = open('TrainFiles/train_3.txt','w',encoding='utf-8')
    train_four = open('TrainFiles/train_4.txt','w',encoding='utf-8')
    train_five = open('TrainFiles/train_5.txt','w',encoding='utf-8')
    train_six = open('TrainFiles/train_6.txt','w',encoding='utf-8')
    train_sev = open('TrainFiles/train_7.txt','w',encoding='utf-8')
    train_eig = open('TrainFiles/train_8.txt','w',encoding='utf-8')
    train_nin = open('TrainFiles/train_9.txt','w',encoding='utf-8')
    train_ten = open('TrainFiles/train_10.txt','w',encoding='utf-8')
    test_one = open('TestFiles/test_1.txt','w',encoding='utf-8')
    test_two = open('TestFiles/test_2.txt', 'w', encoding='utf-8')
    test_thr = open('TestFiles/test_3.txt', 'w', encoding='utf-8')
    test_four = open('TestFiles/test_4.txt', 'w', encoding='utf-8')
    test_five = open('TestFiles/test_5.txt', 'w', encoding='utf-8')
    test_six = open('TestFiles/test_6.txt', 'w', encoding='utf-8')
    test_sev = open('TestFiles/test_7.txt', 'w', encoding='utf-8')
    test_eig = open('TestFiles/test_8.txt', 'w', encoding='utf-8')
    test_nin = open('TestFiles/test_9.txt', 'w', encoding='utf-8')
    test_ten = open('TestFiles/test_10.txt', 'w', encoding='utf-8')
    std_one = open('TestFiles/std_1.txt', 'w', encoding='utf-8')
    std_two = open('TestFiles/std_2.txt', 'w', encoding='utf-8')
    std_thr = open('TestFiles/std_3.txt', 'w', encoding='utf-8')
    std_four = open('TestFiles/std_4.txt', 'w', encoding='utf-8')
    std_five = open('TestFiles/std_5.txt', 'w', encoding='utf-8')
    std_six = open('TestFiles/std_6.txt', 'w', encoding='utf-8')
    std_sev = open('TestFiles/std_7.txt', 'w', encoding='utf-8')
    std_eig = open('TestFiles/std_8.txt', 'w', encoding='utf-8')
    std_nin = open('TestFiles/std_9.txt', 'w', encoding='utf-8')
    std_ten = open('TestFiles/std_10.txt', 'w', encoding='utf-8')

    with open('199801_seg&pos.txt','r',encoding='gbk') as train_file:
        with open('199801_sent.txt','r',encoding='gbk') as test_file:
            test_lines = test_file.readlines()
            i = 0
            for line in train_file:
                if i % 10 == 1:
                    test_one.write(test_lines[i])
                    std_one.write(line)
                else:
                    train_one.write(line)
                if i % 10 == 2:
                    test_two.write(test_lines[i])
                    std_two.write(line)
                else:
                    train_two.write(line)
                if i % 10 == 3:
                    test_thr.write(test_lines[i])
                    std_thr.write(line)
                else:
                    train_thr.write(line)
                if i % 10 == 4:
                    test_four.write(test_lines[i])
                    std_four.write(line)
                else:
                    train_four.write(line)
                if i % 10 == 5:
                    test_five.write(test_lines[i])
                    std_five.write(line)
                else:
                    train_five.write(line)
                if i % 10 == 6:
                    test_six.write(test_lines[i])
                    std_six.write(line)
                else:
                    train_six.write(line)
                if i % 10 == 7:
                    test_sev.write(test_lines[i])
                    std_sev.write(line)
                else:
                    train_sev.write(line)
                if i % 10 == 8:
                    test_eig.write(test_lines[i])
                    std_eig.write(line)
                else:
                    train_eig.write(line)
                if i % 10 == 9:
                    test_nin.write(test_lines[i])
                    std_nin.write(line)
                else:
                    train_nin.write(line)
                if i % 10 == 0:
                    test_ten.write(test_lines[i])
                    std_ten.write(line)
                else:
                    train_ten.write(line)
                i += 1
    return




def gene_dic(from_file = '199801_seg&pos.txt',writo_path = 'dic.txt',encoding='gbk'):
    """
    利用给定文本生成词典
    :param from_file:
    :return:
    """
    f = open(from_file,encoding=encoding)
    lines = f.readlines()
    f.close()

    word_dic = set()  # 在不需要统计词频时，以集合的形式存储，避免出现重复的词
    max_length = 0  # 词长度最大值
    for line in lines:
        for word in line.split():
            if '/m' in word and '-' in word:  # 去掉对应格式的日期
                continue
            if '/w' in word:
                continue
            if word[0] == '[':  # 去除专有名词中夹杂的'['符号
                word = word[1:word.index('/')]
            else:
                word = word[0:word.index('/')]
            word_length = len(word)
            if word_length > max_length:  # 更新最大长度
                max_length = word_length
            word_dic.add(word)
    # 转化为列表 更容易
    word_list = list(word_dic)
    word_list.sort()
    # 生成词典'dic.txt'
    dic_file = open(writo_path,'w',encoding = 'utf-8')
    dic_file.write('\n'.join(word_list))
    dic_file.close()

    return max_length, word_dic

# get_train_test()





# 客户端
# max_Length,word_dic = gene_dic(from_file='TrainFiles/train_1.txt',encoding='utf-8')
# print("the max length of the word is :"+ str(max_Length))
# print(len(word_dic))  # 如检查请取消这三行注释
