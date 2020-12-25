import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

//Using cube coordinates: see https://www.redblobgames.com/grids/hexagons/
class Direction {
  static const List<String> moveOptions = ['ne', 'e', 'se', 'sw', 'w', 'nw'];
  static final Map<String, Direction> moveVectors = {
    moveOptions[0]: Direction(1, 0, -1), //ne
    moveOptions[1]: Direction(1, -1, 0), //e
    moveOptions[2]: Direction(0, -1, 1), //se
    moveOptions[3]: Direction(-1, 0, 1), //sw
    moveOptions[4]: Direction(-1, 1, 0), //w
    moveOptions[5]: Direction(0, 1, -1) //nw
  };

  final int x, y, z;
  Direction([this.x = 0, this.y = 0, this.z = 0]);
  Direction move(location, instruction) {
    // print('$location, $instruction, ${moveVectors[instruction]}');
    var r = location + moveVectors[instruction];
    return r;
  }

  Direction operator +(Direction v) => Direction(x + v.x, y + v.y, z + v.z);

  @override
  String toString() => '$x, $y, $z';
}

class Floor {
  final List<String> input;
  List<List<String>> moveDirections = [];

  Floor(this.input) {
    parseInput();
    print(Direction.moveVectors);
  }

  int doFlips() {
    var blackTiles = <String>{};

    moveDirections.forEach((md) {
      var location = Direction();
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

  int artShow(int days) {
    for (var i = 0; i < days; i++) {
      //todo
    }
  }

  void parseInput() {
    String findDirection(t) {
      for (var op in Direction.moveOptions) {
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

void runPart1(String name, List input) {
  printHeader(name);
  // var floor = Floor(['esew']);
  // var floor = Floor(['nwwswee']);
  var floor = Floor(input);
  print(floor.doFlips());
}

void runPart2(String name, List input, days) {
  printHeader(name);
  var floor = Floor(input);
  floor.doFlips();
  print(floor.artShow(100));
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day24-test.txt');
  MAIN_INPUT = fileAsString('../data/day24.txt');

  //Answer: 10
  runPart1('24 test part 1', TEST_INPUT);
  //Answer: 2208
  runPart2('24 test part 2', TEST_INPUT, 100);

  //Answer: 346
  runPart1('24 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('24 part 2', MAIN_INPUT);
}
