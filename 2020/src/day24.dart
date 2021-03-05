import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

//Using cube coordinates: see https://www.redblobgames.com/grids/hexagons/
class Location {
  static const List<String> moveOptions = ['ne', 'e', 'se', 'sw', 'w', 'nw'];
  static final Map<String, Location> moveVectors = {
    moveOptions[0]: Location(1, 0, -1), //ne
    moveOptions[1]: Location(1, -1, 0), //e
    moveOptions[2]: Location(0, -1, 1), //se
    moveOptions[3]: Location(-1, 0, 1), //sw
    moveOptions[4]: Location(-1, 1, 0), //w
    moveOptions[5]: Location(0, 1, -1) //nw
  };

  final int x, y, z;
  Location([this.x = 0, this.y = 0, this.z = 0]);
  Location move(location, instruction) {
    // print('$location, $instruction, ${moveVectors[instruction]}');
    var r = location + moveVectors[instruction];
    return r;
  }

  Location operator +(Location v) => Location(x + v.x, y + v.y, z + v.z);

  @override
  String toString() => '$x, $y, $z';

  static Location parse(s) {
    var coords = s.split(',').map(int.parse).toList();
    return Location(coords[0], coords[1], coords[2]);
  }
}

class Floor {
  final List<String> input;
  List<List<String>> moveDirections = [];
  var blackTiles = <String>{};

  Floor(this.input) {
    parseInput();
  }

  int doFlips() {
    moveDirections.forEach((md) {
      var location = Location();
      md.forEach((instruction) {
        if (DEBUG) print('before: $location');
        location = location.move(location, instruction);
        if (DEBUG) print('-> $instruction result: $location');
      });
      var dirAsStr = location.toString();
      if (blackTiles.contains(dirAsStr)) {
        blackTiles.remove(dirAsStr);
      } else {
        blackTiles.add(dirAsStr);
      }
    });

    // print(blackTiles);
    return blackTiles.length;
  }

  int adjacentBlackTiles(Set blackTiles, Location tile) {
    var result = 0;
    Location.moveVectors.values.forEach((side) {
      if (blackTiles.contains((tile + side).toString())) result++;
    });
    return result;
  }

  List<Location> findWhiteTilesThatNeedFlipping(blackTiles) {
    bool isWhite(t) => !blackTiles.contains(t.toString());

    var result = <Location>[];
    blackTiles.forEach((blackAsStr) {
      var black = Location.parse(blackAsStr);
      Location.moveVectors.values.forEach((side) {
        var adjTile = black + side;
        if (isWhite(adjTile) && adjacentBlackTiles(blackTiles, adjTile) == 2) {
          result.add(adjTile);
        }
      });
    });
    return result;
  }

  int artShow(int days) {
    var nextDaysBlackTiles = blackTiles;

    for (var i = 0; i < days; i++) {
      var daysBlackTiles = nextDaysBlackTiles;
      nextDaysBlackTiles = <String>{};

      daysBlackTiles.forEach((tile) {
        var adjBlackTiles =
            adjacentBlackTiles(daysBlackTiles, Location.parse(tile));
        if (adjBlackTiles.isBetween(1, 2)) {
          nextDaysBlackTiles.add(tile.toString());
        }
        var flipWhite = findWhiteTilesThatNeedFlipping(daysBlackTiles);
        nextDaysBlackTiles.addAll(flipWhite.map((t) => t.toString()));
      });

      print('day $i: ${nextDaysBlackTiles.length} ---- ');
    }
    return nextDaysBlackTiles.length;
  }

  void parseInput() {
    String findDirection(t) {
      for (var op in Location.moveOptions) {
        if (t.startsWith(op)) return op;
      }
      throw 'Direction not found in instructions $t';
    }

    input.forEach((t) {
      var directions = <String>[];
      var instructions = t;
      while (instructions.isNotEmpty) {
        var dir = findDirection(instructions);
        directions.add(dir);
        instructions = instructions.substring(dir.length);
      }
      moveDirections.add(directions);
    });
  }
}

void runPart1(String name, List<String> input) {
  printHeader(name);
  // var floor = Floor(['esew']);
  // var floor = Floor(['nwwswee']);
  var floor = Floor(input);
  print(floor.doFlips());
}

void runPart2(String name, List<String> input, days) {
  printHeader(name);
  var floor = Floor(input);
  floor.doFlips();
  print(floor.artShow(days));
}

void main(List<String> arguments) {
  var TEST_INPUT = FileUtils.asLines('../data/day24-test.txt');
  var MAIN_INPUT = FileUtils.asLines('../data/day24.txt');

  //Answer: 10
  runPart1('24 test part 1', TEST_INPUT);
  //Answer: 2208
  runPart2('24 test part 2', TEST_INPUT, 100);

  //Answer: 346
  runPart1('24 part 1', MAIN_INPUT);
  //Answer: 3802
  runPart2('24 part 2', MAIN_INPUT, 100);
}
