import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

enum RuleType { nonterminal, terminal }

class Rule {
  RuleType type;
  String value;
  List mappings = [];

  Rule(String input) {
    if (input.contains('"')) {
      type = RuleType.terminal;
      value = input.replaceAll('"', '').trim();
    } else {
      type = RuleType.nonterminal;
      var options = input.split('|');
      options.forEach((r) => mappings.add(r.trim().split(' ').map(int.parse)));
    }
  }
  @override
  String toString() {
    return (type == RuleType.nonterminal ? mappings.toString() : value);
  }
}

class Rules {
  final List<String> input;
  Map rules = {};
  Set messages = {};

  Rules(this.input) {
    parseInput();
  }
  void parseInput() {
    var isRule = true;
    input.forEach((line) {
      var s = line.trim();
      if (s.isEmpty) {
        isRule = false;
      }
      if (isRule) {
        var parts = s.split(':');
        var id = int.parse(parts[0]);
        rules[id] = Rule(parts[1]);
      } else {
        if (s.isNotEmpty) messages.add(s);
      }
    });
  }

  Object rule8() => '(${createRegex(42, true)})+';
  Object rule11() {
    var r42 = '(${createRegex(42, true)})';
    var r31 = '(${createRegex(31, true)})';

    //HACK! to create repeating groups since Dart doesn't seem
    //to support. The 10 is chose based on part 2 rules. Other
    //rules/data may not work.
    var r8 = range(1, 10).map((i) => '$r42{$i}$r31{$i}').toList();

    return '(?:${r8.join('|')})';
  }

  Object createRegex([start = 0, part2 = false]) {
    if (part2) {
      if (start == 8) return rule8();
      if (start == 11) return rule11();
    }

    var rule = rules[start];

    if (rule.type == RuleType.terminal) return rule.value;

    var regex = rule.mappings.map((alternatives) =>
        alternatives.map((id) => createRegex(id, part2)).join());

    //Use non-capturing groups (?:) otherwise it's slow.
    return '(?:${regex.join('|')})';
  }

  @override
  String toString() {
    return 'Rules:\n${rules.toString()}\nMessages:\n$messages';
  }
}

void runPart(String name, List input, [isPart2 = false]) {
  printHeader(name);

  var rules = Rules(input);
  var rulesRegexStr = '^${rules.createRegex(0, isPart2)}\$';
  var regexRule0 = RegExp(rulesRegexStr);
  var result = rules.messages
      .fold(0, (acc, m) => acc + (regexRule0.hasMatch(m) ? 1 : 0));
  print(result);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day19-test.txt');
  TEST_INPUT2 = fileAsString('../data/day19b-test.txt');
  MAIN_INPUT = fileAsString('../data/day19.txt');

  //Answer: 2
  runPart('19 test part 1', TEST_INPUT);
  //Answer:
  runPart('19 test part 2', TEST_INPUT2, true);

  //Answer: 165
  runPart('19 part 1', MAIN_INPUT);
  //Answer: 274
  runPart('19 part 2', MAIN_INPUT, true);
}
