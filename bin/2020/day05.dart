import 'dart:io';
import '../utils.dart';

//Part 1 here is long-winded. After writing, I saw that treating each row as a binary
//representation (B, R=1 and F,L = 0) results in the largest binary number
//being the max seat ID.
//
//Part 2 has various solutions.

const bool DEBUG = false;

final List<String> TEST_INPUT =
    File('./2020/data/day05-test.txt').readAsLinesSync();

final List<String> MAIN_INPUT = File('./2020/data/day05.txt').readAsLinesSync();

const ROW_RANGE = Range(0, 127);
const COLUMN_RANGE = Range(0, 7);

class Range {
  final upper;
  final int lower;
  const Range(this.lower, this.upper);

  double _midPoint() => (lower + upper) / 2;
  Range lowerHalf() => Range(lower, _midPoint().floor());
  Range upperHalf() => Range(_midPoint().ceil(), upper);

  @override
  String toString() => 'lower: $lower, upper: $upper';
}

class SeatInfo {
  List<int> seatIDs;
  SeatInfo(this.seatIDs);
  int maxSeatID() => seatIDs.max;
  int minSeatID() => seatIDs.min;

  List<int> missingSeatIDs() {
    var result = <int>[];
    seatIDs.sort();
    var counter = minSeatID();
    seatIDs.forEach((id) {
      if (counter != id) {
        result.add(counter);
        counter = id;
      }
      counter++;
    });
    return result;
  }
}

int findRow(String passRows) {
  var result = ROW_RANGE;
  passRows.split('').forEach((direction) {
    var oldResult = result;
    switch (direction) {
      case 'F':
        result = result.lowerHalf();
        break;
      case 'B':
        result = result.upperHalf();
        break;
      default:
        print('invalid direction for row');
        return 0;
    }
    if (DEBUG) print('$oldResult: $direction => $result');
  });

  return result.lower;
}

int findColumn(String passColumns) {
  var result = COLUMN_RANGE;
  passColumns.split('').forEach((direction) {
    var oldResult = result;
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
    if (DEBUG) print('$oldResult: $direction => $result');
  });
  return result.lower;
}

SeatInfo findSeatInfo(List<String> boardingPasses) {
  var seatIDs = <int>[];
  boardingPasses.forEach((line) {
    if (line.length == 10) {
      var row = findRow(line.substring(0, 7));
      var column = findColumn(line.substring(7, 10));
      var seatId = (row * 8) + column;
      seatIDs.add(seatId);
      if (DEBUG) print('$line: row $row, column: $column, seat ID $seatId');
    } else {
      print('Wrong length for boarding pass: $line');
    }
  });
  return SeatInfo(seatIDs);
}

void test5() {
  printHeader('5a test');
  //answer 820
  print('Max seat ID: ${findSeatInfo(TEST_INPUT).maxSeatID()}');
}

void day5() {
  printHeader('5a');
  //answers 858 and 557
  var seatInfo = findSeatInfo(MAIN_INPUT);
  print('Max seat ID: ${seatInfo.maxSeatID()}');
  print('Missing seatIDs: ${seatInfo.missingSeatIDs()}');
}
