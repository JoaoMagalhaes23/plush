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
	movl	%esi, (%rsp)
	movq	actual_min@GOTPCREL(%rip), %rax
	movl	$7, (%rax)
	movl	$7, %edi
	callq	print_int@PLT
	movl	$1, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	actual_min,@object              # @actual_min
	.data
	.globl	actual_min
	.p2align	2
actual_min:
	.long	9                               # 0x9
	.size	actual_min, 4

	.section	".note.GNU-stack","",@progbits
