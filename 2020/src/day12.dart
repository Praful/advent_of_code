import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

enum Compass { north, east, south, west }

class Position {
  static const Set compassPoints = {'N', 'E', 'S', 'W'};
  static const Set turns = {'L', 'R'};

  static const Map stringToCompass = {
    'N': Compass.north,
    'E': Compass.east,
    'S': Compass.south,
    'W': Compass.west
  };

  int longitude = 0; //north/south
  int latitude = 0; //east/west
  Compass facing;

  Position(this.facing);

  @override
  String toString() =>
      'Facing: $facing, longitude: $longitude, latitude: $latitude';

  List move(Compass direction, int amount) {
    switch (direction) {
      case Compass.north:
        longitude += amount;
        break;
      case Compass.east:
        latitude += amount;
        break;
      case Compass.south:
        longitude -= amount;
        break;
      case Compass.west:
        latitude -= amount;
        break;
      default:
    }
    return [longitude, latitude];
  }

  Compass turn(String side, int angle) {
    var turns = (angle ~/ 90) * (side == 'L' ? -1 : 1);
    var newIndex = facing.index + turns;
    if (newIndex < 0) newIndex += Compass.values.length;
    if (newIndex > Compass.values.length - 1) newIndex -= Compass.values.length;
    facing = Compass.values[newIndex];
    return facing;
  }
}

int navigate(List<String> input) {
  var position = Position(Compass.east);
  input.forEach((instruction) {
    var action = instruction[0];
    var value = int.parse(instruction.substring(1));
    if (Position.compassPoints.contains(action)) {
      position.move(Position.stringToCompass[action], value);
    } else if (Position.turns.contains(action)) {
      position.turn(action, value);
    } else if (action == 'F') {
      position.move(position.facing, value);
    } else {
      throw 'Instruction is invalid: $instruction';
    }
    // print('$instruction: $position');
  });
  return position.latitude.abs() + position.longitude.abs();
}

void test() {
  var pos = Position(Compass.east);
  void turn(action, value) {
    pos.turn(action, value);
    print('$action$value: $pos');
  }

  turn('L', 90);
  turn('R', 270);
  turn('L', 270);
  turn('L', 90);
  turn('R', 180);
  turn('L', 180);
  turn('R', 90);
}

void runPart1(String name, List input) {
  printHeader(name);
  print(navigate(input));
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day12-test.txt');
  MAIN_INPUT = fileAsString('../data/day12.txt');

  // test();

  //Answer: 25
  runPart1('12 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('12 test part 2', TEST_INPUT);

  //Answer:
  runPart1('12 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('12 part 2', MAIN_INPUT);
}
