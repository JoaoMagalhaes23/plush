function binarySearch(val arr: [int], val target: int, val size: int): int {
    var low : int := 0;
    var high : int := size - 1;
    while low <= high {
        val mid : int := (low + high) / 2;
        if arr[mid] = target {
            binarySearch := mid;
        } else if arr[mid] < target {
            low := mid + 1;
        } else {
            high := mid - 1;
        }
    }
    binarySearch := -1;
}

function main (val args:[string]) {
    val arr : [int] := [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
    val target : int := 13;
    val index : int := binarySearch(arr, target, 10);
    if index != -1 {
        print_string("Element ");
        print_int(target);
        print_string(" found at index ");
        print_int(index);
    } else {
        print_string("Element ");
        print_int(target);
        print_string(" not found in the array.");
    }
}