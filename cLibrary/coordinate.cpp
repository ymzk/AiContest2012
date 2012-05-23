#include "Coordinate.h"

istream& operator >> (istream& is,Coordinate& opponent){
  return(is>>opponent.x>>opponent.y);
}