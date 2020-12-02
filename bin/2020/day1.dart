import 'dart:io';
import '../utils.dart';

var verbose = true;
var debug = true;

var lines = File('./2020/data/day1a.txt').readAsLinesSync();

//Find three numbers that add to 2020 and print their product
void day1b() {
  printDay('1b');

  var numbers = lines.map(int.parse).toList();

  var unique = Set.from(numbers);
  var target = 2020;
  for (var n1 in numbers) {
    for (var n2 in numbers) {
      var twoNumsSummed = n1 + n2;
      if (twoNumsSummed < target) {
        var required = target - twoNumsSummed;
        if (unique.contains(required)) {
          print('$n1 * $n2 * $required = ${n1 * n2 * required}');
          return;
        }
      }
    }
  }
}

//Find two numbers that add to 2020 and print their product
void day1a() {
  printDay('1a');

  var unique = Set.from(lines);
  var target = 2020;
  for (var num1 in lines) {
    var n1 = int.parse(num1);
    var required = target - n1;
    if (unique.contains(required.toString())) {
      print('$num1 * $required = ${n1 * required}');
      return;
    }
  }
}
