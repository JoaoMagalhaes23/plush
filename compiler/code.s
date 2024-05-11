	.text
	.file	"code.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	%edi, 4(%rsp)
	movl	$0, (%rsp)
	cmpl	$9, (%rsp)
	jg	.LBB0_3
	.p2align	4, 0x90
.LBB0_2:                                # %while.body3
                                        # =>This Inner Loop Header: Depth=1
	movl	(%rsp), %edi
	callq	print_int@PLT
	incl	(%rsp)
	cmpl	$9, (%rsp)
	jle	.LBB0_2
.LBB0_3:                                # %while.end4
	xorl	%eax, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
