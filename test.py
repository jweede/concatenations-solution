import os, re, itertools

def concat_test(fn):
    with open(fn) as ff:
        testf = ff.readlines()
        #print testf
        return triefind(testf[0][:-1], testf[1][:-1])

def triefind(searchexp, blob):
    words = searchexp.split(' ')
    t = Trie()
    for w in words:
        t.add_word(w, w)
    t.make_automaton()
    matches = 0
    for i in range(len(blob)):
        if t.match(blob[i:]):
            matches += 1 
    return matches


# def ourfind(searchexp, blob):
#     #l = searchexp[:-1].split(' ')
#     #ol = searchexp[:-1].split(' ')
#     blob = blob[:-1]

#     def match_rest(pos, words):
#         #base case - match
#         if len(words) == 0:
#             return True
#         else:
#             m = re.match( '|'.join( words )
#                          , blob[pos:]
#                          )
#             if m:
#                 #print m.group(0), pos+m.end()
#                 words.remove( m.group(0) )
#                 #print words
#                 return match_rest( pos+m.end()
#                                  , words
#                                  )
#             #base case - no match
#             else:
#                 return False
#     matches = 0
#     for i in range(len(blob)):
#         if match_rest(i, searchexp[:-1].split(' ') ):
#             matches += 1

#     return matches

def outfile_dump(out_f):
    with open(out_f) as ff:
        return ff.read()[:-1]

nil = object()  # used to distinguish from None

class TrieNode(object):
    __slots__ = ['char', 'output', 'fail', 'children']
    def __init__(self, char):
        self.char = char
        self.output = nil
        self.fail = nil
        self.children = {}

    def __repr__(self):
        if self.output is not nil:
            return "<TrieNode '%s' '%s'>" % (self.char, self.output)
        else:
            return "<TrieNode '%s'>" % self.char


class Trie(object):
    def __init__(self):
        self.root = TrieNode('')


    def __get_node(self, word):
        node = self.root
        for c in word:
            try:
                node = node.children[c]
            except KeyError:
                return None

        return node


    def get(self, word, default=nil):
        node = self.__get_node(word)
        output = nil
        if node:
            output = node.output

        if output is nil:
            if default is nil:
                raise KeyError("no key '%s'" % word)
            else:
                return default
        else:
            return output


    def keys(self):
        for key, _ in self.items():
            yield key


    def values(self):
        for _, value in self.items():
            yield value

    
    def items(self):
        L = []
        def aux(node, s):
            s = s + node.char
            if node.output is not nil:
                L.append((s, node.output))

            for child in node.children.values():
                if child is not node:
                    aux(child, s)

        aux(self.root, '')
        return iter(L)

    
    def __len__(self):
        stack = [self.root]
        n = 0
        while stack:
            n += 1
            node = stack.pop()
            for child in node.children.values():
                stack.append(child)

        return n


    def add_word(self, word, value):
        if not word:
            return

        node = self.root
        for i, c in enumerate(word):
            try:
                node = node.children[c]
            except KeyError:
                n = TrieNode(c)
                node.children[c] = n
                node = n

        node.output = value


    def clear(self):
        self.root = TrieNode('')


    def exists(self, word):
        node = self.__get_node(word)
        if node:
            return bool(node.output != nil)
        else:
            return False


    def match(self, word):
        return (self.__get_node(word) is not None)
        

    def make_automaton(self):
        queue = []

        # 1.
        for i in range(256):
            c = chr(i)
            if c in self.root.children:
                node = self.root.children[c]
                node.fail = self.root   # f(s) = 0
                queue.append(node)
            else:
                self.root.children[c] = self.root

        # 2.
        while queue:
            r = queue.pop(0);
            for node in r.children.values():
                queue.append(node)
                state = r.fail
                while node.char not in state.children:
                        state = state.fail

                node.fail = state.children.get(node.char, self.root)


    def find_all(self, string, callback, start=None, end=None):
        for index, output in self.iter():
            callback(index, output)


    def iter(self, string, start=None, end=None):
        start = start if start is not None else 0
        end = end if end is not None else len(string)

        state = self.root
        for index, c in enumerate(string[start:end]):
            while c not in state.children:
                state = state.fail

            state = state.children.get(c, self.root)

            tmp = state
            output = []
            while tmp is not nil and tmp.output is not nil:
                output.append(tmp.output)
                tmp = tmp.fail

            if output:
                yield (index + start, output)

if __name__ == '__main__':
    ins_outs_f = [("input0%d.txt" % i, "output0%d.txt" % i) for i in range(2+1) ]

    for i, o in ins_outs_f:
        match_count = concat_test( i )
        print match_count, outfile_dump(o)
