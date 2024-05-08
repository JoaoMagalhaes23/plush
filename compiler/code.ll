define i32 @x() {
entry:
   ret i32 1
}
define i32 @main(i32 %args) {
entry:
   %x1 = alloca i32
   store i32 %args, i32* %x1
   %x = alloca i32
   store i32 1, i32* %x
   %x2 = load i32, i32* %x
   call void @print_int(i32 %x2)
   ret i32 1
}
declare void @print_int(i32)
declare void @print_string(i8*)