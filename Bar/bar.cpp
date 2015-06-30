#include <iostream> // std::cout
#include <bar_export.h> // BAR_EXPORT

void foo();
void boo();

void BAR_EXPORT bar() {
  foo();
  boo();
  std::cout << "Hello from bar" << std::endl;
}
