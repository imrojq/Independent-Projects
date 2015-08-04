#include <iostream>
#include <vector>
#include <fstream>
#include <stdio.h>
#include <string.h>
#include <algorithm>
#include <map>

using namespace std;

#define forall(i,a,b)       for(int i=a;i<b;i++)

typedef vector<string> vs;
typedef vector<int> vi;
typedef vector<char> vc;
typedef vector<vc> vvc;
typedef vector<vs> vvs;

struct MyStruct
{
    int key;
    string stringValue;

    MyStruct(int k, const std::string& s) : key(k), stringValue(s) {}

    bool operator < (const MyStruct& str) const
    {
        return (key < str.key);
    }
};

vector < MyStruct > vec;


char highestProb(vs &givenWords,vi &guessed)
{
    vi letters(26,0);
    int totalWords=givenWords.size(),max=0,maxIndex=0;
    string word;
    forall(i,0,totalWords)
    {
        word=givenWords[i];
        vi temp(26,0);
        forall(j,0,word.length())
            temp[word[j]-'a']+=1;
        forall(i,0,26)
            if(temp[i]!=0 && guessed[i]==0)     letters[i]+=1;
    }
    forall(i,0,26)
    {
        if(letters[i]>max)
        {
            max=letters[i];
            maxIndex=i;
        }
    }
    return 'a'+maxIndex;
}
    

void update(vs &possibleWords,string guessWord,char letter,bool success)
{
    vs newList;
    int length=possibleWords.size(),len,wordLength;
    string word;
    bool flag;
    if (success)
    {
        forall(i,0,length)
        {
            flag=true;
            word=possibleWords[i];
            wordLength=word.size();
            forall(j,0,wordLength)
            {
                if ((guessWord[j]==letter && word[j]!=letter) || (guessWord[j]!=letter && word[j]==letter) )
                {
                    flag=false;
                    break;
                }
            }
            if (flag)
                newList.push_back(word);
        }
    }
    else
    {
        forall(i,0,length)
        {
            word=possibleWords[i];
            if (word.find(letter)==string::npos)
                newList.push_back(word);
        }
    }
    possibleWords=newList;
}
    


            
                    
        
void assignScore(vvs &wordsByLength,vs &wordlist,vvc &topLetter,int maxLength)
{
    int sum,limit,length;
    string word;
    forall(i,1,maxLength+1)
    {
        vs possibleWords=wordsByLength[i];
        vi guessed(26,0);
        char letter;
        string guessWord(i,'-');
        forall(j,0,7)
        {
            letter=highestProb(possibleWords,guessed);
            guessed[letter-'a']=1;
            topLetter[i].push_back(letter);
          //  update(possibleWords,guessWord,letter,false);
        }
    }
    forall(i,0,wordlist.size())
    {
        sum=0;
        word=wordlist[i];
        length=word.length();
        int size=topLetter[length].size();
        limit=min(6,size);
        forall(j,0,size)
        {
            if(word.find(topLetter[length][j])!=string::npos)
                sum+=1;
        }
        vec.push_back(MyStruct(sum,word));
    }
}
    
    

int main()
{
    //FILE *fp;
    ifstream fp ("dist.txt");
    string str;
    vs wordlist;
    vvs wordsByLength;
    vvc topLetter;
    int l,chances,numguessed,length;
    char letter,command;
    string word;
    int num;
    int maxLength=0;
    int a;
    fp>>num;
    
    forall(i,0,num)
    {
        fp>>str;
        wordlist.push_back(str);
        if (str.length() > maxLength)
            maxLength=str.length();
    }

    cin>>command;
    if (command=='S')
    {
        vs possibleWords;
        vi guessed(26,0);
        cin>>l>>word>>chances>>numguessed;
        vc guesses(numguessed);
        forall(i,0,numguessed)
            cin>>guesses[i];
        length=word.size();
        forall(i,0,num)
            if(wordlist[i].size()==length) possibleWords.push_back(wordlist[i]);
        forall(i,0,numguessed)
        {
            guessed[guesses[i]-'a']=1;
            if (word.find(guesses[i])!=string::npos)
                update(possibleWords,word,guesses[i],true);
            else
                update(possibleWords,word,guesses[i],false);
        }
        letter=highestProb(possibleWords,guessed);
        cout<<letter<<"\n";

    }
    else if (command=='G')
    {
        vs temp;
        vc temp1;
        forall(i,0,maxLength+1)
        {
            wordsByLength.push_back(temp);
            topLetter.push_back(temp1);
        }
        forall(i,0,wordlist.size())
            wordsByLength[wordlist[i].size()].push_back(wordlist[i]);
        assignScore(wordsByLength,wordlist,topLetter,maxLength);
        sort(vec.begin(),vec.end());
        cin>>l;
        forall(i,0,l)
            cout<<vec[i].stringValue<<"\n";
           
    }
    return 0;
}

/*Team
Imroj Qamar 2011CS1011
Rahul Kumar 2011CS1030
*/