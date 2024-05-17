function fizzBuzz(var mi: int, val ma: int) : string {
    var s : string := "";
    while mi <= ma {
        if (mi % 3) = 0 {
            s := concatenate_strings(s, "Fizz");
        }
        else if (mi % 4) = 0 {
            s := concatenate_strings(s, "Buzz");
        }
        else if ((mi % 3) != 0) && ((mi % 4) != 0) {
            s := concatenate_strings(s, int_to_string(mi));  
        }
        mi := mi + 1;
    }
    fizzBuzz := s;
}
# The return type of fizzBuzz is string, but the type of result is int
function main(val args:[string]): int {
    val result : int := fizzBuzz(1, 10);
    print_string(result);
    main := 0;
}