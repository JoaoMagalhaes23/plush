
function bubbleSort(val arr: [int], val size: int): [int] {
    var swapped : int := 1;
    while swapped = 1 {
        swapped := 0;
        var i: int := 0;
        while i < size-1 {
            if arr[i] > arr[i+1] {
                val temp : int := arr[i];
                arr[i] := arr[i+1];
                arr[i+1] := temp;
                swapped := 1;
            }
            i := i + 1;
        }
    }
}
# tying to pass a float to a int
function main(val args:[string]) {
    val arr : [int] := [64, 34, 25, 12, 22, 11, 90];
    val size : int := 7.6;
    val res : [int] := bubbleSort(arr, size);
    var i : int := 0;
    while i < size {
        print_int(res[i]);
        i := i + 1;
    }
}
