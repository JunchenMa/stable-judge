#include<iostream>
#include <vector>
#include <set>

using namespace std;

vector<vector<int> > men, women;
int num;
set<vector<int> > stable_pairs;


bool judge_stable(vector<int> p){
    for(int i=0;i<num;i++){
        //对本次排列的男i的来说,匹配为pi，更喜欢的在set里
        int wife = p[i];
        set<int> men_like_more_women;
        for(int j=0;j<num;j++){
            if(men[i][j]!=wife){
                men_like_more_women.insert(men[i][j]);
            }else{
                break;
            }
        }
        //判断男i更喜欢set中的女性，比起她对应的配偶是否有男i更喜欢
        for(auto x:men_like_more_women){
            int husband;
            for(int k=0;k<num;k++){
                if(p[k]==x){
                    husband = k+1;
                }
            }
            for(int m=0;m<num;m++){
                if(women[x-1][m]==i+1){
                    return false;
                }
                if(women[x-1][m]==husband){
                    break;
                }
            }
        }
    }
    return true;
}

int main(){
    // 样例
    men = {{2,1,3},{1,3,2},{1,2,3}};
    women = {{1,3,2},{3,1,2},{1,3,2}};
    num = men.size();

    // 全排列
    // 3，2，1 代表 男1女3，男2女2，男3女1
    vector<int> t;
    for(int i=1;i<=num;i++){
        t.emplace_back(i);
    }
    do{
        //pairs.insert(t);
        if(judge_stable(t)){
            stable_pairs.insert(t);
        }
    }while(next_permutation(t.begin(),t.end()));

    for(auto x:stable_pairs){
        for(auto y:x){
            cout <<y<<" ";
        }
        cout << endl;
    }

    return 0;
}