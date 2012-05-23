#include "bullet.h"
#include "main.h"

Bullet::Bullet(istream& is){
  read(is);
}

void Bullet::read(istream& is){
  is>>team>>position>>direction>>move_vector;
}

