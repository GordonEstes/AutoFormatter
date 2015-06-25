import string
import sys
sys.path.insert(0,"/Users/Gordon/Gordon's Files/AutoFormatter/lib")
import filelib, listlib, regexlib, doclib

text = "THE lawyer regarded Boyce with a half-amused, half-pained expression on his face. Then, taking off his round tortoise-shell eyeglasses, and fastening them on his thumb, he half shook his head."

if len(text) >= 2:
    print("Step 1")
    if text[1] in string.ascii_uppercase:
        print("Step 2")
        s = text
        for i in xrange(1,len(s)):
            print s[i]
            if s[i] in string.ascii_lowercase: break
            if s[i] in string.ascii_uppercase:
                print("Step 3")
                s = regexlib.replaceIndex(s,i,string.lower(s[i]))
        text = s

print text