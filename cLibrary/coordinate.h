#ifndef __COORDINATE_H__
#define __COORDINATE_H__

#include <iostream>

using namespace std;

class Coordinate{
public:
  double x,y;
  Coordinate(){}
  Coordinate(double x,double y):x(x),y(y){}
  ~Coordinate(){}
  friend istream& operator >> (istream&, Coordinate&);
};
istream& operator >> (istream&, Coordinate&);

#endif