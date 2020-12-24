import 'dart:collection';

import './utils.dart';

const bool DEBUG = false;

class CupEntry<T> extends LinkedListEntry<CupEntry> {
  T value;
  CupEntry(this.value);

  @override
  String toString() => '$value';
}

class Cups {
  final List<int> input;
  final int picksPerMove;
  int maxCupValue;
  int minCupValue;
  CupEntry currentCup;

  LinkedList<CupEntry> cups = LinkedList();
  Map<int, CupEntry> cupIndex = {};

  Cups(this.input, this.picksPerMove) {
    minCupValue = input.min;
    maxCupValue = input.max;

    cups.addAll(input.map((e) {
      var cup = CupEntry(e);
      cupIndex[e] = cup;
      return cup;
    }));
    currentCup = cups.first;
  }

  List<CupEntry> pickup() {
    var pickedCups = <CupEntry>[];
    var next = currentCup;
    for (var i = 0; i < picksPerMove; i++) {
      next = nextCup(next);
      pickedCups.add(next);
    }
    return pickedCups;
  }

  //anticlockwise
  CupEntry previousCup(CupEntry start) {
    return start.previous ?? cups.last;
  }

  //clockwise
  CupEntry nextCup(CupEntry start) {
    return start.next ?? cups.first;
  }

  bool isPicked(cup, pickedList) {
    return pickedList.map((e) => e.value == cup).any((v) => v == true);
  }

  CupEntry selectDestinationCup(List<CupEntry> pickedList) {
    var destCupValue =
        currentCup.value != minCupValue ? currentCup.value - 1 : maxCupValue;
    while (isPicked(destCupValue, pickedList)) {
      destCupValue--;
      if (destCupValue < minCupValue) destCupValue = maxCupValue;
    }
    return cupIndex[destCupValue];
  }

  void placeCup(CupEntry destCup, List<CupEntry> pickedCups) {
    var start = destCup;
    for (var cup in pickedCups) {
      cup.unlink();
      start.insertAfter(cup);
      start = cup;
    }
  }

  void newCurrentCup() {
    currentCup = nextCup(currentCup);
  }

  void play(int moves) {
    var pickedCups;
    var destCup;

    void printStateOfPlay() {
      print('Destination: $destCup');
      print('Picked: $pickedCups');
      print(toString());
    }

    if (DEBUG) printStateOfPlay();

    for (var i = 0; i < moves; i++) {
      if (DEBUG) print('Move ${i + 1} ---------------------------------');
      if (DEBUG && i % 1000 == 0) print('Index: $i');
      pickedCups = pickup();
      destCup = selectDestinationCup(pickedCups);
      placeCup(destCup, pickedCups);
      newCurrentCup();
      if (DEBUG) printStateOfPlay();
    }
  }

  String playResult1() {
    var result = '';
    var next = cupIndex[1];
    while (result.length < input.length - 1) {
      next = nextCup(next);
      result += '${next.value}';
    }

    return result;
  }

  @override
  String toString() {
    return '$currentCup: $cups';
  }

  int playResult2() {
    var first = nextCup(cupIndex[1]);
    var second = nextCup(first);
    // print('first: $first, second: $second');
    return first.value * second.value;
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
  //Answer: 934001 x 159792 = 149245887792
  runPart2('23 test part 2', '389125467', 10000000);

  //Answer: 27865934
  runPart1('23 part 1', '872495136', 100);
  //Answer: 170836011000
  runPart2('23 part 2', '872495136', 10000000);
}
