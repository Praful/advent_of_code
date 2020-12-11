import 'dart:io';
import './utils.dart';

const bool DEBUG = false;
const int MAX_DIFF = 3;

List<int> TEST_INPUT;
List<int> TEST_INPUT2;
List<int> MAIN_INPUT;

List<int> file(input) {
  var result = File(input).readAsLinesSync().map((l) => int.parse(l)).toList();
  result.sort();
  return result;
}

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
class AdapterNode {
  final List<int> linkedAdapterJolts;
  bool wasCalculated = false;
  int _pathCount = 0;

  AdapterNode(this.linkedAdapterJolts);

  //v = how many adapter paths there are from this one to the end
  set pathCount(v) {
    _pathCount = v;
    wasCalculated = true;
  }

  int get pathCount => _pathCount;

  @override
  String toString() {
    return '$linkedAdapterJolts (visited: $wasCalculated, path: $_pathCount)\n';
  }
}

class Graph {
  Map<int, AdapterNode> _graph;
  AdapterNode root;

  Graph(List<int> input) {
    _graph = buildGraph(input);
    root = _graph[0];
  }

  Map<int, AdapterNode> buildGraph(List<int> input) {
    var graph = <int, AdapterNode>{};

    input.forEach((adapterJolt) {
      graph[adapterJolt] = AdapterNode(input
          .where((e) => e.isBetween(adapterJolt, adapterJolt + MAX_DIFF + 1))
          .toList());
    });
    // print(graph);
    return graph;
  }

  // returns the number of paths from adapter to the end of the graph
  int pathsFromAdapter(AdapterNode adapterNode) {
    if (adapterNode.linkedAdapterJolts.isEmpty) return 1; //end reached

    return adapterNode.linkedAdapterJolts.fold(0, (acc, adapterJolt) {
      var linkedAdapterNode = _graph[adapterJolt];
      if (!linkedAdapterNode.wasCalculated) {
        linkedAdapterNode.pathCount = pathsFromAdapter(linkedAdapterNode);
      }
      acc += linkedAdapterNode.pathCount;
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
  var graph = Graph(input);
  print(graph.pathsFromAdapter(graph.root));
  // print(graph._graph);
}

void main(List<String> arguments) {
  TEST_INPUT = file('../data/day10-test.txt');
  TEST_INPUT2 = file('../data/day10b-test.txt');
  MAIN_INPUT = file('../data/day10.txt');

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
