import os
import re
import sys

file_dir = r"E:\Grade 15  2019\Python课\2019.12.22\test2\dist"


def find():
    while(1):
        voca = input()
        num = 0
        for filename in os.listdir(file_dir):
            if filename.endswith('.txt'):
                with open(filename, 'r', encoding='utf-8') as file:
                    comment_piece = file.readlines()
                    for j in range(len(comment_piece)):
                        flag = re.findall(r'(' + voca + ')', comment_piece[j])
                        if len(flag) != 0:
                            print(comment_piece[j])
                            num = num + 1
        print(num)
        os.system("pause")


find()
