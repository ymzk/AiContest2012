#ifndef __ITEM_H__
#define __ITEM_H__

#include "coordinate.h"

#include <iostream>
#include <string>

using namespace std;

class Item{
public:
  Item(){}
  Item(istream& file_or_cin);
  ~Item(){}
  Coordinate position;
  string itemType;
  void read(istream& file_or_cin);
};

#endif


