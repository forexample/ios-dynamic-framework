#include <iostream> // std::cout

void foo();
void boo();

void bar() {
  foo();
  boo();
  std::cout << "Hello from bar" << std::endl;
}
