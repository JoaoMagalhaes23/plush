@y = global i32 1
define i32 @main(i32 %args) {
entry:
   %x1 = alloca i32
   store i32 %args, i32* %x1
  %x2 = icmp sgt i1 1, 2
  %x3 = or i1 %x2, true
   %x = alloca i1
   store i1 %x3, i1* %x
   %x4 = load i1, i1* %x
   call void @print_boolean(i1 %x4)
   ret i32 1
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)