#include <stdio.h>
#include <stdlib.h>
#include <seccomp.h>

int init(){
  setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
}

void setup_seccomp()
{
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(open),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(read),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(write),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit),0);
	seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(exit_group),0);
  seccomp_rule_add(ctx,SCMP_ACT_ALLOW,SCMP_SYS(openat), 0);
	seccomp_load(ctx);
}

int main(int argc, char **argv, char **envp){
  init();
  setup_seccomp();
  char buf[0xff];
  unsigned long long int *bufptr;
  unsigned long long int *bufptr2;

  fgets(buf, 0xc, stdin);
  printf(buf);
  scanf("%p", &bufptr);
  printf("%llu\n", *bufptr);
  scanf("%p", &bufptr2);
  read(0, bufptr2, 0xf0);
  
  return 0;
}