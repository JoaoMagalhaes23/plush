function assign_array(var aa: [[int]]): void {
	aa[0] := {7,8};
	print_2d_int_array(aa, 2, 2);
}
function main(): int {
	val aa: [[int]] := {{1,2},{3,6}};
	assign_array(aa);
	print_2d_int_array(aa, 2, 2);
}