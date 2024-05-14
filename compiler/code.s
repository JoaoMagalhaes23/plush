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
	movq	e@GOTPCREL(%rip), %rax
	movq	(%rax), %rdi
	movl	$2, %esi
	movl	$5, %edx
	callq	print_2d_int_array@PLT
	movl	$1, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.array1,@object                 # @.array1
	.data
	.globl	.array1
	.p2align	2
.array1:
	.long	1                               # 0x1
	.long	2                               # 0x2
	.size	.array1, 8

	.type	.array2,@object                 # @.array2
	.globl	.array2
	.p2align	2
.array2:
	.long	3                               # 0x3
	.long	4                               # 0x4
	.long	5                               # 0x5
	.size	.array2, 12

	.type	.array3,@object                 # @.array3
	.globl	.array3
	.p2align	3
.array3:
	.quad	.array1
	.quad	.array2
	.size	.array3, 16

	.type	e,@object                       # @e
	.globl	e
	.p2align	3
e:
	.quad	.array3
	.size	e, 8

	.section	".note.GNU-stack","",@progbits
