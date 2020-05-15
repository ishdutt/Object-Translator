from word2word import Word2word

en2fr = Word2word("en","fr")        #French
en2es = Word2word("en","es")        #Spanish
en2it = Word2word("en","it")        #Italian
en2de = Word2word("en","de")        #German
en2ta = Word2word("en","ta")
en2te = Word2word("en","te")


def translate(english_word,caseTranslate):
    print("Yaha Translate.py ka ilaka start hota hai")
    list=english_word.split(" ")
    print(list)
    try:
        if(caseTranslate==1):
            for word in list:
                trans=en2fr(word)[0]
                english_word=english_word.replace(word,trans)
            return english_word

        elif(caseTranslate==2):
            for word in list:
                trans=en2es(word)[0]
                english_word=english_word.replace(word,trans)
            return english_word

        elif(caseTranslate==3):
            for word in list:
                trans=en2it(word)[0]
                english_word=english_word.replace(word,trans)
            return english_word
        
        elif(caseTranslate==4):
            for word in list:
                trans=en2de(word)[0]
                english_word=english_word.replace(word,trans)
            return english_word
        
    except:
        return "It is beyond our scope :("

