define i32 @main() {
entry:
   %retval = alloca i32
   %actual_min = alloca float
   store float 0x400b333333333333, float* %actual_min
   %x1 = load float, float* %actual_min
   call void @print_float(float %x1)
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