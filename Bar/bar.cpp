#include <iostream> // std::cout
#include <bar_export.h> // BAR_EXPORT

void foo();
void boo();

std::string BAR_EXPORT bar() {
  foo();
  boo();
  std::string result("Hello from bar");
  std::cout << result << std::endl;
  return result;
}
