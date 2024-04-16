val actual_min : int := -9;
val actual_max : int := 9;

function maxRangeSquared(var mi:int, val ma:int) : int {
	# question mark after the operation is not allowed
	var current_max : int := mi ^? 2;
	while mi <= ma {
		int current_candidate : int := mi ^ 2;
		if current_candidate > current_max {
			current_max := current_candidate;
		}
	} 
	maxRangeSquared := current_max; # This line returns the current max!
}


function main(val args:[string]) {
	val result : int := maxRangeSquared(actual_min, actual_max);
	print_int(result);
}