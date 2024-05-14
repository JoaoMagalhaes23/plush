@__const.square.arr1 =  [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
@x = unnamed_addr global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
define i32 @main(i32 %args) {
entry:
   %x2 = alloca i32
   store i32 %args, i32* %x2
   %x3 = load [5 x i32], [5 x i32]* @x
   call void @print_int_array([5 x i32] %x3, i32 5)
   ret i32 1
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)
declare void @print_int_array(i32*, i32)