	.text
	.file	"code.ll"
	.globl	x                               # -- Begin function x
	.p2align	4, 0x90
	.type	x,@function
x:                                      # @x
	.cfi_startproc
# %bb.0:                                # %entry
	movl	$1, %eax
	retq
.Lfunc_end0:
	.size	x, .Lfunc_end0-x
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	%edi, 4(%rsp)
	movl	$1, (%rsp)
	movl	$1, %edi
	callq	print_int@PLT
	movl	$1, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
