import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

enum RuleType { nonterminal, terminal }

class Rule {
  RuleType type;
  String value;
  List ruleIds = [];

  Rule(String input) {
    if (input.contains('"')) {
      type = RuleType.terminal;
      value = input.replaceAll('"', '').trim();
    } else {
      type = RuleType.nonterminal;
      var options = input.split('|');
      options.forEach((r) => ruleIds.add(r.trim().split(' ')));
    }
  }
  @override
  String toString() {
    return (type == RuleType.nonterminal ? ruleIds.toString() : value);
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
        var id = parts[0];
        rules[id] = Rule(parts[1]);
      } else {
        if (s.isNotEmpty) messages.add(s);
      }
    });
  }

  Object createRegex([start = '0']) {
    var top = rules[start];
    if (top.type == RuleType.terminal) return top.value;
    return top.ruleIds.map((subrule) => subrule
        .map((subsubrule) => createRegex(subsubrule))
        .toList()
        .map((alts) => alts.length == 1
            ? alts
            : "(${alts.map((r) => r.join()).join('|')})"));
  }

  @override
  String toString() {
    return 'Rules:\n${rules.toString()}\nMessages:\n$messages';
  }
}

void runPart1(String name, List input) {
  printHeader(name);
  var rules = Rules(input);
  var rulesRegexStr =
      '^' + rules.createRegex().toString().replaceAll(', ', '') + '\$';
  var regex = RegExp(rulesRegexStr);
  var result =
      rules.messages.fold(0, (acc, m) => acc + (regex.hasMatch(m) ? 1 : 0));
  print(result);
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day19-test.txt');
  TEST_INPUT2 = fileAsString('../data/day19b-test.txt');
  MAIN_INPUT = fileAsString('../data/day19.txt');

  //Answer: 2
  runPart1('19 test part 1', TEST_INPUT);
  //Answer:
  runPart2('19 test part 2', TEST_INPUT2);

  //Answer: 165
  runPart1('19 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('19 part 2', MAIN_INPUT);
}
