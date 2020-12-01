import 'dart:async';
import 'dart:io';

//Find three numbers that add to 2020 and print their product
void day1b() {
  print('day1b');

  var lines = File('./data/day1a.txt').readAsLinesSync();
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
