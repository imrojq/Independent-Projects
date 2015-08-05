#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <string.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <queue>
#include <map>

using namespace std;

#define forall(i,a,b)                   for(int i=a;i<b;i++)
#define all(c)                          c.begin(),c.end()
#define tr(container,it )               for(typeof(container.begin()) it = container.begin(); it!=container.end();it++)

typedef vector<int> vi;
typedef vector<vi> vvi;
typedef pair<int,int> pii;
typedef map<vi,int> mvivi;
typedef pair<int,vi> pivi;
typedef pair<int,int> ii;
//typedef pair<vi,vvi> pvivvi;
// typedef vector<pvivvi> vpvivvi;
// typedef pair<int,vvi> pivvi;
// typedef map<vvi,pivvi> mvvipivvi;

void readState(int k,vi &state)
{
    int ans;
    int temp;
    forall(i,0,k*k)
    {
        cin>>temp;
        if (temp==0)
            ans=i;
        state[i]=temp;
    }
    state[k*k]=ans;
    // state[k*k+1]=ans;
}
    
 void printState(int k,vi &state)
{
   // int k=state.size();
    
    forall(i,0,k)
    {
        forall(j,0,k)
            cout<<state[i*k+j]<<" ";
       // cout<<state[k*k];
        cout<<"\n";
    }
    
}
        
void createGoalState(vi &success,int k)
{
    forall(i,0,k*k)
        success[i]=i;
}

int  heuristic(vi &success, vi &state,int k, map<int,ii> &cordinate)
{
    int count=0;
    ii a,b;
    forall(i,0,k*k)
    {
        if (success[i]!=state[i])
            count+=1;
        /*a=cordinate[i];
        b=cordinate[state[i]];
        count+=(abs(a.first-b.first));
        count+=(abs(a.second-b.second));*/
    }
    return count;
}

void getSuccessors(vi state, int k, vvi &successors, mvivi &parent)
{
    int zero= state[k*k];
    int itemp;
    //left
    if (zero%k!=0)
    {
        vi temp=state;
        temp[zero]=temp[zero-1];
        temp[zero-1]=0;
        // temp[k*k]=1;
        temp[k*k]=zero-1;
        if(parent.find(temp)==parent.end())
        {
            parent[temp]=1;
            successors.push_back(temp);
        }
    }   
    //right
    if (zero%k!=k-1)
    {
        vi temp=state;
        temp[zero]=temp[zero+1];
        temp[zero+1]=0;
        // temp[k*k]=2;
        temp[k*k]=zero+1;
        if(parent.find(temp)==parent.end())
        {
            parent[temp]=2;
            successors.push_back(temp);
        }
    }    
    //up
    if (zero/k!=0)
    {
        vi temp=state;
        temp[zero]=temp[zero-k];
        temp[zero-k]=0;
        // temp[k*k]=3;
        temp[k*k]=zero-k;
        if(parent.find(temp)==parent.end())
        {
            parent[temp]=3;
            successors.push_back(temp);
        }
    }    
    if (zero/k!=k-1)
    {
        vi temp=state;
        temp[zero]=temp[zero+k];
        temp[zero+k]=0;
        // temp[k*k]=4;
        temp[k*k]=zero+k;
        if(parent.find(temp)==parent.end())
        {
            parent[temp]=4;
            successors.push_back(temp);
        }
    }
}
        
void findParent(int n, vi &state , vector<string> &path,int k)
{
    int zero=state[k*k];
    if (n==1)
    {
        state[zero]=state[zero+1];
        state[zero+1]=0;
        state[k*k]+=1;
        path.push_back("LEFT");
    }
    if (n==2)
    {
        state[zero]=state[zero-1];
        state[zero-1]=0;
        state[k*k]-=1;
        path.push_back("RIGHT");
    }
    if (n==3)
    {
        state[zero]=state[zero+k];
        state[zero+k]=0;
        state[k*k]+=k;
        path.push_back("UP");
    }
    if (n==4)
    {
        state[zero]=state[zero-k];
        state[zero-k]=0;
        state[k*k]-=k;
        path.push_back("DOWN");
    }
}
        
        
int main()
{
    int k,zero,elements,itemp;
    cin>>k;
    elements=k*k;
    priority_queue<pivi,vector<pivi>,greater<pivi> > qvi;
    vi state(elements+1),success(elements+1);
    readState(k,state);
    createGoalState(success,k);
    //printState(k,state); 
    mvivi parent;
    parent[state]=5;
    map <int,ii> cordinate;
    forall(i,0,elements)
    cordinate[i]=ii(i/k,i%k);
    cout<<"\n";
    cout<<"\n";
    int count=heuristic(success,state,k,cordinate);
    ofstream myfile;
    myfile.open("ans.txt");
    while(count!=0)
    {
        vvi successors;
        getSuccessors(state,k,successors,parent);
        forall(i,0,successors.size())   
                qvi.push(pivi(heuristic(success,successors[i],k,cordinate),successors[i]));
        pivi a=qvi.top();
        qvi.pop();
        count=a.first;
        state=a.second;
        //printState(k,state);
        myfile<<count<<"\n";
    }
   // printState(k,state);
    vector<string> path;
    int dir=parent[state];
    
   // cout<<"\n\n\n";
    
    while(dir!=5)
    {
        findParent(dir,state,path,k);
        // printState(k,state);
        // cout<<"\n";
        //cout<<dir<<"\n";
        //if (parent.find(state)==parent.end())
          //  break;
        dir=parent[state];
        //cout<<"hi";
    }
    int length=path.size();
    cout<<length<<"\n";
    forall(i,1,length+1)
        myfile<<path[length-i]<<"\n";
    
    
    return 0;
}
        
                
        
    
    

            
         

