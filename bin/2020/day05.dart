import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

const int MAX_FIELDS = 8;
const int MIN_FIELDS = 7;

final List<String> TEST_INPUT =
    File('./2020/data/day05-test.txt').readAsLinesSync();

final List<String> MAIN_INPUT = File('./2020/data/day05.txt').readAsLinesSync();

typedef bool IsValidPassportFn(Map<String, String> p);

const ROW_RANGE = Range(0, 127);
const COLUMN_RANGE = Range(0, 7);

class Range {
  final upper;
  final int lower;
  const Range(this.lower, this.upper);

  //~/ is integer division
  double _midPoint() => (lower + upper) / 2;

  Range lowerHalf() => Range(lower, _midPoint().floor());
  Range upperHalf() => Range(_midPoint().ceil(), upper);

  @override
  String toString() => 'lower: $lower, upper: $upper';
}

int findRow(String passRows) {
  if (DEBUG) print(passRows);
  var result = ROW_RANGE;

  passRows.split('').forEach((direction) {
    if (DEBUG) print(result);
    switch (direction) {
      case 'F':
        result = result.lowerHalf();
        break;
      case 'B':
        result = result.upperHalf();
        break;
      default:
        if (DEBUG) print('invalid direction for row');
        return 0;
    }
    if (DEBUG) print('$direction: $result');
  });

  if (DEBUG) print(passRows[passRows.length - 1]);
  return passRows[passRows.length - 1] == 'F' ? result.lower : result.upper;
}

int findColumn(String passColumns) {
  if (DEBUG) print(passColumns);
  var result = COLUMN_RANGE;
  passColumns.split('').forEach((direction) {
    if (DEBUG) print(result);
    switch (direction) {
      case 'R':
        result = result.upperHalf();
        break;
      case 'L':
        result = result.lowerHalf();
        break;
      default:
        print('invalid direction for column');
        return 0;
    }
    if (DEBUG) print('$direction: $result');
  });
  if (DEBUG) print(passColumns[passColumns.length - 1]);
  return passColumns[passColumns.length - 1] == 'L'
      ? result.lower
      : result.upper;
}

int findHighestSeatId(List<String> boardingPasses) {
  var result = 0;
  boardingPasses.forEach((line) {
    if (line.length == 10) {
      var row = findRow(line.substring(0, 7));
      var column = findColumn(line.substring(7, 10));
      var seatId = (row * 8) + column;
      if (seatId > result) result = seatId;
      if (DEBUG) print('$line: row $row, column: $column, seat ID $seatId');
    } else {
      print('Wrong length: $line');
    }
  });
  return result;
}

void test5a() {
  printHeader('5a test');
  print(findHighestSeatId(TEST_INPUT));
}

void test5b() {
  printHeader('5b test');
}

void day5a() {
  printHeader('5a');
  print(findHighestSeatId(MAIN_INPUT));
}

void day5b() {
  printHeader('5b');
}
