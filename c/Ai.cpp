#include "Ai.h"
#include "main.h"

bool Ai::read_init(istream& is){
  string str;
  is>>str;
  if(str != "startInit"){
    return false;
  } 
  while(is>>str){
    if(str == "unit"){
      myunit = Unit(is);
    }else if(str == "field"){
      field = Field(is);
    }else if(str == "endInit"){
      //success
      return true;
    }else{
      return false;
    }
  }
  return false;
}
void Ai::init_commit_message(){
  cout<<"0 0 0"<<endl;
}

bool Ai::read_main(istream& is){
  string str;
  is>>str;
  if(str != "start"){
    if(read_end(str, is)){
      return false;
    }else{
      cerr<<"read_main_err"<<endl;
      return false;
    //解析ミス。
    }
  }
  units.clear();
  bullets.clear();
  bases.clear();
  items.clear();
  while(is>>str){
    if(str == "unit"){
      Unit unit = Unit(is);
      if(unit.is_same(myunit)){
        myunit = unit;
      }else{
        units.push_back(unit);
      }
    }else if(str == "bullet"){
      bullets.push_back(Bullet(is));
    }else if(str == "base"){
      bases.push_back(Base(is));
    }else if(str == "item"){
      items.push_back(Item(is));
    }else if(str == "end"){
      return true;
    }else{
      return false;
    }
  }
  return false;
}
double Ai::limited_move(double move){
  if(move > 3){
    return 3;
  }else if(move < 0){
    return 0;
  }else{
    return move;
  }
}
double Ai::regularize_angle(double angle){
  double pi = 3.14159265;
  return angle - int(angle/pi/2 + 0.5) * 2 * pi + pi;
}
double Ai::limited_angle(double angle){
  angle = regularize_angle(angle);
  double limit = 0.1;
  if(angle > limit){
    return limit;
  }else if(angle < -limit){
    return -limit;
  }else{
    return angle;
  }
}
void Ai::commit_message(double move, double angle, bool firing){
  cout<<limited_move(move)<<limited_angle(angle)<<(firing?1:0)<<endl;
}
bool Ai::read_end(string read,istream& is){
  return true;
  //終了時表示とかする？
}



void Ai::main(){}



