val actual_min : int := -9;
val actual_max : int := 9;

function maxRangeSquared(var mi:int, val ma:int) : int;

function maxRangeSquared(var mi:int, val ma:int) : int {
	var current_max : int := actual_min ^ 2;
	while actual_min <= actual_max {
		val current_candidate : int := actual_min ^ 2;
		if current_candidate > current_max {
			current_max := current_candidate;
		}
	} 
}

function main(val args:[string]): int {
	val result : int := maxRangeSquared(actual_min, 1, 4);
}
