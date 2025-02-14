#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
  int fd = open("/flag.txt", 0);
  setuid(getuid());
  system("/bin/sh");
  return 0;
}
