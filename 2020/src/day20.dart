import './utils.dart';
import 'package:trotter/trotter.dart';

const bool DEBUG = false;

Image TEST_INPUT;
Image TEST_INPUT2;
Image MAIN_INPUT;

class Tile {
  final input;
  int id;
  List<String> tile;
  Set<String> possibleEdges;
  List<int> adjacentTiles = [];

  Tile(this.input) {
    parseInput();
  }

  void parseInput() {
    tile = input.split('\n');
    id = int.parse(tile[0].split(' ')[1].split(':')[0]);
    tile.removeAt(0); //remove id row
    possibleEdges = generatePossibleEdges();
  }

  Set<String> generatePossibleEdges() {
    var result = <String>{};

    void add(String s) {
      result.add(s);
      result.add(s.reversed());
    }

    add(tile[0]); //top
    add(tile.last); //bottom
    add(tile.map((line) => line[0]).join()); //left
    add(tile.map((line) => line[line.length - 1]).join()); //right

    return result;
  }

  @override
  String toString() => '$id:\n${tile.join('\n')}';
}

class Image {
  List<Tile> tiles;
  final String input;

  Image(this.input) {
    tiles = parseInput();
  }

  List<Tile> parseInput() => input
      .split('\n\n')
      .where((s) => s.trim().isNotEmpty)
      .map((t) => Tile(t.trim()))
      .toList();

  void findAdjacentTiles() {
    var combos = Combinations(2, tiles);
    for (final combo in combos()) {
      var tile1 = combo[0];
      var tile2 = combo[1];

      var adj = tile1.possibleEdges.intersection(tile2.possibleEdges);
      if (adj.isNotEmpty) {
        tile1.adjacentTiles.add(tile2.id);
        tile2.adjacentTiles.add(tile1.id);
      }
    }
    // printAdjacentTiles();
  }

  //part 1 solution
  int cornerIdMultiplier() => tiles
      .where((t1) => t1.adjacentTiles.length == 2)
      .map((t2) => t2.id)
      .multiply;

  void printAdjacentTiles() {
    tiles.forEach((t) {
      print('${t.id}: ${t.adjacentTiles.length}');
    });
  }
}

void runPart1(String name, Image image) {
  printHeader(name);
  image.findAdjacentTiles();
  print(image.cornerIdMultiplier());
}

void runPart2(String name, List input) {
  printHeader(name);
  //1. remove border (outer four tiles) of all tiles
  //2. merge tiles into one image
  //3. look for sea monsters, rotating and flipping until found
  //4. mark sea monsters with 0
  //5. return number of # that are not part of sea monster
}

void main(List<String> arguments) {
  TEST_INPUT = Image(readFile('../data/day20-test.txt'));
  MAIN_INPUT = Image(readFile('../data/day20.txt'));

  //Answer: 1951 * 3079 * 2971 * 1171 = 20899048083289
  runPart1('20 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('20 test part 2', TEST_INPUT);

  //Answer: 22878471088273
  runPart1('20 part 1', MAIN_INPUT);
  //Answer:
  // runPart2(20 part 2', MAIN_INPUT);
}
