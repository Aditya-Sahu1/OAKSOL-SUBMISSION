#include<bits/stdc++.h>
using namespace std;
int main(){
    string s1="1122233222234455";
    vector<bool>hash(10,false);
    string s2="";
    for(int i=0;i<s1.size();++i){
        int digit=s1[i]-'0';
        if(i>0 && s1[i]!=s1[i-1]){
            hash[s1[i]-'0']=false;
        }
        if(hash[digit]==false){
            s2+=s1[i];
            hash[digit]=true;
        }
        
    }
    cout<<s2<<"\n";
    return 0;
}