#ifndef __AI_H__
#define __AI_H__

#include "Base.h"
#include "Bullet.h"
#include "Coordinate.h"
#include "Field.h"
#include "Item.h"
#include "Unit.h"

#include <iostream>
#include <vector>
using namespace std;

class Ai{
  bool read_end(string read,istream& file_or_cin);
public:
  Ai(){}
  ~Ai(){}

  vector<Base> bases;
  vector<Bullet> bullets;
  Field field;
  vector<Item> items;
  vector<Unit> units;
  Unit myunit;

  bool read_init(istream& file_or_cin = cin);
  bool read_main(istream& file_or_cin = cin);
  void main();
  void init_commit_message();
  void commit_message(double move, double roll_angle, bool firing);

  double limited_move(double move);
  double limited_angle(double angle);
  double regularize_angle(double angle);
};

#endif