import './utils.dart';
import 'dart:collection';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

List parseInput(input) {
  void addCard(player, card) => player.addBottom(int.parse(card));

  var player1 = Player();
  var player2 = Player();
  var player = 0;

  for (var line in input) {
    var card = line.trim();
    if (card == '') continue;
    if (line.startsWith('Player')) {
      player++;
    } else {
      switch (player) {
        case 1:
          addCard(player1, line);
          break;
        case 2:
          addCard(player2, line);
          break;
        default:
      }
    }
  }
  return [player1, player2];
}

class Game {
  final Player player1;
  final Player player2;
  var winningPlayer;
  Game(this.player1, this.player2);

  int play() {
    void win(player, winningCard, losingCard) {
      player.addBottom(winningCard);
      player.addBottom(losingCard);
    }

    while (player1.hasMoreCards && player2.hasMoreCards) {
      var p1Card = player1.play();
      var p2Card = player2.play();
      if (p1Card > p2Card) {
        win(player1, p1Card, p2Card);
      } else {
        win(player2, p2Card, p1Card);
      }
    }
    winningPlayer = player1.hasMoreCards ? player1 : player2;
    return winningScore();
  }

  int winningScore() {
    var cards = winningPlayer.cards.toList();
    var score = 0;
    for (var i = 0; i < cards.length; i++) {
      score += cards[i] * (cards.length - i);
    }
    return score;
  }

  @override
  String toString() {
    return 'Player 1: \n$player1\nPlayer2:\n$player2';
  }
}

class Player {
  var cards = Queue();

  void addTop(card) => cards.addFirst(card);
  void addBottom(card) => cards.addLast(card);

  bool get hasMoreCards => cards.isNotEmpty;

  int play() => cards.removeFirst();

  @override
  String toString() => cards.toString();
}

void runPart1(String name, List<String> input) {
  printHeader(name);
  var players = parseInput(input);
  // print(players);
  var game = Game(players[0], players[1]);
  print(game.play());
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day22-test.txt');
  MAIN_INPUT = fileAsString('../data/day22.txt');

  //Answer:
  runPart1('22 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('22 test part 2', TEST_INPUT);

  //Answer:
  runPart1('22 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('22 part 2', MAIN_INPUT);
}
