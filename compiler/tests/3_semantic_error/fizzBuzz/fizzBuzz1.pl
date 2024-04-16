# The return type and the type of mi are missmatched
function fizzBuzz(var mi, val ma: int) : string {
    var s : string := "";
    while mi <= ma {
        if mi % 3 = 0 {
            s := s + "Fizz";
        }
        if mi % 4 = 0 {
            s := s + "Buzz";
        }
        if mi % 3 != 0 && mi % 4 != 0 {
            s := s + mi;
        }
        print_string(s);
        mi := mi + 1;
    }
    fizzBuzz := mi;
}

function main(val args:[string]) {
    val result : string := fizzBuzz(1, 100);
    print_string(result);
}