function fib(val n: int): int {
	if n <= 1 {
		fib := n;
	}
	else {
		fib := fib(n - 1) + fib(n - 2);
	}
}
function main(): int {
	var n : int := 9;
	print_int(n);
	print_string("th Fibonacci Number: ");
	print_int(fib(n));
	main := 0;
}

