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
#        self.words = RE_WORD.findall(text) def __repr__(self):
#        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
#        for word in self.words:
#            yield word
#        return
        return (match.group() for match in RE_WORD.finditer(self.text))


a = Sentence(s)

for i in a:
    print(i)

# generator function
def gen_AB():
    print('Start')
    yield 'A'
    print('Continue')
    yield 'B'
    print('End')
    yield 'C'

#for i in gen_AB():
#    print(i)
print('----------------------')
res1 = [x*3 for x in gen_AB()]
print(res1)


print('-------------------')

# generator expression
res2 = (x*3 for x in gen_AB())  # res2 is a generator object
print(res2)


import itertools

a = itertools.count(1,.5)
gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))




# itertools
## compress
def vowel(c):
    return c.lower() in 'aeiou'   # True False seqs
l1 = list(filter(vowel, 'Aardvark'))
print(l1)
l2 = list(itertools.filterfalse(vowel, 'Aardvark'))
print(l2)
l3 = list(itertools.dropwhile(vowel, 'Axardvark'))
print(l3)
l4 = list(itertools.takewhile(vowel, 'Axardvark'))
print(l4)
l5 = list(itertools.compress('Aardvark', (1,0,1,1,0,0,0,0,1)))
print(l5)
list(itertools.islice('Aardvark', 4))
list(itertools.islice('Aardvark', 4, 7))
list(itertools.islice('Aardvark', 1, 7, 2))

## accumulate
sample=[5,4,2,8,7,6,3,0,9,1]
x1 = list(itertools.accumulate(sample))
print(x1)
list(itertools.accumulate(sample, min))
list(itertools.accumulate(sample, max))
import operator
x2 = list(itertools.accumulate(sample, operator.mul))
print(x2)

x3 = list(itertools.accumulate(range(1, 11), operator.mul))
print(x3)

x4 = list(enumerate('albatroz', 102))
print(x4)

x5 = list(map(operator.mul, range(5), range(3)))
print(x5)

x6 = list(map(operator.mul, range(11), [2, 4, 8]))
print(x6)

x7 = list(map(lambda a, b: (a, b), range(11), [2, 4, 8]))
print(x7)

x8 = map(lambda a, b: (a, b), [1,1,1], [2, 4, 8])
print(x8)

x9 = list(itertools.starmap(operator.mul, enumerate('albatroz', 1)))
print(x9)

x10 = list(itertools.starmap(lambda a, b: b/a,enumerate(itertools.accumulate(sample), 1)))
print(x10)

x11 = list(itertools.chain('effgg',range(10)))
print(x11)

x12 = list(itertools.chain(enumerate('ABC')))
print(x12)

x13 = list(itertools.chain.from_iterable(enumerate('ABC')))
print(x13)

x14 = list(itertools.zip_longest('ABC', range(5)))
print(x14)

x15 = list(itertools.zip_longest('ABC', range(5), fillvalue='?'))
print(x15)

x16 = list(itertools.product('ABC', range(2)))
print(x16)

x17 = list(itertools.product('ABC', repeat=2))
print(x17)


for char, group in itertools.groupby(['A','A','B','B','A','C','C']):
    print(char, '->', list(group))

animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear','bat', 'dolphin', 'shark', 'lion']
animals.sort(key=len)
print(animals)


for length, group in itertools.groupby(animals, len):
    print(length, '->', list(group))

for length, group in itertools.groupby(reversed(animals), len):
    print(length, '->', list(group))

g1, g2 = itertools.tee('ABC')
list(zip(*itertools.tee('ABC')))


## dropwhile
## filter(built in)
## filterfalse
## islice
## takewhile


## yield from

def chain(*iterables):
    for i in iterables:
        yield from i
s = 'ABC'
t = tuple(range(3))

r = chain(s,t)
print(list(r))


g=(n for n in[0,0.0,7,8])
print(any(g))
print(next(g))



















