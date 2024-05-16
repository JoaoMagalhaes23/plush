	.text
	.file	"code.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	%edi, 16(%rsp)
	movq	b@GOTPCREL(%rip), %rax
	movl	(%rax), %edi
	movl	%edi, %eax
	negl	%eax
	movl	%eax, 12(%rsp)
	callq	print_int@PLT
	movl	12(%rsp), %edi
	callq	print_int@PLT
	movl	20(%rsp), %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	b,@object                       # @b
	.data
	.globl	b
	.p2align	2
b:
	.long	4294967295                      # 0xffffffff
	.size	b, 4

	.section	".note.GNU-stack","",@progbits
