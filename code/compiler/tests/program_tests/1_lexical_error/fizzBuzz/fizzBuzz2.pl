# The | is not the correct form to represent an or
function fizzBuzz(var mi, val ma: int) : string {
    var s : string := "";
    while mi <= ma | mi > 0 {
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
    fizzBuzz := s;
}
function main(val args:[string]) {
    val result : string := fizzBuzz(4, 100);
    print_string(result);
}