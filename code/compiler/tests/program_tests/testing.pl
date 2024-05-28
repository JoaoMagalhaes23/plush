import "tests/program_tests/simple_operations_module.pl";

function main(val argc: int, val argv: [string]): int {
    print_int(argc);
    print_string("\n");
    print_string_array(argv, argc);
    print_string("\n");
    print_string_array({"aaaa", "aaaa"}, 2);
    print_string("\n");
}
