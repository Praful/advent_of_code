import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

class Vector {
  int x;
  int y;
  Vector(this.x, this.y);

  Vector rotate(side, angle) {
    //For vector (x,y) a 90 clockwise (=R turn) => (y, -x)
    //For vector (x,y) a 90 anti-clockwise (=L turn) => (-y, x)
    //So we turn once, twice or three times depending on angle (90,180, 270).
    var x2 = x, y2 = y, tmp;
    for (var numTurns = 0; numTurns < (angle ~/ 90); numTurns++) {
      if (side == 'R') {
        tmp = x2;
        x2 = y2;
        y2 = -tmp;
      } else if (side == 'L') {
        tmp = x2;
        x2 = -y2;
        y2 = tmp;
      } else {
        throw 'Turn must be L (anti-clockwise) or R (clockwise)';
      }
    }

    return Vector(x2, y2);
  }

  Vector operator +(Vector v) => Vector(x + v.x, y + v.y);
}

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

  //x = latitude, y = longitude
  Vector coord = Vector(0, 0);
  Compass facing;

  Position(this.facing);

  @override
  String toString() =>
      'Facing: $facing, latitude: $coord.x, longitude: $coord.y';

  void moveByCompassPoint(Compass direction, int amount) {
    switch (direction) {
      case Compass.north:
        coord.y += amount;
        break;
      case Compass.east:
        coord.x += amount;
        break;
      case Compass.south:
        coord.y -= amount;
        break;
      case Compass.west:
        coord.x -= amount;
        break;
      default:
    }
  }

  void moveByLatitudeLongitude(Vector v) {
    coord = coord + v;
  }

  void turnLatitudeLongitude(String side, int angle) {
    coord = coord.rotate(side, angle);
  }

  void turnCompassPoint(String side, int angle) {
    var newIndex = facing.index + ((angle ~/ 90) * (side == 'L' ? -1 : 1));
    if (newIndex < 0) newIndex += Compass.values.length;
    if (newIndex > Compass.values.length - 1) newIndex -= Compass.values.length;
    facing = Compass.values[newIndex];
  }
}

int navigate1(List<String> input) {
  var position = Position(Compass.east);
  input.forEach((instruction) {
    var action = instruction[0];
    var value = int.parse(instruction.substring(1));

    if (Position.compassPoints.contains(action)) {
      position.moveByCompassPoint(Position.stringToCompass[action], value);
    } else if (Position.turns.contains(action)) {
      position.turnCompassPoint(action, value);
    } else if (action == 'F') {
      position.moveByCompassPoint(position.facing, value);
    } else {
      throw 'Instruction is invalid: $instruction';
    }
    // print('$instruction: $position');
  });
  return position.coord.x.abs() + position.coord.y.abs();
}

int navigate2(List<String> input) {
  var ship = Position(null);
  var waypoint = Position(null);

  waypoint.moveByCompassPoint(Compass.east, 10);
  waypoint.moveByCompassPoint(Compass.north, 1);

  input.forEach((instruction) {
    var action = instruction[0];
    var value = int.parse(instruction.substring(1));

    if (Position.compassPoints.contains(action)) {
      waypoint.moveByCompassPoint(Position.stringToCompass[action], value);
    } else if (Position.turns.contains(action)) {
      waypoint.turnLatitudeLongitude(action, value);
    } else if (action == 'F') {
      ship.moveByLatitudeLongitude(
          Vector(waypoint.coord.x * value, waypoint.coord.y * value));
    } else {
      throw 'Instruction is invalid: $instruction';
    }
    // print('$instruction\nwp  : $waypoint\nship: $ship');
  });
  return ship.coord.x.abs() + ship.coord.y.abs();
}

void test() {
  var pos = Position(Compass.east);
  void turn(action, value) {
    pos.turnCompassPoint(action, value);
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
  print(navigate1(input));
}

void runPart2(String name, List input) {
  printHeader(name);
  print(navigate2(input));
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day12-test.txt');
  MAIN_INPUT = fileAsString('../data/day12.txt');

  // test();

  //Answer: 25
  runPart1('12 test part 1', TEST_INPUT);
  //Answer: 286
  runPart2('12 test part 2', TEST_INPUT);

  //Answer: 1221
  runPart1('12 part 1', MAIN_INPUT);
  //Answer: 59435
  runPart2('12 part 2', MAIN_INPUT);
}
