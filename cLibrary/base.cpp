#include "base.h"
#include "main.h"

Base::Base(istream& is){
  read(is);
}

void Base::read(istream& is){
  is>>hp>>team>>position;
  return;
}

