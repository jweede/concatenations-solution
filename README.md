You might run into this question in a coding interview. I finally took and afternoon to think it through and solve it properly.

I think the prompt goes something like: 

> You are given a list of words, L, that are all of the same length, and a string, S. Find a substring in S such that it is formed by concatenating each word in L exactly once and without any intervening characters. You are guaranteed that such substring will occur exactly once in S.

So I made a simple solution that uses a regex of the form `"word1|word2|word3..."` to search for a phrase, a hashed set of found words, and a simple recursive function `match` to ensure that the matches are consecutive and unique.

Just run `python test.py` and it'll pull in and run the testcases