#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <unistd.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>

void sandbox(){
	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_ALLOW);
	seccomp_arch_add(ctx, SCMP_ARCH_X86_64);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_open, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_mmap, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_mremap, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_ptrace, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_shmat, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_shmget, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_clone, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_fork, 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, __NR_execve, 0);
	seccomp_rule_add_exact(ctx, SCMP_ACT_KILL, __NR_execveat, 1, SCMP_A1(SCMP_CMP_NE, 0x696969690000));
	seccomp_load(ctx);
	seccomp_release(ctx);
}

int main(){
	char *func = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANON|MAP_PRIVATE, -1, 0);
	sandbox();
	printf("gimme your best shot\n");
	fgets(func,0x1000,stdin);
	((void (*)())func)();
}

__attribute__((constructor))
void init(){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
}
