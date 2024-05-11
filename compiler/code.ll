define i32 @main(i32 %args) {
entry:
   %x1 = alloca i32
   store i32 %args, i32* %x1
   %x = alloca i32
   store i32 0, i32* %x
   br label %while.cond2
while.cond2:
   %x5 = load i32, i32* %x
   %x6 = icmp slt i32 %x5, 10
   br i1 %x6, label %while.body3, label %while.end4
while.body3:
   %x7 = load i32, i32* %x
   call void @print_int(i32 %x7)
   %x8 = load i32, i32* %x
   %x9 = add i32 %x8, 1
   store i32 %x9, i32* %x
   br label %while.cond2
while.end4:
   ret i32 0
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)