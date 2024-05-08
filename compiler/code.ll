@actual_min = global i32 9
define i32 @main(i32 %args,i32 %x) {
entry:
   %x1 = alloca i32
   store i32 %args, i32* %x1
   %x2 = alloca i32
   store i32 %x, i32* %x2
   store i32 7, i32* @actual_min
   %x3 = load i32, i32* @actual_min
   call void @print_int(i32 %x3)
   ret i32 1
}
declare void @print_int(i32)