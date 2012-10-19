# Solve this

----

# The Problem

> You are given a list of words, L, that are all of the same length, and a string, S. Find a substring in S such that it is formed by concatenating each word in L exactly once and without any intervening characters. You are guaranteed that such substring will occur exactly once in S.

## Example Input:

    aba bab abb bba
    bbabbababbaabbbabbb

## Example Output:

    5

## So:
    
<tt>bbabb**aba**:**bba**:**abb**:**bab**bb</tt>

---


# Brute force

## handle reading files and comparing the output:

    !python
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

## then do the find with `ourfind`

    !python
    def ourfind(searchexp, blob):
        for pattern in itertools.permutations(searchexp.split(' ')):
            find_str = ''.join(pattern)
            idex = find(find_str, blob)
            if idex >= 0:
                return idex
---
# That takes a long while

So don't do that. There's a linear solution.

---
# Solution

Our lives are easier thanks to recursion and regular expressions.

    !python
    def match(searchexp, blob):
        words = searchexp.split(' ')
        regex = re.compile('|'.join(words))
        m = regex.match( blob )
        if not m:
            return -1
        else:
            return m.start()

---
# Fleshed out a bit more

    !python
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
                if len(found) == self.num_of_words:
                    return True
                else:
                    return self.match(blob, pos+m.end(), found)

    def ourfind(searchexp, blob):
        matcher = concatMatcher( searchexp.split(' ') )
        for i in range(len(blob)):
            if matcher.match(blob, i, found=set() ):
                return i
        return -1