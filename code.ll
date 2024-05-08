@actual_min = global i32 9
define i32 @main(i32 noundef %args,i32 noundef %x) {
entry:
   store i32 7, i32* @actual_min
   %x1 = call void @print_int(i32 1)
   ret i32 1
}
declare void @print_int(i32 noundef)