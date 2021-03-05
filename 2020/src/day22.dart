import 'dart:collection';
import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

List parseInput(input) {
  void addCard(player, card) => player.addBottom(int.parse(card));

  var player1 = Player(1);
  var player2 = Player(2);
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
  Game(this.player1, this.player2);

  void winRound(player, winningCard, losingCard) {
    player.addBottom(winningCard);
    player.addBottom(losingCard);
  }

  //return winning player
  Player playCombat() {
    while (player1.hasMoreCards && player2.hasMoreCards) {
      var p1Card = player1.playRound();
      var p2Card = player2.playRound();
      if (p1Card > p2Card) {
        winRound(player1, p1Card, p2Card);
      } else {
        winRound(player2, p2Card, p1Card);
      }
    }
    return (player1.hasMoreCards ? player1 : player2);
  }

  //return winning player
  Player playSubGame(cardCountPlayer1, cardCountPlayer2) {
    var player1Clone = Player.clone(player1, cardCountPlayer1);
    var player2Clone = Player.clone(player2, cardCountPlayer2);
    var subGame = Game(player1Clone, player2Clone);
    return subGame.playRecursiveCombat();
  }

  //return winning player
  Player playRecursiveCombat() {
    while (player1.hasMoreCards && player2.hasMoreCards) {
      if (player1.hasRepeatHand && player2.hasRepeatHand) return player1;
      var p1Card = player1.playRound();
      var p2Card = player2.playRound();
      if (player1.cardsInDeck >= p1Card && player2.cardsInDeck >= p2Card) {
        if (playSubGame(p1Card, p2Card).id == 1) {
          winRound(player1, p1Card, p2Card);
        } else {
          winRound(player2, p2Card, p1Card);
        }
      } else if (p1Card > p2Card) {
        winRound(player1, p1Card, p2Card);
      } else {
        winRound(player2, p2Card, p1Card);
      }
    }

    return (player1.hasMoreCards ? player1 : player2);
  }

  int score(player) {
    return player.cards
        .toList()
        .asMap()
        .entries
        .map((e) => (e.value * (player.cards.length - e.key)))
        .toList()
        .reduce((acc, v) => acc + v);
  }

  // int score2(player) {
  //   var cards = player.cards.toList();
  //   var score = 0;
  //   for (var i = 0; i < cards.length; i++) {
  //     score += cards[i] * (cards.length - i);
  //   }
  //   return score;
  // }

  @override
  String toString() {
    return 'Player 1: \n$player1\nPlayer2:\n$player2';
  }
}

class Player {
  var cards = Queue();
  var deckHistory = <String>{};
  var id;
  Player(this.id);

  void addTop(card) => cards.addFirst(card);
  void addBottom(card) => cards.addLast(card);
  bool get hasMoreCards => cards.isNotEmpty;
  bool get hasRepeatHand => deckHistory.contains(cards.join());
  int get cardsInDeck => cards.length;

  static Player clone(player, cardsToCopy) {
    var clone = Player(player.id);
    for (var i = 0; i < cardsToCopy; i++) {
      clone.addBottom(player.cards.elementAt(i));
    }
    return clone;
  }

  int playRound() {
    deckHistory.add(cards.join());
    return cards.removeFirst();
  }

  @override
  String toString() => cards.toString();
}

void runPart1(String name, List<String> input) {
  printHeader(name);
  var players = parseInput(input);
  var game = Game(players[0], players[1]);

  var winner = game.playCombat();
  print(game.score(winner));
}

void runPart2(String name, List input) {
  printHeader(name);
  var players = parseInput(input);
  var game = Game(players[0], players[1]);
  var winner = game.playRecursiveCombat();
  print(game.score(winner));
}

void main(List<String> arguments) {
  var TEST_INPUT = FileUtils.asLines('../data/day22-test.txt');
  var MAIN_INPUT = FileUtils.asLines('../data/day22.txt');

  //Answer: 306
  runPart1('22 test part 1', TEST_INPUT);
  //Answer: 291
  runPart2('22 test part 2', TEST_INPUT);

  //Answer: 31957
  runPart1('22 part 1', MAIN_INPUT);
  //Answer: 33212
  runPart2('22 part 2', MAIN_INPUT);
}
