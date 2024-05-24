function fib_tail_call(val n:int, val a:int, val b: int): int {
	if n = 0 {
		fib_tail_call := a;
	}
	if n = 1 {
		fib_tail_call := b;
	}
	else {
		fib_tail_call := fib_tail_call(n - 1, b, a + b);
	}

}

function main(): int {
	var n : int := 9;
	print_int(n);
	print_string("th Fibonacci Number: ");
	print_int(fib_tail_call(n, 0, 1));
	print_string("\n");
	main := 0;
}

