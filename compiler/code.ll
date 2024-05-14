@.array1 = global [2 x i32] [i32 1, i32 2]
@.array2 = global [3 x i32] [i32 3, i32 4, i32 5]
@.array3 = global [2 x i32*] [i32* getelementptr inbounds ([2 x i32], [2 x i32]* @.array1, i64 0, i64 0), i32* getelementptr inbounds ([3 x i32], [3 x i32]* @.array2, i64 0, i64 0)]
@e = unnamed_addr global i32** getelementptr inbounds ([2 x i32*], [2 x i32*]* @.array3, i64 0, i64 0)
define i32 @main(i32 %args) {
entry:
   %x4 = alloca i32
   store i32 %args, i32* %x4
   %x5 = load i32**, i32*** @e
   call void @print_2d_int_array(i32** %x5, i32 2, i32 5)
   ret i32 1
}
declare void @print_int(i32)
declare void @print_string(i8*)
declare void @print_boolean(i1)
declare void @print_int_array(i32*, i32)
declare void @print_2d_int_array(i32**, i32, i32)