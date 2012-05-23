#include "unit.h"
#include "main.h"

Unit::Unit(istream& is){
  read(is);
}

void Unit::read(istream& is){
  is>>hp>>team>>position>>direction>>attack>>reload>>unit_id;
}

bool Unit::is_same(Unit& opponent){
  return unit_id == opponent.unit_id;
}