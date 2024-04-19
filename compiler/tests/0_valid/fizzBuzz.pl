function fizzBuzz(var mi: int, val ma: int) : string {
    var s : string := "";
    while mi <= ma {
        if mi % 3 = 0 {
            s := s + "Fizz";
        }
        else if mi % 4 = 0 {
            s := s + "Buzz";
        }
        else if mi % 3 != 0 && mi % 4 != 0 {
            s := s + mi;
        }
        print_string(s);
        mi := mi + 1;
    }
    fizzBuzz := s;
}

function main(val args:[string]): int {
    val result : string := fizzBuzz(1, 100);
    print_string(result);
    main := 0;
}