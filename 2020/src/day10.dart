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
class Node {
  final int adapter;
  final List<int> nextNodes;
  bool wasVisited = false;
  int pathCount = 0;

  Node(this.adapter, this.nextNodes);

  //count = how many node paths there are from this node to the end
  void visited(count) {
    wasVisited = true;
    pathCount = count;
  }

  @override
  String toString() {
    return '$adapter: $nextNodes (visited: $visited, path: $pathCount)\n';
  }
}

class Graph {
  Map<int, Node> graph;
  Node root;

  Graph(List<int> input) {
    graph = buildGraph(input);
    root = graph[0];
  }

  //For any entry, it can "connect" up to MAX_DIFF ahead
  //eg 23 can connect to 24,25 and 26 and the map entry would be
  //tree[23]=[24,25,26]
  Map<int, Node> buildGraph(input) {
    var tree = <int, Node>{};
    for (var i = 0; i < input.length; i++) {
      var nextNodes = <int>[];
      var lookahead =
          ((i + MAX_DIFF) < input.length ? i + MAX_DIFF : input.length - 1);
      for (var k = i + 1; k <= lookahead; k++) {
        if (input[k] - input[i] <= MAX_DIFF) {
          nextNodes.add(input[k]);
        }
      }
      tree[input[i]] = Node(input[i], nextNodes);
    }
    return tree;
  }

  // returns the number of paths from node to the end of the tree
  int pathsFromNode(Node node) {
    if (node.nextNodes.isEmpty) return 1; //end reached: complete path found

    return node.nextNodes.fold(0, (acc, adapter) {
      var subNode = graph[adapter];
      if (!subNode.wasVisited) {
        subNode.visited(pathsFromNode(subNode));
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
  print(tree.pathsFromNode(tree.root));
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
