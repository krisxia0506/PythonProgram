input_str = input()  # 获取输入字符串

output_str = ""  # 初始化输出字符串
is_first_word = True  # 是否为句子的第一个单词
for i in range(len(input_str)):
    c = input_str[i]  # 获取当前字符
    if c.isalpha():  # 如果当前字符是字母
        if is_first_word:  # 如果当前单词是句子的第一个单词
            output_str += c.upper()  # 将当前字母转为大写
            is_first_word = False
        elif c.lower() == 'i' and (i == len(input_str) - 1 or not input_str[i + 1].isalpha()):  # 如果当前字母是 i 且两侧均为空格或标点
            output_str += 'I'  # 将 i 转为大写的 I
        else:
            output_str += c.lower()  # 将当前字母转为小写
    else:  # 如果当前字符不是字母
        output_str += c  # 直接将当前字符添加到输出字符串中
        if c == '.':  # 如果当前字符是句号，下一个单词是新句子的第一个单词
            is_first_word = True

print(output_str)
