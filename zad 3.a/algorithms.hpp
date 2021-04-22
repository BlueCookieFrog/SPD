#ifndef ALGORITHMS_HH
#define ALGORITHMS_HH

#include <vector>
#include <stdio.h>

#include "graph.hpp"
#include "RandomNumberGenerator.h"

using namespace std;
//**************************************************
// classes for generator functions
class Operation
{
public:

    int number,start,time,end;
    Operation(int number, int time): number(number), time(time) {}
    Operation(){}
    ~Operation(){}
};


class Task
{
public:
    vector<Operation>operation;
    Task(){}
    ~Task(){}
    void addOperation(Operation operant){
        operation.push_back(operant);
    }
    int last(){
        return this->operation.size() - 1;
    }
};
//**************************************************



//**************************************************
//cmax calculation function
int Cmax(const vector<Task*> &Tasks)
{
    int lastpoint = 0;
    int lastOp=Tasks[lastpoint]->last(),lastTask=Tasks.size()-1;

    for(int i =0; i<=lastOp; ++i)
    {
        for (int j=0; j<=lastTask;++j)
        {
            int currentCmax,previousCmax,totalCmax;
            int currentTaskTime=Tasks[j]->operation[i].time;;
            if(i==0)
            {
                previousCmax=0;
                if(j == 0)
                { 
                    currentCmax = 0 + currentTaskTime; 
                }
                else
                {
                 currentCmax = Tasks[j-1]->operation[i].end + currentTaskTime; 
                }

            }
            else
            { 
                previousCmax = Tasks[j]->operation[i-1].end;
                if(j == 0) 
                {
                    totalCmax = 0; 
                }
                else {
                    totalCmax = Tasks[j-1]->operation[i].end; 
                }
                currentCmax = max(previousCmax, totalCmax) + currentTaskTime; 
            }
            Tasks[j]->operation[i].end = currentCmax; 
        }

    }
    return Tasks[lastTask]->operation[lastOp].end; 
}
    

//**************************************************

//**************************************************
//shortest time finder
inline Task* shortestTask(const vector<Task*> &Tasks, int *task) {
    Task* minTask = Tasks[0]; 
    *task = 0;
        int currFirstMach ,currLastMach,chFirstMach,chLastMach ;
    //int bestl =
    //int bestf = 
    for(int i = 0; i < Tasks.size(); ++i) { 
         currFirstMach = Tasks[i]->operation[0].time; 
         currLastMach = Tasks[i]->operation[minTask->last()].time; 
         chFirstMach = minTask->operation[0].time; 
         chLastMach = minTask->operation[minTask->last()].time; 
    //cout<<i;
        if(currFirstMach < chFirstMach) { 
            if (currFirstMach < chLastMach) { 
                minTask = Tasks[i];
                *task = i; 
            }
        }

        if(currLastMach < chFirstMach) { 
            if(currLastMach < chLastMach) { 
                minTask = Tasks[i];
                *task = i;
            }
        }
    }
    //cout<<"mintask"<<;
    return minTask;
}
//**************************************************


//**************************************************
//johnson
vector<Task*> Jonson(vector<Task*> Tasks) {
    int a = 0,b=Tasks.size() - 1; 
    vector<Task*> Pi;
    Pi.resize(Tasks.size());

    while(!Tasks.empty()) 
    {
        int taskNumber; 
        Task* minTask;
        minTask = shortestTask(Tasks, &taskNumber); 
        if(minTask->operation[0].time < minTask->operation[minTask->operation.size()-1].time) 
        {
            Pi.at(a++) = minTask; 
        }
         else
        {
            Pi.at(b--) = minTask; 
        }
        Tasks.erase(Tasks.begin() + taskNumber); 
        //cout<<"test12";
    }

    return Pi;
}   
//**************************************************



//**************************************************
//
vector<vector<Task*>>traverse(Graph<Task*> &graph, const vector<vector<Task*>> values = {{}}, int node = 0) {
  if (graph.adj[node].size() > 1) { 
    auto res = vector<vector<Task*>>(); 

    for (auto i = graph.adj[node].begin(); i != graph.adj[node].end(); ++i) { 
      auto x = traverse(graph, values, *i); 
      res.insert(res.end(), x.begin(), x.end()); 
    }
    if (node != 0) { 
      for (int i = 0; i < res.size(); ++i) { 
        res[i].push_back(graph.vertices[node]); 
      }
    }

    return res;
  } else { 
    Task* child = graph.vertices[graph.adj[node][0]]; 
    Task* parent = graph.vertices[node]; 
    return {{child, parent}};
  }
}




vector<Task*> BruteForce(vector<Task*> N)
 {
    int minimumCmax = (1<<16); 
    vector<Task*>* Pi; 

    auto graph_n = Graph<Task*>::tree(N); 
    auto combinations = traverse(graph_n); 

    for(int i = 0; i < combinations.size(); ++i) 
    { 
        int actualC = Cmax(combinations[i]); 
        if(actualC < minimumCmax) 
        { 
            minimumCmax = actualC; 
            Pi = &(combinations[i]); 
        }
    }
    return *Pi;
}


#endif