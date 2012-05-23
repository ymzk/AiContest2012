#ifndef __BASE_H__
#define __BASE_H__

#include "Coordinate.h"

#include <iostream>

using namespace std;

class Base{
public:
  Base(){}
  Base(istream& file_or_cin);
  ~Base(){}
  int hp;
  int team;
  Coordinate position;
  void read(istream& file_or_cin);
};

#endif