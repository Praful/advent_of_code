import './utils.dart';
import 'day04.dart';

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
    int value(name) => int.parse(match.namedGroup(name));
    _property[match.namedGroup('name')] = [
      [value('range1Min'), value('range1Max')],
      [value('range2Min'), value('range2Max')]
    ];
  }

  void parseInput() {
    var section = Section.property;
    for (var l in input) {
      var line = l.trim();
      if (line.isEmpty) continue;
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

  bool _isInRange(int v, int min, int max) => v.isBetweenI(min, max);

  bool _isInEitherRange(n, MapEntry kv) =>
      (_isInRange(n, kv.value[0][0], kv.value[0][1])) ||
      (_isInRange(n, kv.value[1][0], kv.value[1][1]));

  bool _isValueValid(int n) {
    for (var e in _property.entries) {
      if (_isInEitherRange(n, e)) return true;
    }
    return false;
  }

  int ticketScanningErrorRate() {
    return _nearByTickets
        .expand((i) => i)
        .toList()
        .fold(0, (acc, v) => acc + (!_isValueValid(v) ? v : 0));
  }

  bool _isTicketValid(List t) {
    return t.map((v) => _isValueValid(v)).every((r) => r);
  }

  List _validTickets() =>
      _nearByTickets.where((t) => _isTicketValid(t)).toList();

  //Return the labels for which value n is in range.
  Set _findValidLabels(int n) {
    var result = <String>{};

    _property.entries.forEach((e) {
      if (_isInEitherRange(n, e)) result.add(e.key);
    });
    return result;
  }

  //Work out the labels for each field in the tickets.
  List determineFieldLabels() {
    var result = [];
    var validTickets = List.from(_validTickets());
    for (var col = 0; col < validTickets[0].length; col++) {
      var columnLabelName = _property.keys.toSet();
      for (var row = 0; row < validTickets.length; row++) {
        columnLabelName = columnLabelName
            .intersection(_findValidLabels(validTickets[row][col]));
      }
      result.add(columnLabelName);
    }

    return _removeRepeatedLabels(result);
  }

  //at this stage fieldsNames will not be narrowed down to one name eg
  //an entry could be the set {a, b, c}. However, if another entry is {a}
  //then we can eliminate a from {a,b,c}. We repeatedly do this until
  //each set in labelNames consists of a single element.
  List _removeRepeatedLabels(List labelNames) {
    while (true) {
      var singleElementSets = labelNames.where((s) => s.length == 1);
      if (singleElementSets.length == labelNames.length) break;
      var multipleElementSets = labelNames.where((s) => s.length > 1);
      singleElementSets.forEach((singles) => multipleElementSets
          .forEach((multiples) => multiples.remove(singles.first)));
    }
    return labelNames;
  }

  int departureMultiplied(List fieldLabels) => fieldLabels.asMap().entries.fold(
      1,
      (result, e) =>
          result *
          (e.value.first.startsWith('departure') ? _yourTicket[e.key] : 1));

//   int departureMultiplied2(List fieldLabels) {
//     var result = 1;
//     for (var i = 0; i < fieldLabels.length; i++) {
//       if (fieldLabels[i].first.startsWith('departure')) {
//         print('${fieldLabels[i].first}: ${_yourTicket[i]}');
//         result *= _yourTicket[i];
//       }
//     }
//     return result;
//   }
}

void runPart1(String name, List input) {
  printHeader(name);
  var flightInfo = FlightInfo(input);
  print(flightInfo.ticketScanningErrorRate());
  // print(flightInfo.validTickets());
}

void runPart2(String name, List input) {
  printHeader(name);
  var flightInfo = FlightInfo(input);
  var fieldLabels = flightInfo.determineFieldLabels();
  print(flightInfo.departureMultiplied(fieldLabels));
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day16-test.txt');
  TEST_INPUT2 = fileAsString('../data/day16b-test.txt');
  MAIN_INPUT = fileAsString('../data/day16.txt');

  //Answer: 71
  runPart1('16 test part 1', TEST_INPUT);
  //Answer:
  runPart2('16 test part 2', TEST_INPUT2);

  //Answer: 24980
  runPart1('16 part 1', MAIN_INPUT);

  // departure time: 97
  // departure station: 163
  // departure date: 101
  // departure platform: 73
  // departure location: 53
  // departure track: 131
  //Answer: 809376774329
  runPart2('16 part 2', MAIN_INPUT);
}
