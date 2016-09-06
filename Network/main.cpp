#include <iostream>
using namespace std;


int main(){
	int counter = 0;
	while(counter < 100){
		int data;
		cin>>data;
		// cerr<<"Child Received "<<data<<"\n";
		counter = data + 1;
		cout<<counter<<"\n";
	}
	
}