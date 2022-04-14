import P3_2
import Handle_number
from time import time

"""
这是实验的第四部分，机械匹配分词的速度优化～
"""


class TriNode:
    """
    Trie树的节点类
    """

    def __init__(self,char='',is_word=False,list_size = 100,):
        self.char = char  # 父节点到该节点路径上的字
        self.child_num = 0  # 该节点的子节点数
        self.child_list = [None] * list_size  # 该节点对应的子节点
        self.is_word = is_word  # 判断根节点到该节点路径上的字是否构成一个词

    def get_keybychar(self, char):
        """
        获取字符char对应的hash值
        :param char: 字符
        :return: hash值
        """
        # TODO 换汉字专用hash函数尝试性能
        return ord(char)%len(self.child_list)

    def insert_child(self,new_child):
        """
        为该节点插入子节点
        :param new_child: 新插入的子节点
        :return: 无
        """
        if self.child_num/ len(self.child_list) > (1/2):
            self.rebuilt_hash()
        index = self.get_keybychar(new_child.char)
        while True:  # 在子节点列表中寻找位置并插入
            if self.child_list[index] is None:
                self.child_list[index] = new_child
                break
            else:
                index = (index + 1) % len(self.child_list)
        self.child_num += 1
        return

    def find_child(self,char):
        """
        根据字符，返回对应子节点（如果有）
        :param char: 字符
        :return: 子节点或NONE
        """
        index = self.get_keybychar(char)
        while True:
            node = self.child_list[index]
            if node is None:
                return None
            elif node.char == char:
                return node
            else:
                index = (index + 1) % len(self.child_list)

    def rebuilt_hash(self):
        """
        当容量不足时 扩大该节点的子hash表为原来的2倍
        :return: 无
        """
        former_list = self.child_list
        self.child_list = [None] * 2 * len(former_list)
        self.child_num = 0
        new_length = len(self.child_list)
        for child_node in former_list:
            if child_node is not None:
                index = self.get_keybychar(child_node.char)
                while True:
                    if self.child_list[index] is None:
                        self.child_list[index] = child_node
                        self.child_num += 1
                        break
                    else:
                        index = (index + 1) % new_length
        return


class TrieDic:
    """
    Trie树的类
    """
    @staticmethod
    def gene_fmm_trie(file_path,encoding = 'utf-8'):
        """
        基于词典为fmm构建trie树
        :param file_path: 词典路径
        :param encoding: 词典编码
        :return: trie树根节点
        """
        file = open(file_path,'r',encoding=encoding)
        word_list = []
        for line in file:
            word_list.append(line.split()[0])
        root = TriNode(list_size=1000)
        for word in word_list:
            TrieDic.fmm_trie_insert(root, word)
        return root

    @staticmethod
    def gene_bmm_trie(file_path,encoding = 'utf-8'):
        """
       基于词典为bmm构建trie树
       :param file_path: 词典路径
       :param encoding: 词典编码
       :return: trie树根节点
       """
        file = open(file_path, 'r', encoding=encoding)
        word_list = []
        for line in file:
            word_list.append(line.split()[0])
        root = TriNode(list_size=1000)
        for word in word_list:
            TrieDic.bmm_trie_insert(root, word)
        return root


    @staticmethod
    def fmm_trie_insert(root,word):
        """
        为fmm trie树插入一个单词
        :param root: 树根节点
        :param word: 单词
        :return: 无
        """
        parent_node = root
        char_index = 0  # 指定词中的字符索引
        char_length = len(word)
        while char_index < char_length:
            this_char = word[char_index]
            if parent_node.find_child(this_char) is not None:
                parent_node = parent_node.find_child(this_char)
            else :
                child_node = TriNode(char=this_char)
                parent_node.insert_child(child_node)
                parent_node = child_node
            char_index += 1
        parent_node.is_word = True
        return

    @staticmethod
    def bmm_trie_insert(root,word):
        """
        为bmm trie树倒序插入一个单词，便于bmm查找
        :param root: 树根节点
        :param word: 单词
        :return: 无
        """
        parent_node = root
        char_length = len(word)
        char_index = char_length -1  # 指定词中的字符索引 倒序处理
        while char_index >= 0:
            this_char = word[char_index]
            if parent_node.find_child(this_char) is not None:
                parent_node = parent_node.find_child(this_char)
            else:
                child_node = TriNode(char=this_char)
                parent_node.insert_child(child_node)
                parent_node = child_node
            char_index -= 1
        parent_node.is_word = True
        return


def optimized_fmm(file_path,write_to_path,trie_root,encoding = 'gbk'):
    """
    使用自实现数据结构trie树的优化前向最大匹配分词算法，对
    文本文件进行分词并将结果写入响应路径
    :param file_path: 需要切分的文本文件的路径
    :param write_to_path: 将切分结果写入的文件位置
    :param trie_root: 词典trie树的根节点
    :return: 无返回
    """
    seged_text = ''
    texts = open(file_path,'r',encoding=encoding).readlines()
    with open (write_to_path, 'w', encoding='utf-8') as seg_file:
        leng = len(texts)
        index = 0
        for this_line in texts:
            index += 1
            texto_write, this_text = '', this_line[:-1]  # 当前行文本长度    5  0-4
            text_len = len(this_text)
            while text_len > 0:
                layer,word_len = 0,1
                buffer = this_text[0]
                child_node = trie_root.find_child(this_text[0])  # 找到第一个字符对应的字节点
                while child_node is not None:
                    layer += 1
                    if child_node.is_word:
                        word_len = layer
                        buffer = this_text[:layer]
                    if layer == len(this_text):
                        break
                    child_node = child_node.find_child(this_text[layer])
                this_text = this_text[word_len:]
                text_len = len(this_text)
                texto_write += buffer +'/ '
            seg_file.write(Handle_number.handle_specond(texto_write) + ('\n' if index != leng else ''))
    return

def optimized_bmm(file_path,write_to_path,trie_root,encoding='gbk'):
    """
    使用自实现数据结构trie树的优化后向最大匹配分词算法，对
    文本文件进行分词并将结果写入响应路径
    :param file_path: 需要切分的文本文件的路径
    :param write_to_path: 将切分结果写入的文件位置
    :param trie_root: 词典trie树的根节点
    :return: 无返回
    """
    seged_text = ''
    texts = open(file_path,'r',encoding=encoding).readlines()
    with open (write_to_path, 'w', encoding='utf-8') as seg_file:
        leng = len(texts)
        index = 0
        for this_line in texts:
            index +=1
            texto_write, this_text = '', this_line[:-1]  # 当前行文本长度    5  0-4
            text_len = len(this_text)
            while text_len > 0:
                layer,word_len = 0,1
                buffer = this_text[text_len -1]
                child_node = trie_root.find_child(this_text[text_len - 1])  # 找到第一个字符对应的字节点
                while child_node is not None:
                    layer += 1
                    if child_node.is_word:
                        word_len = layer
                        buffer = this_text[-1*layer:]
                    if layer == len(this_text):
                        break
                    child_node = child_node.find_child(this_text[text_len - layer - 1])
                this_text = this_text[:-1*word_len]
                text_len = len(this_text)
                texto_write = buffer +'/ '+ texto_write
            seg_file.write(Handle_number.handle_specond(texto_write) + ('\n' if index != leng else ''))
    return

def time_compare(opt_fmm_path,opt_bmm_path,fmm_path,bmm_path,test_path='199801_sent.txt',time_path = 'TimeCost.txt'):
    result = ''
    result += 'FMM:\n'
    texts,max_len,dic = P3_2.init()
    result += '\t时间为'+str(P3_2.fmm_time(texts,max_len,dic))+'s\n'
    result += 'BMM:\n'
    texts, max_len, dic = P3_2.init()
    result += '\t时间为'+str(P3_2.fmm_time(texts, max_len, dic))+'s\n\n'

    trie_root_f = TrieDic.gene_fmm_trie(file_path='dic.txt',encoding='utf-8')
    trie_root_b = TrieDic.gene_bmm_trie(file_path='dic.txt', encoding='utf-8')
    opt_fmm_start = time()
    optimized_fmm(test_path,opt_fmm_path,trie_root_f)
    opt_bmm_start = time()
    optimized_bmm(test_path,opt_bmm_path,trie_root_b)
    end_time = time()
    result += '优化FMM：\n' + '\t时间为'+ str(opt_bmm_start - opt_fmm_start)+'s\n'
    result += '优化BMM：\n' + '\t时间为'+ str(end_time - opt_bmm_start)+'s\n'

    with open(time_path,'w',encoding='utf-8') as time_cost:
        time_cost.write(result)
    return



# file_path = '199801_sent.txt'
# writo_path = 'Scores/seg_FMM.txt'
# trie_root = TrieDic.gene_fmm_trie(file_path='dic.txt',encoding='utf-8')
# optimized_fmm(file_path,writo_path,trie_root)
#
# writo_path = 'Scores/seg_BMM.txt'
# trie_root = TrieDic.gene_bmm_trie(file_path='dic.txt',encoding='utf-8')
# optimized_bmm(file_path,writo_path,trie_root)

# time_compare('1.txt','2.txt','3.txt','4.txt')