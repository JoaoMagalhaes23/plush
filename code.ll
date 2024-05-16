@b = unnamed_addr global i32 -1
define i32 @main(i32 %a) {
entry:
   %retval = alloca i32
   %a.addr = alloca i32
   store i32 %a, i32* %a.addr
   %x1 = load i32, i32* @b
   %x2 = sub i32 0, %x1
   %c = alloca i32
   store i32 %x2, i32* %c
   %x3 = load i32, i32* @b
   call void @print_int(i32 %x3)
   %x4 = load i32, i32* %c
   call void @print_int(i32 %x4)
   %x5 = load i32, i32* %retval
   ret i32 %x5
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)
declare void @print_int_array(i32*, i32)
declare void @print_2d_int_array(i32**, i32, i32)
declare i8* @concatenate_strings(i8*, i8*)
declare i8* @int_to_string(i32)