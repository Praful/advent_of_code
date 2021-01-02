import './utils.dart';
import 'package:trotter/trotter.dart';

const bool DEBUG = false;

Image TEST_INPUT;
Image TEST_INPUT2;
Image MAIN_INPUT;

class AdjacentTile {
  final int id;
  final String commonEdge;
  AdjacentTile(this.id, this.commonEdge);

  @override
  String toString() => '$id: $commonEdge';
}

enum Location { top, bottom, left, right, none }

class Edge {
  final Location location;
  final String value;
  Edge(this.location, this.value);

  @override
  String toString() => '$location, $value';
}

class Tile {
  final input;
  int id;
  List<String> tile;
  Map<String, Edge> possibleEdges;
  Map<int, AdjacentTile> adjacentTiles = {};
  bool aligned = false;
  Map<Location, int> edges = {};
  // Map<Side, Function> enumToMethod;

  //Align top with bottom, left with right, etc
  static Map<Location, Location> alignsWith = {}
    ..[Location.left] = Location.right
    ..[Location.right] = Location.left
    ..[Location.top] = Location.bottom
    ..[Location.bottom] = Location.top;

  Tile(this.input) {
    parseInput();
    // enumToMethod[Side.bottom] = bottom;
    // enumToMethod[Side.top] = top;
    // enumToMethod[Side.left] = left;
    // enumToMethod[Side.right] = right;
  }

  void parseInput() {
    tile = input.split('\n');
    id = int.parse(tile[0].split(' ')[1].split(':')[0]);
    tile.removeAt(0); //remove id row
    possibleEdges = generatePossibleEdges();
  }

  Map<String, Edge> generatePossibleEdges() {
    var result = <String, Edge>{};

    void add(String s, Location location) {
      result[s] = Edge(location, s);
      result[s.reversed] = Edge(location, s.reversed);
    }

    add(top, Location.top);
    add(bottom, Location.bottom);
    add(left, Location.left);
    add(right, Location.right);

    return result;
  }

  //Return true if we managed to align tile edge to the correct location
  bool alignEdges(Location location, String value) {
    print('aligning $location for $value');
    for (var n = 0; n < 4; n++) {
      var target;
      // if (s == enumToMethod[side]()) break;
      switch (location) {
        case Location.top:
          target = top;
          break;
        case Location.bottom:
          target = bottom;
          break;
        case Location.left:
          target = left;
          break;
        case Location.right:
          target = right;
          break;
        default:
          throw 'Invalid value for location $location';
      }
      if (target == value) return true;
      rotate90();
    }
    return false;
  }

  List<String> rotate90() {
    var result = <String>[];
    for (var i = 0; i < tile.length; i++) {
      result.add(tile.reversed.map((line) => line[i]).join());
    }
    tile = result;
    return tile;
  }

  List<String> flip() {
    print('Flipping ${toString()}');
    tile = tile.reversed.toList();
    print('Flipped to ${toString()}');
    return tile;
  }

  Edge edge(String value) {
    bool equals(String a, String b) => (a == b) || (a == b.reversed);

    if (equals(value, top)) return Edge(Location.top, top);
    if (equals(value, bottom)) return Edge(Location.bottom, bottom);
    if (equals(value, left)) return Edge(Location.left, left);
    if (equals(value, right)) return Edge(Location.right, right);
    throw '$value is not on any side of the tile';
  }

  String get top => tile[0];
  String get bottom => tile.last;
  String get left => tile.map((line) => line[0]).join();
  String get right => tile.map((line) => line[line.length - 1]).join();

  @override
  String toString() => '$id:${adjacentTiles.values}\n${tile.join('\n')}';
}

class Image {
  Map<int, Tile> tiles;
  final String input;

  Image(this.input) {
    tiles = {for (var e in parseInput()) e.id: e};
  }

  List<Tile> parseInput() => input
      .split('\n\n')
      .where((s) => s.trim().isNotEmpty)
      .map((t) => Tile(t.trim()))
      .toList();

  void findAdjacentTiles() {
    var combos = Combinations(2, tiles.values.toList());
    for (final combo in combos()) {
      var tile1 = combo[0];
      var tile2 = combo[1];

      var adj = tile1.possibleEdges.keys
          .toSet()
          .intersection(tile2.possibleEdges.keys.toSet());

      if (adj.isNotEmpty) {
        tile1.adjacentTiles[tile2.id] = AdjacentTile(tile2.id, adj.first);
        tile2.adjacentTiles[tile1.id] = AdjacentTile(tile1.id, adj.first);
      }
    }
    // printAdjacentTiles();
  }

  void alignTiles() {
    var startingTile = cornerTiles()[0];
    // print(startingTile);
    // return;

    startingTile.aligned = true;
    alignAdjacent(startingTile);

    print('===============================');
    printTiles();
  }

  //tile1 must bealigned before this method is invoked
  void alignAdjacent(Tile tile1) {
    print('Aligning tiles adjacent to: $tile1 ----------------------');

    for (var adjacent in tile1.adjacentTiles.values) {
      var tile2 = tiles[adjacent.id];
      print('     Processing $tile2');
      if (!tile2.aligned) {
        var edge = tile1.edge(adjacent.commonEdge);
        var targetLocation = Tile.alignsWith[edge.location];
        tile1.edges[edge.location] = tile2.id;

        if (!tile2.alignEdges(targetLocation, edge.value)) {
          tile2.flip();
          if (!tile2.alignEdges(targetLocation, edge.value)) {
            throw 'Cannot align ${tile2.id} with ${tile1.id}';
          }
        }
        tile2.aligned = true;
        alignAdjacent(tile2);
      } else {
        print('${tile2.id} aligned');
      }
    }
  }

  List<Tile> cornerTiles() =>
      tiles.values.where((t1) => t1.adjacentTiles.keys.length == 2).toList();

  //part 1 solution
  int cornerIdMultiplier() => cornerTiles().map((t2) => t2.id).multiply;

  void printTiles() {
    tiles.entries.forEach((t) {
      print('${t.key}: ${t.value}, ${t.value.edges}');
    });
  }

  void printAdjacentTiles() {
    tiles.values.forEach((t) {
      print('${t.id}: ${t.adjacentTiles}');
    });
  }
}

void runPart1(String name, Image image) {
  printHeader(name);
  image.findAdjacentTiles();
  print(image.cornerIdMultiplier());
  // image.alignEdges();
}

void runPart2(String name, Image image) {
  printHeader(name);
  //0. align tiles
  //1. remove border (outer four tiles) of all tiles
  //2. merge tiles into one image
  //3. look for sea monsters, rotating and flipping until found
  //4. mark sea monsters with 0
  //5. return number of # that are not part of sea monster
  image.findAdjacentTiles();
  // print(image.cornerIdMultiplier());
  // print(image.tiles[0]);
  // print(image.tiles[0].rotate90());
  // print(image.tiles[0].flip());
  // image.alignEdges();
  image.alignTiles();
}

void main(List<String> arguments) {
  TEST_INPUT = Image(readFile('../data/day20-test.txt'));
  MAIN_INPUT = Image(readFile('../data/day20.txt'));

  //Answer: 1951 * 3079 * 2971 * 1171 = 20899048083289
  runPart1('20 test part 1', TEST_INPUT);
  //Answer:
  runPart2('20 test part 2', TEST_INPUT);

  //Answer: 22878471088273
  // runPart1('20 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('20 part 2', MAIN_INPUT);
}
