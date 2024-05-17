define i32 @main() {
entry:
   %retval = alloca i32
   %x = alloca i32
   store i32 4, i32* %x
   %x1 = load i32, i32* %x
   call void @print_int(i32 %x1)
   %x2 = load i32, i32* %retval
   ret i32 %x2
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)
declare void @print_float(float)
declare void @print_int_array(i32*, i32)
declare void @print_2d_int_array(i32**, i32, i32)
declare i8* @concatenate_strings(i8*, i8*)
declare i8* @int_to_string(i32)