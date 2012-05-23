#include "Item.h"
#include "main.h"

Item::Item(istream& is){
  read(is);
}

void Item::read(istream& is){
  is>>position>>itemType;
}

