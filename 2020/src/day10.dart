import 'dart:io';
import './utils.dart';

const bool DEBUG = false;
const int MAX_DIFF = 3;

final List<int> TEST_INPUT = File('../data/day10-test.txt')
    .readAsLinesSync()
    .map((l) => int.parse(l))
    .toList();

final List<int> TEST_INPUT2 = File('../data/day10b-test.txt')
    .readAsLinesSync()
    .map((l) => int.parse(l))
    .toList();

final List<int> MAIN_INPUT = File('../data/day10.txt')
    .readAsLinesSync()
    .map((l) => int.parse(l))
    .toList();

//Part 1 = quick and dirty
int findJoltsPart1(List<int> input) {
  var sumOfOnes = 0;
  var sumOfThrees = 1;
  if (input[0] == 1) sumOfOnes++;
  if (input[0] == 3) sumOfThrees++;
  for (var i = 0; i < input.length - 1; i++) {
    var diff = input[i + 1] - input[i];
    if (diff == 1) sumOfOnes++;
    if (diff == 3) sumOfThrees++;
  }

  return sumOfOnes * sumOfThrees;
}

//part 2
class Adapter {
  final List<int> nextAdapters;
  bool wasCalculated = false;
  int _pathCount = 0;

  Adapter(this.nextAdapters);

  //v = how many adapter paths there are from this one to the end
  set pathCount(v) {
    _pathCount = v;
    wasCalculated = true;
  }

  int get pathCount => _pathCount;

  @override
  String toString() {
    return '$nextAdapters (visited: $wasCalculated, path: $_pathCount)\n';
  }
}

class Graph {
  Map<int, Adapter> _graph;
  Adapter root;

  Graph(List<int> input) {
    _graph = buildGraph(input);
    root = _graph[0];
  }

  Map<int, Adapter> buildGraph(List<int> input) {
    var graph = <int, Adapter>{};
    input.forEach((adapter) {
      graph[adapter] = Adapter(
          input.where((e) => e > adapter && e <= adapter + MAX_DIFF).toList());
    });

    return graph;
  }

  // returns the number of paths from adapter to the end of the graph
  int pathsFromAdapter(Adapter node) {
    if (node.nextAdapters.isEmpty) return 1; //end reached: complete path found

    return node.nextAdapters.fold(0, (acc, adapter) {
      var subNode = _graph[adapter];
      if (!subNode.wasCalculated) {
        subNode.pathCount = pathsFromAdapter(subNode);
      }
      acc += subNode.pathCount;
      return acc;
    });
  }
}

void runPart1(String name, List<int> input) {
  printHeader(name);
  print(findJoltsPart1(input));
}

void runPart2(String name, List<int> input) {
  printHeader(name);
  var tree = Graph(input);
  // print(tree);
  print(tree.pathsFromAdapter(tree.root));
}

void main(List<String> arguments) {
  TEST_INPUT.sort();
  TEST_INPUT2.sort();
  MAIN_INPUT.sort();

  //Answer: 35
  runPart1('10 test 1a', TEST_INPUT);
  //Answer: 220
  runPart1('10 test 1b', TEST_INPUT2);

  // Answer: 1980
  runPart1('10 part 1', MAIN_INPUT);

  //Answer: 8
  runPart2('10 test 2a', [0, ...TEST_INPUT, TEST_INPUT.max + 3]);
  //Answer:19208
  runPart2('10 test 2b', [0, ...TEST_INPUT2, TEST_INPUT2.max + 3]);

  //Answer: 4628074479616
  runPart2('10 part 2', [0, ...MAIN_INPUT, MAIN_INPUT.max + 3]);
}
