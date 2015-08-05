"""
The code requires different python packages to be installed before runnig these code
these packages can be found on http://www.lfd.uci.edu/~gohlke/pythonlibs/
"""

import re
import numpy as np
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier  
stemmer=SnowballStemmer("english")
stopwords_list=stopwords.words("english")

vocab={}
"""These are lists used for maintaining various features such as number of scores ,dates ,hashtag and average length of the tweets """

countwordlist=[]
avglenlist=[]
countyears=[]
counthttps=[]
countdates=[]
countnums=[]
countscores=[]
counthashtag=[]
countattherate=[]


    

def getwords(word):
    #This function breaks compount words in their constituent words
    start=0
    wordlist=[]
    count=0
    length=len(word)
    prev_upper=False
    prev_digit=False
    prev_alnum=True
    upper_streak=False
    lower_streak=False
    temp=""
    isfirst=True
    for i in range(length):
        if i==0:
            if not word[i].isalnum():
                count=1
                prev_alnum=False
            elif word[i].isdigit():
                prev_digit=True
            elif word[i].isupper():
                prev_upper=True
        else:
            if not word[i].isalnum():
                if prev_alnum:
                    wordlist.append(word[count:i])
                    count=i+1
                else:
                    return wordlist
                prev_alnum=False
                prev_upper=False
                prev_digit=False
                lower_streak=False
                upper_streak=False
            elif word[i].isdigit():
                if (not prev_digit) and (prev_alnum):
                    wordlist.append(word[count:i])
                    count=i
                prev_upper=False
                prev_digit=True
                prev_alnum=True
                lower_streak=False
                upper_streak=False
            elif word[i].isupper():
                if (not prev_upper) and (prev_alnum) and (lower_streak or prev_digit):
                    wordlist.append(word[count:i])
                    count=i
                if prev_upper:
                    upper_streak=True
                prev_upper=True
                prev_digit=False
                prev_alnum=True
                lower_streak=False
            else :
                if prev_upper and upper_streak and (not i==length-1):
                    if word[i+1].isupper():
                        wordlist.append(word[count:i])
                        lower_streak=True
                        count=i
                    else:    
                        wordlist.append(word[count:i-1])
                        count=i-1

                elif prev_digit:
                    wordlist.append(word[count:i])
                    count=i
                elif prev_alnum==True and prev_digit==False and (prev_upper==False or (prev_upper==True and count==i-1)):
                    lower_streak=True
                prev_upper=False
                prev_digit=False
                prev_alnum=True
                upper_streak=False
    if word[i].isalnum():
        wordlist.append(word[count:i+1])
    return wordlist


def insert_vocab(word):
    #Function used for creating the dictionary of all words
    if word not in vocab:
        vocab[word]=1
    else:
        vocab[word]+=1

def if_occur(word,list):
    #used for checking if a word occurs in the list of one tweet 
    count=0
    if word in list :
        return 1


def create_wordlist(tweet,isvocab=True):
    #function used for reading any tweet and creating features out of it 
    wordlist=[]
    no_of_words=0
    no_of_https=0
    no_of_years=0
    no_of_dates=0
    no_of_scores=0
    no_of_symbol=0
    no_of_nums=0
    sum_of_length=0
    complex_words=0
    wordsintweet=tweet.split()
    for word in wordsintweet:
        if not word[:4]=="http":
            no_of_words+=1
            sum_of_length+=len(word)
            temp=getwords(word)
            if len(temp)==0:
                no_of_symbol+=1
            else:
                if len(temp)>1:
                    complex_words+=1
                else:
                    no_of_words+=1
                    sum_of_length+=len(word)
                for i in temp:
                    if i.isdigit():
                        if len(i)==4:
                            no_of_years+=1
                        else:
                            no_of_nums+=1
                    else:
                        stemmedword=str(stemmer.stem(i))
                        stemmedword=stemmedword.lower()
                        if stemmedword not in stopwords_list:
                            wordlist.append(stemmedword)
                        if isvocab:
                            insert_vocab(stemmedword)
        else:
            no_of_https+=1
    temp=re.findall(r'\d+/\d+/\d+',tweet)
    no_of_dates+=len(temp)
    temp=re.findall(r'\d+/\d+',tweet)
    no_of_scores+=len(temp)
    temp=re.findall(r'\d+-\d+',tweet)
    no_of_scores+=len(temp)
    temp=re.findall(r'#',tweet)
    counthashtag.append(len(temp))
    temp=re.findall(r'@',tweet)
    countattherate.append(len(temp))
    if no_of_words==0:
        avg_length=1
    else:
        avg_length=sum_of_length/(1.0*no_of_words)
    no_of_scores-=(2*no_of_dates)
    no_of_years-=no_of_dates
    no_of_nums-=((2*no_of_scores)+(2*no_of_dates))
    countwordlist.append(no_of_words)
    avglenlist.append(avg_length)
    countyears.append(no_of_years)
    counthttps.append(no_of_https)
    countdates.append(no_of_dates)
    countnums.append(no_of_nums)
    countscores.append(no_of_scores) 
    return wordlist


def main():
    global countwordlist
    global avglenlist
    global countyears
    global counthttps
    global countdates
    global countnums
    global countscores
    global counthashtag
    global countattherate
    
    f=open("training.txt","r")
    train_words=[]
    y_train=[]
    counter=0
    totalpol=0
    totalspor=0
    no_sport=0
    no_pol=0
    x=0
    while True :
        line=f.readline()
        if len(line)>0:
            text1=re.findall(r'Sports.+',line)
            text2=re.findall(r'Politics.+',line)
            if len(text1) > len(text2) :
                tweet=text1[0][8:]
                y_train.append(1)
                train_words.append(create_wordlist(tweet))
            else:
                tweet=text2[0][10:]
                y_train.append(0)
                train_words.append(create_wordlist(tweet))
                    
            x+=1
        else:
            break
    print "The number of words in the dictionary are :" ,len(vocab)
    x_train=[]
    vocab_words=vocab.keys()
    i=0
    for wordlist in train_words :
        temp=[]
        for vocab_word in vocab_words:
            temp.append(if_occur(vocab_word,wordlist))
        temp.append(countwordlist[i])
        temp.append(avglenlist[i])
        temp.append(countyears[i])
        temp.append(counthttps[i])
        temp.append(countdates[i])
        temp.append(countnums[i])
        temp.append(countscores[i])
        temp.append(counthashtag[i])
        temp.append(countattherate[i])
        i+=1
        x_train.append(temp)


    countwordlist=[]
    avglenlist=[]
    countyears=[]
    counthttps=[]
    countdates=[]
    countnums=[]
    countscores=[]
    counthashtag=[]
    countattherate=[]
    """ here the test file is opened and its features are extracted """
    f.close()
    f=open("test.txt")
    test_words=[]
    tweet_id_list=[]
    x_test=[]
    while True:
        line=f.readline()
        if len(line) > 0:
            no_list=re.findall(r'\d+',line)
            tweet_id=no_list[0]
            tweet=line[len(tweet_id)+2:]
            tweet_id_list.append(tweet_id)
            test_words.append(create_wordlist(tweet,False))
        else:
            break

    i=0
    for wordlist in test_words:
        temp=[]
        for vocab_word in vocab_words :
            temp.append(if_occur(vocab_word,wordlist))
        temp.append(countwordlist[i])
        temp.append(avglenlist[i])
        temp.append(countyears[i])
        temp.append(counthttps[i])
        temp.append(countdates[i])
        temp.append(countnums[i])
        temp.append(countscores[i])
        temp.append(counthashtag[i])
        temp.append(countattherate[i])
        i+=1

            
            
        x_test.append(temp)

    svc=svm.SVC(kernel='linear')
    svc.fit(x_train[:-1000],y_train[:-1000])
    print svc.score(x_train[-1000:],y_train[-1000:])
    #ans=svc.predict(x_test)
    f.close()
    f=open("answer.txt","w+")
    for pair in zip(tweet_id_list,ans):
        f.write(str(pair[0])+" ")
        if pair[1]==0:
            category="Politics"
        else :
            category="Sports"
        f.write(category+"\n")
    f.close()
            
    
if __name__=="__main__":
    main()
    
