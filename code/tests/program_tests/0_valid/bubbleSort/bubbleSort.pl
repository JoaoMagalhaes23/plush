function bubbleSort(var arr: [int], val size: int): [int] {
    var swapped : boolean := true;
    while swapped {
        swapped := false;
        var i: int := 0;
        while i < (size-1) {
            if arr[i] > arr[i+1] {
                val temp : int := arr[i];
                arr[i] := arr[i+1];
                arr[i+1] := temp;
                swapped := true;
            }
            i := i + 1;
        }
    }
}

function main(): int {
    val arr : [int] := {25, 12, 22, 11, 34, 64, 90};
    val size : int := 7;
    bubbleSort(arr, size);
    print_int_array(arr, size);
}
