import 'dart:math';
import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import '../../shared/dart/src/grid.dart';

/// Puzzle description: https://adventofcode.com/2019/day/17
///
/// The camera output, worked out in part 1 is:
///
/// ............................#######............
/// ............................#.....#............
/// ............................#.....#............
/// ............................#.....#............
/// ..........#.....#############.....#............
/// ..........#.....#.................#............
/// ..........#...#####...............#............
/// ..........#...#.#.#...............#............
/// ..........#.#########.............#............
/// ..........#.#.#.#.#.#.............#............
/// ....#######.#.#########...........#............
/// ....#.......#...#.#.#.#...........#............
/// #############...#####.#...........#####........
/// #...#.............#...#...............#........
/// #...#.^############...#...............#........
/// #...#.................#...............#........
/// #...#.................#######.....#########....
/// #...#.......................#.....#...#...#....
/// #####.......................#.....#...#...#....
/// ............................#.....#...#...#....
/// ............................#.....#####...#....
/// ............................#.............#....
/// ............................#.............#....
/// ............................#.............#....
/// ............................#...#####.....#....
/// ............................#...#...#.....#....
/// ............................#...#...#.....#....
/// ............................#...#...#.....#....
/// ............................#########.....#####
/// ................................#.............#
/// ................................#.............#
/// ................................#.............#
/// ..........................#######.............#
/// ..........................#...................#
/// ..........................#.......#############
/// ..........................#.......#............
/// ..........................#.......#............
/// ..........................#.......#............
/// ..........................#########............

const bool DEBUG = false;
const DELIM = ',';
const LF = 10;

class Scaffold {
  final program;
  late Position robotStartPosition;

  Scaffold(this.program);

  var robotSymbol = <String, Direction>{
    '<': Direction.left,
    '>': Direction.right,
    'V': Direction.down,
    '^': Direction.up
  };

  Position nextTurn(scaffold, Position pos) {
    var turn = Direction.values
        .where((d) =>
            scaffold.containsKey(pos.xy! + adjacentVector[d]) &&
            d != oppositeDirection(pos.dir!))
        .toList();
    return Position(pos.xy, turn.isEmpty ? null : turn.first);
  }

  Position nextMove(Map scaffold, Position pos) {
    var next = pos.xy! + adjacentVector[pos.dir];
    return Position(scaffold.containsKey(next) ? next : null, pos.dir);
  }

  String turnCode(Position pos1, Position pos2) =>
      (rightTurns[pos1.dir] == pos2.dir ? 'R' : 'L');

  //Construct path to visit each point, eg L,12,R,4,R,8,....
  //The method is to set the direction then continue in that direction
  //until we can't. Then find next turning and repeat movement.
  List findPath() {
    var scaffold = traverse();
    var pos = robotStartPosition;
    var result = [];
    var steps = 0;

    while (pos.hasDirection) {
      var next = nextMove(scaffold, pos);
      if (next.hasLocation) {
        steps++;
      } else {
        next = nextTurn(scaffold, pos);
        if (steps > 0) result.add(steps);
        if (next.hasDirection) result.add(turnCode(pos, next));
        steps = 0;
      }
      pos = next;
    }

    return result;
  }

  String asciiCodeToText(List<int> output) =>
      output.isNotEmpty ? String.fromCharCode(output.first) : '';

  int collectDust() {
    var compressedPath = Compressor(findPath());
    if (!compressedPath.run()) throw 'Could not compress path';

    print('main: ' + compressedPath.mainRoutine);
    print('A: ' + compressedPath.functionA);
    print('B: ' + compressedPath.functionB);
    print('C: ' + compressedPath.functionC);

    var continuousVideoFeed = 'n';

    var inputCommands = [
      ...compressedPath.mainRoutine.codeUnits,
      LF,
      ...compressedPath.functionA.codeUnits,
      LF,
      ...compressedPath.functionB.codeUnits,
      LF,
      ...compressedPath.functionC.codeUnits,
      LF,
      continuousVideoFeed.codeUnits.first,
      LF
    ];

    program[0] = 2;
    var robot = Computer(program, () => inputCommands.removeAt(0));
    var response = '';
    var result = 0;
    var output;

    while (!robot.halted) {
      robot.run([], true);
      output = robot.output(true);
      if (output.isNotEmpty) {
        if (output.first == LF) {
          print(response);
          response = '';
        } else {
          response += asciiCodeToText(output);
        }
        //The last output is the dust collected.
        result = output.first;
      }
    }
    return result;
  }

  Map<Point, int> traverse() {
    var robot = Computer(program);
    // ignore: unused_local_variable
    var view = '';
    var x = 0, y = 0;
    var scaffold = <Point, int>{};
    while (!robot.halted) {
      robot.run([], true);
      var output = robot.output(true);
      if (output.isNotEmpty) {
        var char = asciiCodeToText(output);
        view += char;

        if (robotSymbol.keys.contains(char)) {
          robotStartPosition = Position(Point(x, y), robotSymbol[char]);
        }

        if (output.first == LF) {
          x = 0;
          y++;
        } else if (char == '#') {
          scaffold[Point(x++, y)] = output.first;
        } else {
          x++;
        }
      }
    }
    //Uncomment to print scaffold
    // print(view);
    return scaffold;
  }

  int calibrateCameras() {
    return calcAlignmentParameters(traverse());
  }

  bool isIntersection(Map scaffold, Point p) => Direction.values
      .every((d) => scaffold.containsKey(p + adjacentVector[d]));

  int calcAlignmentParameters(Map scaffold) => scaffold.keys
      .fold(0, (acc, p) => acc + (isIntersection(scaffold, p) ? p.x * p.y : 0) as int);
}

class Compressor {
  //Max length of movement function (A, B, C)
  static const int MAX_FN_CHARS = 20;

  final inputString;
  Compressor(this.inputString);

  late final String mainRoutine;
  late final String functionA;
  late final String functionB;
  late final String functionC;

  //Whilst trying to compress, if we're left with just commas, the string
  //has been fully compressed.
  final _regex = RegExp(r'^' + DELIM + r'*$');

  bool _isCompressed(s) => _regex.hasMatch(s);

  void saveResults(String a, String b, String c) {
    functionA = a.trimChar(DELIM);
    functionB = b.trimChar(DELIM);
    functionC = c.trimChar(DELIM);

    mainRoutine = inputString
        .join(DELIM)
        .replaceAll(functionA, 'A')
        .replaceAll(functionB, 'B')
        .replaceAll(functionC, 'C');
  }

  //Crude brute force method of finding functions A, B and C.
  //We're done when all that's left is a number of commas ie every
  //repeating group has been removed from the original path.
  bool run() {
    var originalInput = inputString.join(DELIM) + DELIM;

    for (var iA in range(3, MAX_FN_CHARS + 1)) {
      var funcA = originalInput.substring(0, iA);
      var pathB = originalInput.replaceAll(funcA, '');
      for (var iB in range(3, MAX_FN_CHARS + 1)) {
        var funcB = pathB.substring(0, iB);
        var pathC = pathB.replaceAll(funcB, '');
        for (var iC in range(3, MAX_FN_CHARS + 1)) {
          var funcC = pathC.substring(0, iC);
          var pathFinal = pathC.replaceAll(funcC, '');
          if (_isCompressed(pathFinal)) {
            saveResults(funcA, funcB, funcC);
            return true;
          }
        }
      }
    }

    return false;
  }
}

Object part1(String header, List input) {
  printHeader(header);
  return Scaffold(input).calibrateCameras();
}

Object part2(String header, List input) {
  printHeader(header);
  return Scaffold(input).collectDust();
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day17.txt', DELIM);

  printAndAssert(part1('17 part 1', mainInput), 2788);

  // Path:
  // R, 12, L, 8, L, 4, L, 4, L, 8, R, 6, L, 6, R, 12, L, 8, L, 4, L, 4, L, 8,
  // R, 6, L, 6, L, 8, L, 4, R, 12, L, 6, L, 4, R, 12, L, 8, L, 4, L, 4, L, 8,
  // L, 4, R, 12, L, 6, L, 4, R, 12, L, 8, L, 4, L, 4, L, 8, L, 4, R, 12, L,
  // 6, L, 4, L, 8, R, 6, L, 6]

  // main = A,B,A,B,C,A,C,A,C,B
  // A= R,12,L,8,L,4,L,4
  // B= L,8,R,6,L,6
  // C= L,8,L,4,R,12,L,6,L,4
  printAndAssert(part2('17 part 2', mainInput), 761085);
}
