import os, re

class concatMatcher():
    def __init__(self, words):
        self.regex = re.compile('|'.join(words))
        self.num_of_words = len(set(words))
        self.word_len = len(words[0])

    # returns the starting index of the match, -1 if no match
    def match(self, blob, pos, found):
        m = self.regex.match( blob[ pos : pos+self.word_len ] )
        if not m or m.group(0) in found:
            return False
        else:
            found.add(m.group(0))
            return True if len(found) == self.num_of_words \
                        else self.match(blob, pos+m.end(), found)

def ourfind(searchexp, blob):
    matcher = concatMatcher( searchexp.split(' ') )
    for i in range(len(blob)):
        if matcher.match(blob, i, found=set() ):
            return i
    return -1

def outfile_dump(out_f):
    with open(out_f) as ff:
        return ff.read()

if __name__ == '__main__':
    ins_outs_fs = [("input0%d.txt" % i, "output0%d.txt" % i) for i in range(5+1) ]

    for i, o in ins_outs_fs:
        with open(i) as ff:
            testf = ff.read().split('\n')
            result = ourfind( testf[0]   # first line: input words 
                            , testf[1] ) # second line: search blob
        print "result: %d; expected result: %s;" % (result, outfile_dump(o))
