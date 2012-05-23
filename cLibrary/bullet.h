#ifndef __BULLET_H__
#define __BULLET_H__

#include "coordinate.h"

#include <iostream>

using namespace std;

class Bullet{
public:
  Bullet(){}
  Bullet(istream& file_or_cin);
  ~Bullet(){}
  int team;
  Coordinate position;
  double direction;
  Coordinate move_vector;
  void read(istream& file_or_cin);

};

#endif