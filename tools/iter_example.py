from collections import abc
import re
import reprlib

RE_WORD = re.compile('\w+')
s = 'have a nice day'

# for i in s:
#     print(i)


# class Foo:
#     '''
#     实现了iter内置方法
#     '''
#     def __iter__(self):
#         pass

# class Bar:
#     '''
#     '''
#     def __getitem__(self):
#         pass

# class Sentence:
#     def __init__(self, text): 
#         self.text = text
#         self.words = RE_WORD.findall(text) 
#     def __getitem__(self, index):
#         return self.words[index] 
#     def __len__(self):
#         return len(self.words) 
#     def __repr__(self):
#         return 'Sentence(%s)' % reprlib.repr(self.text)
# a = Foo()
# b = Bar()
# c = Sentence(s)

# print(issubclass(Foo, abc.Iterable))
# print(isinstance(a, abc.Iterable))



# print(issubclass(Bar, abc.Iterable))
# print(isinstance(b, abc.Iterable))
# print(issubclass(Sentence, abc.Iterable))
# print(isinstance(c, abc.Iterable))

# print(iter(s))
# #iter(a)
# print(iter(b))
# print(iter(c))



# # iterator
# S = 'ABC'

# for char in S:
#     print(char)

# s = iter(S)
# while True:
#     try:
#         print(next(s))
#     except StopIteration:
#         del s
#         break


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text) 
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
        for word in self.words:
            yield word
        return

a = Sentence(s)
for i in a:
    print(i)
    
    
















