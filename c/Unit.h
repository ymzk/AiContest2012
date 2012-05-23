#ifndef __UNIT_H__
#define __UNIT_H__

#include "Coordinate.h"

#include <iostream>

using namespace std;


class Unit{
public:
  Unit(){}
  Unit(istream& file_or_cin);
  ~Unit(){}
  int hp;
  int team;
  Coordinate position;
  double direction;
  int attack;
  int reload;
  int unit_id;
  void read(istream& file_or_cin);

  bool is_same(Unit& opponent);
};

#endif