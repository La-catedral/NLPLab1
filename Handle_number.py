"""
用于处理带分词语句含有各种格式的连续数字、符号、字母的特殊情况
"""

def handle_specond(seged_sentence):
    """
    处理带分词语句含有各种格式的连续数字(比如学号)、符号、字母的特殊情况，语句已经被分词过
    :return:
    """
    # todo isascii 合适吗 效果
    special_signs = '-./'
    handled_sen = ''
    spec_str = ''
    # special_signs = '-@#$%&/._\''
    words = seged_sentence.split('/ ')[:-1]
    for index, word in enumerate(words):
        if word.isascii() or word in special_signs:  # 若是字母、数字或者英文标点
            spec_str += word
            if index + 1 == len(words):
                handled_sen += spec_str + '/ '
        else:
            if spec_str:
                handled_sen += spec_str + '/ '
                spec_str = ''
            handled_sen += word + '/ '
    return handled_sen