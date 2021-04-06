import 'dart:collection';
import 'dart:math' as math;
// import 'package:console/console.dart';
import 'package:collection/collection.dart';

import '../../shared/dart/src/utils.dart';
// import 'package:basics/basics.dart' hide NumIterableBasics;
// import 'package:tuple/tuple.dart';

// extension IterableNum<T extends num> on Iterable<T> {
//   T get max => reduce(math.max);
//   T get min => reduce(math.min);
//   T get sum => reduce((a, b) => a + b as T);
// }

void test1() {
  // print([1.2, 1.3, 5, 2.2].sum); //works
  print([1.2, 1.3, 5, 2.2].max); //works
  print([1.2, 1.3, 5.3, 2.2].min); //works
  print([1.2, 1.3, 5.0, 2.2].sum); //does not work

  //these don't work
  print([1, 2, 3].max);
  print([1, 2, 3].min);
  print([1, 2, 3].sum);
}

void test2() {
  print('eeeeddabcde'.where((c) => c == 'c').length);
}

void test3() {
  print(3.1450000001.compareTo(3.145000002));
}

void test4() {
  // double d = 2.3456789;
  var d = 5.550;
  var d1 = d.toPrecision(1); // 2.3
  var d2 = d.toPrecision(2); // 2.35
  var d3 = d.toPrecision(3); // 2.345
  var d4 = d.toPrecision(4); // 2.345
  print(d1);
  print(d2);
  print(d3);
  print(d4);
  print(d.toStringAsFixed(1));
  print(d.toStringAsFixed(2));
  print(d.toStringAsFixed(3));
  print(d.toStringAsFixed(4));
}

void test5() {
  var p1 = math.Point(11, 13);
  print(p1.distanceTo(math.Point(11, 2)));
  print(p1.distanceTo(math.Point(11, 3)));
  print(p1.distanceTo(math.Point(11, 4)));
  print(p1.distanceTo(math.Point(11, 5)));
  print(p1.distanceTo(math.Point(11, 6)));
  print(p1.distanceTo(math.Point(11, 7)));
  print(p1.distanceTo(math.Point(11, 8)));
  print(p1.distanceTo(math.Point(11, 9)));
  print(p1.distanceTo(math.Point(11, 10)));
  print(p1.distanceTo(math.Point(11, 11)));
  print(p1.distanceTo(math.Point(11, 12)));
  print(p1.distanceTo(math.Point(11, 14)));
  print(p1.distanceTo(math.Point(11, 16)));
  print(p1.distanceTo(math.Point(11, 17)));
}

enum Direction { north, east, south, west }
void test6() {
  print(Direction.values[0]);
  print('${-1 % 4}');
  // print(Direction.north.index);
  // print(Direction.west.index);
  var facing = Direction.north;
  print(Direction.values[(facing.index - 1) % 4]);
  print(Direction.values[(facing.index + 1) % 4]);
}

void test7() {
  var input = '<x=-8, y=-10, z=0>\n'
      '<x=5, y=5, z=10>\n'
      '<x=2, y=-7, z=3>\n '
      '<x=9, y=-8, z=-3>';

  // var regex = RegExp('x\=(?\<x\>-?\d*), y\=(?\<y\>-?\d*), z\=(?\<z\>-?\d*)\>');
  var regex = RegExp(r'x\=(?<x>-?\d*), y\=(?<y>-?\d*), z=(?<z>-?\d*)\>');
  // var match = regex.firstMatch(input);
  regex.allMatches(input).forEach((match) {
    print(match.namedGroup('x'));
    print(match.namedGroup('y'));
    print(match.namedGroup('z'));
  });
}

int roundUp(int numToRound, int multiple) {
  return ((numToRound + multiple - 1) ~/ multiple) * multiple;
}

void test8() {
  print(roundUp(8, 3));
  print(roundUp(3, 3));
  print(roundUp(2, 3));
  print(roundUp(1, 3));
  print(roundUp(8, 4));
}

// void test9() {
//   var cursor = Cursor();
//   //col, row
//   cursor.writeAt(0, 0, 'o');
//   cursor.writeAt(1, 1, '1');
//   cursor.writeAt(2, 2, '2');
// }

RegExp regexLowerCase = RegExp(r'^[a-z]$');
RegExp regexUpperCase = RegExp(r'^[A-Z]$');
bool isKey(String s) => regexLowerCase.hasMatch(s);
bool isLockedDoor(String s) => regexUpperCase.hasMatch(s);

void test10() {
  void check(s) {
    print('$s, key: ${isKey(s)}, lock: ${isLockedDoor(s)}');
  }

  check('a');
  check('B');
  check('~');
  check('4');
  check('Z');
  check('aa');
  check('BB');
}

void test11() {
  var a = HashSet<String>();
  a.add('a');
  a.add('b');

  var b = HashSet<String>();
  b.add('a');
  b.add('b');
  print(a.isEqualTo(b));
}

void test12() {
// IterableZip()
}

void main(List<String> args) {
  test12();
}
