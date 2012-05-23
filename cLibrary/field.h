#ifndef __FIELD_H__
#define __FIELD_H__

#include "coordinate.h"

#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Field{
public:
  Field(){}
  Field(istream& file_or_cin);
  ~Field(){}
  int width;
  int height;
  vector<vector<string>> cell_map;
  vector<Coordinate> base_position_list;
  vector<Coordinate> hp_item_position_list;
  vector<Coordinate> attack_item_position_list;
  void read(istream& file_or_cin);
};

#endif