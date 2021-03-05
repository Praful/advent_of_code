import 'dart:io';
import '../../shared/dart/src/utils.dart';

class Vector {
  final int x;
  final int y;
  const Vector(this.x, this.y);

  @override
  String toString() {
    return 'x = $x, y = $y';
  }
}

const bool DEBUG = false;
const String TREE = '#';

final List<String> TEST_COURSE =
    File('../data/day03-test.txt').readAsLinesSync();
final List<String> MAIN_COURSE = File('../data/day03.txt').readAsLinesSync();

const Vector FIRST_SLOPE = Vector(1, 3);

List<Vector> ALL_COURSE_SLOPES = [
  Vector(1, 1),
  Vector(1, 3),
  Vector(1, 5),
  Vector(1, 7),
  Vector(2, 1)
];

void test3a() {
  printHeader('3a test');
  var treeCount = treesOnCourse(TEST_COURSE, FIRST_SLOPE);
  print('Test trees encountered: $treeCount');
  assert(treeCount == 7);
}

void test3b() {
  printHeader('3b test');
  var result = treesForMultipleSlopes(ALL_COURSE_SLOPES, TEST_COURSE);
  print('Trees multiplied = $result');
  assert(result == 336);
}

void day3a() {
  printHeader('3a');
  print('Trees encountered: ${treesOnCourse(MAIN_COURSE, FIRST_SLOPE)}');
}

void day3b() {
  printHeader('3b');
  var result = treesForMultipleSlopes(ALL_COURSE_SLOPES, MAIN_COURSE);
  print('Trees multiplied = $result');
}

int treesForMultipleSlopes(
    final List<Vector> slopes, final List<String> course) {
  var result = 1;
  for (var slope in slopes) {
    var treeCount = treesOnCourse(course, slope);
    if (DEBUG) print('trees encountered for $slope: $treeCount');
    result = result * treeCount;
  }
  return result;
}

int treesOnCourse(final List<String> course, final Vector slope) {
  var courseWidth = course[0].length;
  if (DEBUG) {
    print('course length ${course.length}\ncourse width $courseWidth');
  }

  Vector nextLocation(final Vector current) {
    var x = current.x + slope.x;
    var y = current.y + slope.y;

    //wraparound since course repeats horizontally
    if (y >= courseWidth) y = y - courseWidth;

    return Vector(x, y);
  }

  bool isTree(Vector location) => (TREE == course[location.x][location.y]);
  bool endOfCourse(int current, int end) => (current >= end);

  var location = slope;
  var treeCount = 0;

  while (!endOfCourse(location.x, course.length)) {
    if (DEBUG) print(location);
    if (isTree(location)) treeCount++;

    location = nextLocation(location);
  }
  return treeCount;
}

void main(List<String> args) {
  test3a();
  test3b();

  day3a();
  day3b();
}
