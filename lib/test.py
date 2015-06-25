# -*- coding: utf-8 -*-
import regexlib



class Test(object):
    def __init__(self):
        return

    def run(self):
        text = '''
        "I'm sorry to say I do," echoed the white-mustached man facing him in the bright 
        high-up skyscraper office, and contemplating him gravely at the same time through 
        round owl-like tortoise-shell eyeglasses. "For you've just read his will-or the carbon 
        copy of it. With which at least, Boyce, I can say I had nothing to do. It was my partner 
        who actually drew it up-for, like yourself, I've been out of town for a week, you know-though 
        even he tried to argue your grandfather out of it-but to no avail."
        '''
        text = regexlib.replaceSub(text,"#'#",u'#’#')
        print text
        print("\nAll done!")