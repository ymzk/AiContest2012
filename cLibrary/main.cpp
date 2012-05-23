#include "ai.h"

#include <iostream>
#include <fstream>

using namespace std;

int main(){
  Ai ai = Ai();
/*
  ifstream init_message = ifstream("initmessage");
  ifstream message = ifstream("message");
  if(!ai.read_init(init_message)){
    cerr<<"read err init"<<endl;
  }
  ai.init_commit_message();
  while(ai.read_main(message)){
    ai.main();
  }
  //*/
  //*
  ai.read_init();
  ai.init_commit_message();
  while(ai.read_main()){
    ai.main();
  }
  //*/
  return 0;
}