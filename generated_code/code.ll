@.str.5 = private unnamed_addr global [26 x i8] c" not found in the array.
\00"
@.str.4 = private unnamed_addr global [9 x i8] c"Element \00"
@.str.3 = private unnamed_addr global [3 x i8] c".
\00"
@.str.2 = private unnamed_addr global [17 x i8] c" found at index \00"
@.str.1 = private unnamed_addr global [9 x i8] c"Element \00"
@.array1 = global [10 x i32] [i32 1, i32 3, i32 5, i32 7, i32 9, i32 11, i32 13, i32 15, i32 17, i32 19]
define i32 @binarySearch(i32* %arr, i32 %target, i32 %size) {
entry:
   %retval = alloca i32
   %arr.addr = alloca i32*
   store i32* %arr, i32** %arr.addr
   %target.addr = alloca i32
   store i32 %target, i32* %target.addr
   %size.addr = alloca i32
   store i32 %size, i32* %size.addr
   %low = alloca i32
   store i32 0, i32* %low
   %x1 = load i32, i32* %size.addr
   %x2 = sub i32 %x1, 1
   %high = alloca i32
   store i32 %x2, i32* %high
   %can_return = alloca i1
   store i1 false, i1* %can_return
   store i32 -1, i32* %retval
   br label %while.cond3
while.cond3:
   %x6 = load i1, i1* %can_return
   %x7 = xor i1 %x6, true
   %x8 = load i32, i32* %low
   %x9 = load i32, i32* %high
   %x10 = icmp sle i32 %x8, %x9
   %x11 = and i1 %x7, %x10
   br i1 %x11, label %while.body4, label %while.end5
while.body4:
   %x12 = load i32, i32* %low
   %x13 = load i32, i32* %high
   %x14 = add i32 %x12, %x13
   %x15 = sdiv i32 %x14, 2
   %mid = alloca i32
   store i32 %x15, i32* %mid
   %x16 = load i32, i32* %mid
   %x17 = load i32*, i32** %arr.addr
   %index.ptr18 = getelementptr inbounds i32, i32* %x17, i32 %x16
   %arrayidx19 = load i32, i32* %index.ptr18
   %mid_idx = alloca i32
   store i32 %arrayidx19, i32* %mid_idx
   %x20 = load i32, i32* %mid_idx
   %x21 = load i32, i32* %target.addr
   %x22 = icmp eq i32 %x20, %x21
   br i1 %x22, label %if.then23, label %if.else25
if.then23:
   %x26 = load i32, i32* %mid
   store i32 %x26, i32* %retval
   store i1 true, i1* %can_return
   br label %if.end24
if.else25:
   %x27 = load i32, i32* %mid_idx
   %x28 = load i32, i32* %target.addr
   %x29 = icmp slt i32 %x27, %x28
   br i1 %x29, label %if.then30, label %if.else32
if.then30:
   %x33 = load i32, i32* %mid
   %x34 = add i32 %x33, 1
   store i32 %x34, i32* %low
   br label %if.end31
if.else32:
   %x35 = load i32, i32* %mid
   %x36 = sub i32 %x35, 1
   store i32 %x36, i32* %high
   br label %if.end31
if.end31:
   br label %if.end24
if.end24:
   br label %while.cond3
while.end5:
   %x37 = load i32, i32* %retval
   ret i32 %x37
}
define i32 @main(i8** %args) {
entry:
   %retval = alloca i32
   %args.addr = alloca i8**
   store i8** %args, i8*** %args.addr
   %arr = alloca i32*
   store i32* getelementptr inbounds ([10 x i32], [10 x i32]* @.array1, i64 0, i64 0), i32** %arr
   %target = alloca i32
   store i32 13, i32* %target
   %x1 = load i32*, i32** %arr
   %x2 = load i32, i32* %target
   %x3 = call i32 @binarySearch(i32* %x1, i32 %x2, i32 10)
   %index = alloca i32
   store i32 %x3, i32* %index
   %x4 = load i32, i32* %index
   %x5 = icmp ne i32 %x4, -1
   br i1 %x5, label %if.then6, label %if.else8
if.then6:
   call void @print_string(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str.1, i64 0, i64 0))
   %x9 = load i32, i32* %target
   call void @print_int(i32 %x9)
   call void @print_string(i8* getelementptr inbounds ([17 x i8], [17 x i8]* @.str.2, i64 0, i64 0))
   %x10 = load i32, i32* %index
   call void @print_int(i32 %x10)
   call void @print_string(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.3, i64 0, i64 0))
   br label %if.end7
if.else8:
   call void @print_string(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.str.4, i64 0, i64 0))
   %x11 = load i32, i32* %target
   call void @print_int(i32 %x11)
   call void @print_string(i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.5, i64 0, i64 0))
   br label %if.end7
if.end7:
   store i32 0, i32* %retval
   %x12 = load i32, i32* %retval
   ret i32 %x12
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)
declare void @print_float(float)
declare void @print_int_array(i32*, i32)
declare void @print_2d_int_array(i32**, i32, i32)
declare i8* @concatenate_strings(i8*, i8*)
declare i8* @int_to_string(i32)