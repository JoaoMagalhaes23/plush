	.text
	.file	"code.ll"
	.globl	binarySearch                    # -- Begin function binarySearch
	.p2align	4, 0x90
	.type	binarySearch,@function
binarySearch:                           # @binarySearch
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movq	%rdi, -32(%rbp)
	movl	%esi, -16(%rbp)
	movl	%edx, -36(%rbp)
	movl	$0, -12(%rbp)
	decl	%edx
	movl	%edx, -8(%rbp)
	movb	$0, -1(%rbp)
	movl	$-1, -20(%rbp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_4:                                # %if.then23
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rax), %eax
	movl	%eax, -20(%rbp)
	movb	$1, -1(%rbp)
.LBB0_1:                                # %while.cond3
                                        # =>This Inner Loop Header: Depth=1
	cmpb	$1, -1(%rbp)
	je	.LBB0_8
# %bb.2:                                # %while.cond3
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	-8(%rbp), %eax
	cmpl	%eax, -12(%rbp)
	jg	.LBB0_8
# %bb.3:                                # %while.body4
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	-12(%rbp), %eax
	addl	-8(%rbp), %eax
	movl	%eax, %ecx
	shrl	$31, %ecx
	addl	%eax, %ecx
	sarl	%ecx
	movq	%rsp, %rdx
	leaq	-16(%rdx), %rax
	movq	%rax, %rsp
	movl	%ecx, -16(%rdx)
	movslq	%ecx, %rcx
	movq	-32(%rbp), %rdx
	movl	(%rdx,%rcx,4), %edx
	movq	%rsp, %rsi
	leaq	-16(%rsi), %rcx
	movq	%rcx, %rsp
	movl	%edx, -16(%rsi)
	cmpl	-16(%rbp), %edx
	je	.LBB0_4
# %bb.5:                                # %if.else25
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rcx), %ecx
	cmpl	-16(%rbp), %ecx
	jge	.LBB0_7
# %bb.6:                                # %if.then30
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rax), %eax
	incl	%eax
	movl	%eax, -12(%rbp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_7:                                # %if.else32
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rax), %eax
	decl	%eax
	movl	%eax, -8(%rbp)
	jmp	.LBB0_1
.LBB0_8:                                # %while.end5
	movl	-20(%rbp), %eax
	movq	%rbp, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	binarySearch, .Lfunc_end0-binarySearch
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	.array1@GOTPCREL(%rip), %rdi
	movq	%rdi, 16(%rsp)
	movl	$13, 4(%rsp)
	movl	$13, %esi
	movl	$10, %edx
	callq	binarySearch@PLT
	movl	%eax, 8(%rsp)
	cmpl	$-1, %eax
	je	.LBB1_2
# %bb.1:                                # %if.then6
	movl	$.L.str.1, %edi
	callq	print_string@PLT
	movl	4(%rsp), %edi
	callq	print_int@PLT
	movl	$.L.str.2, %edi
	callq	print_string@PLT
	movl	8(%rsp), %edi
	callq	print_int@PLT
	movl	$.L.str.3, %edi
	jmp	.LBB1_3
.LBB1_2:                                # %if.else8
	movl	$.L.str.4, %edi
	callq	print_string@PLT
	movl	4(%rsp), %edi
	callq	print_int@PLT
	movl	$.L.str.5, %edi
.LBB1_3:                                # %if.end7
	callq	print_string@PLT
	movl	$0, 12(%rsp)
	xorl	%eax, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	.L.str.5,@object                # @.str.5
	.data
	.p2align	4
.L.str.5:
	.asciz	" not found in the array.\n"
	.size	.L.str.5, 26

	.type	.L.str.4,@object                # @.str.4
.L.str.4:
	.asciz	"Element "
	.size	.L.str.4, 9

	.type	.L.str.3,@object                # @.str.3
.L.str.3:
	.asciz	".\n"
	.size	.L.str.3, 3

	.type	.L.str.2,@object                # @.str.2
	.p2align	4
.L.str.2:
	.asciz	" found at index "
	.size	.L.str.2, 17

	.type	.L.str.1,@object                # @.str.1
.L.str.1:
	.asciz	"Element "
	.size	.L.str.1, 9

	.type	.array1,@object                 # @.array1
	.globl	.array1
	.p2align	4
.array1:
	.long	1                               # 0x1
	.long	3                               # 0x3
	.long	5                               # 0x5
	.long	7                               # 0x7
	.long	9                               # 0x9
	.long	11                              # 0xb
	.long	13                              # 0xd
	.long	15                              # 0xf
	.long	17                              # 0x11
	.long	19                              # 0x13
	.size	.array1, 40

	.section	".note.GNU-stack","",@progbits
