import 'dart:io';
import './utils.dart';

//Add the following to pubspec.yaml for the DeepEquality feature
// dependencies:
//   collection: any
import 'package:collection/collection.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

//Add these vectors to a cell to reach its adjacent cells.
List toGrid(String input) {
  return File(input).readAsLinesSync().map((e) => e.split('')).toList();
}

class Seating {
  static const MAX_ROUNDS = 1000000;
  static const String LOCATION_EMPTY_SEAT = 'L';
  static const String LOCATION_OCCUPIED_SEAT = '#';
  static const String LOCATION_FLOOR = '.';
  static const List MOVE_DIRECTION = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
  ];

  List grid;
  Seating(this.grid);

// If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
// If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
// Otherwise, the seat's state does not change.
  List nextRound(input, [recurseSearch = false, occupiedCount = 4]) {
    var rowCount = input.length;
    var colCount = input[0].length;
    var result =
        List.generate(rowCount, (i) => List(colCount), growable: false);
    // print(result);
    for (var r = 0; r < rowCount; r++) {
      for (var c = 0; c < colCount; c++) {
        var oldValue = input[r][c];
        var newValue = oldValue;
        switch (oldValue) {
          case LOCATION_EMPTY_SEAT:
            if (adjacentOccupied(input, r, c, recurseSearch) == 0) {
              newValue = LOCATION_OCCUPIED_SEAT;
            }
            break;
          case LOCATION_OCCUPIED_SEAT:
            if (adjacentOccupied(input, r, c, recurseSearch) >= occupiedCount) {
              newValue = LOCATION_EMPTY_SEAT;
            }
            break;
          case LOCATION_FLOOR:
            break;
          default:
        }
        result[r][c] = newValue;
      }
    }
    return result;
  }

  int adjacentOccupied(grid, row, col, [recurseSearch = false]) {
    var result = 0, safetyCounter = 0;

    bool inGrid(r, c) =>
        r >= 0 && r < grid.length && c >= 0 && c < grid[0].length;

    MOVE_DIRECTION.forEach((direction) {
      var adjR = row, adjC = col;
      do {
        if (safetyCounter++ > MAX_ROUNDS) throw 'loop appears infinite';
        adjR += direction[0];
        adjC += direction[1];
        if (!inGrid(adjR, adjC)) break;
        if (grid[adjR][adjC] == LOCATION_EMPTY_SEAT) break;
        if (grid[adjR][adjC] == LOCATION_OCCUPIED_SEAT) {
          result++;
          break;
        }
      } while (recurseSearch);
    });

    return result;
  }

  //Repeat rounds until there is no change.
  //Return seats occupied.
  int repeatRounds([recurseSearch = false, occupiedCount = 4]) {
    var currentGrid = grid;
    var nextGrid;
    var safetyCounter = 0;
    do {
      if (safetyCounter++ > MAX_ROUNDS) throw 'loop appears infinite';
      nextGrid = nextRound(currentGrid, recurseSearch, occupiedCount);
      if (sameGrid(currentGrid, nextGrid)) {
        return occupiedSeatCount(nextGrid);
      } else {
        currentGrid = nextGrid;
      }
    } while (true);
  }

  bool sameGrid(List currentGrid, nextGrid) =>
      DeepCollectionEquality().equals(currentGrid, nextGrid);

  int occupiedSeatCount(grid) => grid.fold(0,
      (total, r) => total + r.where((c) => c == LOCATION_OCCUPIED_SEAT).length);
}

void runPart1(String name, List input) {
  printHeader(name);
  var seating = Seating(input);
  print(seating.repeatRounds());
}

void runPart2(String name, List input) {
  printHeader(name);
  var seating = Seating(input);
  print(seating.repeatRounds(true, 5));
}

void main(List<String> arguments) {
  TEST_INPUT = toGrid('../data/day11-test.txt');
  MAIN_INPUT = toGrid('../data/day11.txt');

  //Answer: 37
  runPart1('11 test part 1', TEST_INPUT);
  //Answer: 26
  runPart2('11 test part 2', TEST_INPUT);

  //Answer: 2386
  runPart1('11 part 1', MAIN_INPUT);
  //Answer: 2091
  runPart2('11 part 2', MAIN_INPUT);
}
