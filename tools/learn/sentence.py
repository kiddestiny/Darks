import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self,text):
        self.text = text
        self.words = RE_WORD.findall(text)
    def __getitem__(self, index):
        return self.words[index]
#    def __iter__(self):
#        return self.words  
    def __len__(self):
        return len(self.words)
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

if __name__ == '__main__':
    a = Sentence('hejlfej jwef jkj jekl flwe jfk ekf klwj eflkj wkle fw ef')
    for i in a:
        print(i)
