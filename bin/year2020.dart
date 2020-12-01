import 'dart:async';
import 'dart:io';

//Find two numbers that add to 2020 and print their product
void day1a() {
  print('day1a');

  var lines = File('./data/day1a.txt').readAsLinesSync();
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

//Find three numbers that add to 2020 and print their product
void day1b() {
  print('day1b');

  var lines = File('./data/day1a.txt').readAsLinesSync();
  var unique = Set.from(lines);
  var target = 2020;
  for (var num1 in lines) {
    var n1 = int.parse(num1);
    for (var num2 in lines) {
      var n2 = int.parse(num2);
      var twoNumsSummed = n1 + n2;
      if (twoNumsSummed < target) {
        var required = target - twoNumsSummed;
        if (unique.contains(required.toString())) {
          print('$n1 * $n2 * $required = ${n1 * n2 * required}');
          return;
        }
      }
    }
  }
}
