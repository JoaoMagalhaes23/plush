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
	movb	$1, 3(%rsp)
	movl	$1, %edi
	callq	print_boolean@PLT
	movl	$1, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	y,@object                       # @y
	.data
	.globl	y
	.p2align	2
y:
	.long	1                               # 0x1
	.size	y, 4

	.section	".note.GNU-stack","",@progbits
