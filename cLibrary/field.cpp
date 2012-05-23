#include "field.h"
#include "main.h"

Field::Field(istream& is){
  read(is);
}

void Field::read(istream& is){
  is>>width>>height;
  cell_map.clear();
  for(int h = 0; h < height; h++){
    vector<string> cell_line;
    for(int w = 0; w < width; w++){
      string str;
      is>>str;
      cell_line.push_back(str);
    }
    cell_map.push_back(cell_line);
  }
}

