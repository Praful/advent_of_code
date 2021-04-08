import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import 'dart:math';
import 'package:tuple/tuple.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

enum Action { deal, cut, increment }

class Command {
  final Action action;
  final int quantity;
  Command(this.action, this.quantity);

  @override
  String toString() => '$action, $quantity';
}

int quantity(String action, String s) =>
    action.substring(s.length).trim().toInt();

Command toCommand(String action) {
  if (action.startsWith('deal into new stack')) {
    return Command(Action.deal, 0);
  }

  if (action.startsWith('cut')) {
    return Command(Action.cut, quantity(action, 'cut '));
  }

  if (action.startsWith('deal with increment')) {
    return Command(Action.increment, quantity(action, 'deal with increment '));
  }
  throw 'Invalid action $action';
}

class Deck {
  List<int> deal(List<int> deck) => [...deck].reversed.toList();

  List<int> cut(List<int> deck, int amount) {
    late List first;
    late List second;
    if (amount > 0) {
      second = deck.sublist(0, amount);
      first = deck.sublist(amount);
    } else {
      first = deck.sublist(deck.length + amount);
      second = deck.sublist(0, deck.length - amount.abs());
    }
    return [...first, ...second];
  }

  List<int> dealWithIncrement(List<int> deck, int increment) {
    var result = List.filled(deck.length, 0);
    result[0] = deck[0];
    for (var i in range(0, deck.length)) {
      result[i * increment % deck.length] = deck[i];
    }

    // assert(result.toSet().length == deck.length);

    return result;
  }

  List<int> run(List<int> deck, Command command) {
    // print(command);
    switch (command.action) {
      case Action.deal:
        return deal(deck);
      case Action.cut:
        return cut(deck, command.quantity);
      case Action.increment:
        return dealWithIncrement(deck, command.quantity);
      default:
        throw 'Invalid command $command';
    }
  }

  List<int> shuffle(List<int> originalDeck, List<String> commands) {
    var deck = [...originalDeck];

    for (var action in commands) {
      deck = run(deck, toCommand(action));
    }

    return deck;
  }
}

List<int> part1(String header, List<String> commands, List<int> deck) {
  printHeader(header);

  return Deck().shuffle(deck, commands);
}

//My maths is too rusty to work this out. I've looked at various
//solutions and implemeneted in Dart. See thread:
//
//https://www.reddit.com/r/adventofcode/comments/khyjgv/2020_day_22_solutions/
//
//especially https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbwpk5k?utm_source=share&utm_medium=web2x&context=3

BigInt run2(
    List<String> commands, int deckSize, int position, int shuffleCount) {
  BigInt pow(int x, int exp, int mod) =>
      BigInt.from(x).modPow(BigInt.from(exp), BigInt.from(mod));

  // Fermat's little theorem
  BigInt inv(int a, int n) => pow(a, n - 2, n);

  var a = 1;
  var b = 0;

  for (var action in commands) {
    var la;
    var lb;
    var cmd = toCommand(action);
    switch (cmd.action) {
      case Action.deal:
        la = -1;
        lb = -1;
        break;
      case Action.increment:
        la = cmd.quantity;
        lb = 0;
        break;
      case Action.cut:
        la = 1;
        lb = -cmd.quantity;
        break;
      default:
    }

    a = (la * a) % deckSize;
    b = (la * b + lb) % deckSize;
  }

  var sca = pow(a, shuffleCount, deckSize);
  var scb = (BigInt.from(b) * (sca - BigInt.one) * inv(a - 1, deckSize)) %
      BigInt.from(deckSize);

  //This gives index value (which was asked for in part 1); here we want
  //what's at a particular position.
  //(sca * c + scb) % n

  return ((BigInt.from(position) - scb) * inv(sca.toInt(), deckSize)) %
      BigInt.from(deckSize);
}

BigInt part2(String header, List<String> input) {
  printHeader(header);

  var deckSize = 119315717514047;
  var shuffleCount = 101741582076661;
  var position = 2020;

  return run2(input, deckSize, position, shuffleCount);
}

void main(List<String> arguments) {
  var testInput = FileUtils.asLines('../data/day22-test.txt');
  var testInputb = FileUtils.asLines('../data/day22b-test.txt');
  var testInputc = FileUtils.asLines('../data/day22c-test.txt');
  var testInputd = FileUtils.asLines('../data/day22d-test.txt');

  var mainInput = FileUtils.asLines('../data/day22.txt');
  assertEqual(part1('22 test part 1', testInput, range(0, 10).toList()).join(),
      '0369258147');
  assertEqual(
      part1('22 test part 1b', testInputb, range(0, 10).toList()).join(),
      '3074185296');
  assertEqual(
      part1('22 test part 1c', testInputc, range(0, 10).toList()).join(),
      '6307418529');
  assertEqual(
      part1('22 test part 1d', testInputd, range(0, 10).toList()).join(),
      '9258147036');

  printAndAssert(
      part1('22 part 1', mainInput, range(0, 10007).toList()).indexOf(2019),
      7744);

  printAndAssert(part2('22 part 2', mainInput), BigInt.from(57817797345992));
}
