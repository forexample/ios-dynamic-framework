#include <bar/bar.hpp>

#include <iostream> // std::cout

#include <foo.hpp>
#include <boo.hpp>

void bar() {
  foo();
  boo();
  std::cout << "Hello from bar" << std::endl;
}
