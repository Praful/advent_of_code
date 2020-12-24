import './utils.dart';

const bool DEBUG = false;

class Cups {
  final List<int> input;
  final int picksPerMove;
  int maxCupValue;
  int minCupValue;
  int currentCup;
  List<int> cups;

  Cups(this.input, this.picksPerMove) {
    currentCup = input[0];
    cups = input;
    minCupValue = cups.min;
    maxCupValue = cups.max;
  }

  List<int> strToList(String s) => s.split('').map(int.parse).toList();

  List<int> pickup() {
    var pickedCups = <int>[];
    var removedIndices = [];
    var pickupIndex = cups.indexOf(currentCup) + 1;
    while (pickedCups.length < picksPerMove) {
      if (pickupIndex >= cups.length) pickupIndex = 0;
      pickedCups.add(cups[pickupIndex]);
      removedIndices.add(pickupIndex);
      pickupIndex++;
    }
    removedIndices.sort();
    for (var i = removedIndices.length - 1; i >= 0; i--) {
      cups.removeAt(removedIndices[i]);
    }

    return pickedCups;
  }

  int nextCupClockwise(int start) {
    var nextIndex = cups.indexOf(start) + 1;
    if (nextIndex >= cups.length) nextIndex = 0;
    return cups[nextIndex];
  }

  int selectDestinationCup() {
    var destCup = currentCup - 1;
    while (!cups.contains(destCup)) {
      destCup--;
      if (destCup < minCupValue) destCup = maxCupValue;
    }
    return destCup;
  }

  void placeCup(int destCup, List<int> pickedCups) {
    cups.insertAll(cups.indexOf(destCup) + 1, pickedCups);
  }

  void newCurrentCup() {
    currentCup = nextCupClockwise(currentCup);
  }

  void play(int moves) {
    var pickedCups;
    var destCup;

    void printStateOfPlay() {
      // print('Destination: $destCup');
      // print('Picked: $pickedCups');
      // print(toString());
    }

    printStateOfPlay();

    for (var i = 0; i < moves; i++) {
      // print('Move ${i + 1} -------------------------------------------');
      if (i % 1000 == 0) print('Index: $i');
      pickedCups = pickup();
      // print(cups);
      destCup = selectDestinationCup();
      placeCup(destCup, pickedCups);
      newCurrentCup();
      printStateOfPlay();
    }
  }

  String playResult1() {
    //todo
    var result = '';
    var nextCup = 1;
    while (result.length < input.length - 1) {
      nextCup = nextCupClockwise(nextCup);
      result += nextCup.toString();
    }

    return result;
  }

  @override
  String toString() {
    return '$currentCup: $cups';
  }

  int playResult2() {
    var first = nextCupClockwise(1);
    var second = nextCupClockwise(first);
    return first * second;
  }
}

void runPart1(String name, String input, int moves) {
  printHeader(name);
  var cupGame = Cups(input.split('').map(int.parse).toList(), 3);
  cupGame.play(moves);
  print(cupGame.playResult1());
}

void runPart2(String name, String input, int moves) {
  printHeader(name);
  var newInput = input.split('').map(int.parse).toList();
  var max = newInput.max;
  for (var i = max + 1; i <= 1000000; i++) {
    newInput.add(i);
  }
  var cupGame = Cups(newInput, 3);
  cupGame.play(moves);
  print(cupGame.playResult2());
}

void main(List<String> arguments) {
  //Answer: 92658374
  runPart1('23 test part 1', '389125467', 10);
  //Answer:
  runPart2('23 test part 1', '389125467', 10000000);

  //Answer: 27865934
  runPart1('23 part 1', '872495136', 100);
  //Answer:
  // runPart2('23 part 2', MAIN_INPUT);
}
