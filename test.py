import jieba
import jieba.posseg as pseg
if __name__ == '__main__':
    sentence = input()
    dict_paths=['warName.txt','itemName.txt','countryName.txt']
    for p in dict_paths:
        jieba.load_userdict(p)
    sentence_seged = pseg.cut(sentence.strip())
    outstr = ''
    for x in sentence_seged:
        outstr+="{}/{},".format(x.word,x.flag)
    print(outstr)
