#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm> 
#include <functional> 
#include <cctype>
#include <locale>
using namespace std;
// trim from start
static inline std::string &ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(),
            std::not1(std::ptr_fun<int, int>(std::isspace))));
    return s;

}

// trim from end
static inline std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(),
            std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;

}

// trim from both ends
static inline std::string &trim(std::string &s) {
    return ltrim(rtrim(s));

}
void getAllMoves(vector<string>& allMoves, string fileName){
	ifstream moveFile;
	moveFile.open(fileName);
	while(!moveFile.eof()){
		string move;
		moveFile >> move;
		allMoves.push_back(move);
	}
}
int main(){
	string data;
	int n,TL;
	cin>>data>>n>>TL;
	int player = -1;
	vector<string> allMoves;
	if(data == "1"){
		player = 1;
		getAllMoves(allMoves, "whiteMoves.txt");
	}
	else{
		player = 2;
		getAllMoves(allMoves, "blackMoves.txt");	
	}
	if(player == 1){
		int idx = 0;
		while(1){
			string move = trim(allMoves[idx]);
			move += '\n';
			cout<<move;
			cin>>move;
			idx += 1;
			if( idx == allMoves.size() )
				break;			
		}
	}
	else{
		int idx = 0;
		while(1){
			string move;
			cin >> move;
			move = trim(allMoves[idx]);
			cout<<move<<"\n";
			idx ++;
			if(idx == allMoves.size()){
				break;
			}		
		}
	}

}

