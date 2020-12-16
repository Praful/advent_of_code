import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

enum Section { property, yourTicket, nearByTickets }

class FlightInfo {
  static RegExp propertyRegex = RegExp(
      r'^(?<name>^[\w\s]+):\s(?<range1Min>\d+)-(?<range1Max>\d+) or (?<range2Min>\d+)-(?<range2Max>\d+)$');

  final Map<String, List<List<int>>> _property = {};

  final List<int> _yourTicket = [];
  final List<List<int>> _nearByTickets = [];

  final List<String> input;

  FlightInfo(this.input) {
    parseInput();
  }
  @override
  String toString() => '$_yourTicket\n$_nearByTickets\n$_property';

  void _setProperty(match) {
    // minAppearances = int.parse(match.namedGroup('min'));
    var range1Min = int.parse(match.namedGroup('range1Min'));
    var range1Max = int.parse(match.namedGroup('range1Max'));
    var range2Min = int.parse(match.namedGroup('range2Min'));
    var range2Max = int.parse(match.namedGroup('range2Max'));
    _property[match.namedGroup('name')] = [
      [range1Min, range1Max],
      [range2Min, range2Max]
    ];
  }

  void parseInput() {
    var section = Section.property;
    for (var i = 0; i < input.length; i++) {
      var line = input[i].trim();
      if (line.trim().isEmpty) continue;
      if (line.startsWith('your ticket:')) {
        section = Section.yourTicket;
        continue;
      }
      if (line.startsWith('nearby tickets:')) {
        section = Section.nearByTickets;
        continue;
      }

      switch (section) {
        case Section.property:
          _setProperty(propertyRegex.firstMatch(line));
          break;
        case Section.yourTicket:
          _yourTicket.addAll(line.split(',').map((n) => int.parse(n)).toList());
          break;
        case Section.nearByTickets:
          _nearByTickets.add(line.split(',').map((n) => int.parse(n)).toList());
          break;
        default:
      }
    }
  }

  bool inRange(int v, int min, int max) => v.isBetweenI(min, max);

  bool _validValue(int n) {
    for (var v in _property.values) {
      if (inRange(n, v[0][0], v[0][1])) return true;
      if (inRange(n, v[1][0], v[1][1])) return true;
    }
    return false;
  }

  int ticketScanningErrorRate() {
    return _nearByTickets
        .expand((i) => i)
        .toList()
        .fold(0, (acc, v) => acc + (!_validValue(v) ? v : 0));
  }

void runPart1(String name, List input) {
  printHeader(name);
  var flightInfo = FlightInfo(input);
  print(flightInfo.ticketScanningErrorRate());
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day16-test.txt');
  MAIN_INPUT = fileAsString('../data/day16.txt');

  //Answer: 71
  runPart1('16 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('16 test part 2', TEST_INPUT);

  //Answer:
  runPart1('16 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('16 part 2', MAIN_INPUT);
}
