import './utils.dart';
import 'package:trotter/trotter.dart';
import 'dart:math' as math;

const bool DEBUG = false;

Image TEST_INPUT;
Image TEST_INPUT2;
Image MAIN_INPUT;

class Point {
  final int row;
  final int col;
  Point(this.row, this.col);

  Point operator +(Point other) => Point(row + other.row, col + other.col);

  @override
  String toString() => '$row, $col';
}

class AdjacentTile {
  final int id;
  final String sharedBorder;
  AdjacentTile(this.id, this.sharedBorder);

  @override
  String toString() => '$id: $sharedBorder';
}

enum Location { top, bottom, left, right }

class Edge {
  final Location location;
  final String border;
  Edge(this.location, this.border);

  @override
  String toString() => '$location, $border';
}

class Tile {
  final input;
  int id;
  List<String> tile;
  Map<String, Edge> possibleEdges;
  Map<int, AdjacentTile> adjacentTiles = {};
  bool aligned = false;
  Map<Location, int> edges = {};
  static const NUM_SIDES = 4; //sides of tile!

  // Map<Side, Function> enumToMethod;

  //Align top with bottom, left with right, etc
  static Map<Location, Location> alignsWith = {}
    ..[Location.left] = Location.right
    ..[Location.right] = Location.left
    ..[Location.top] = Location.bottom
    ..[Location.bottom] = Location.top;

  Tile([this.input]) {
    if (input != null) parseInput();

    // TODO how do you map enum to getter or method?
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
  bool alignEdges(Location location, String border) {
    // print('aligning $location for $border');
    for (var n = 0; n < Tile.NUM_SIDES; n++) {
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
          throw 'Invalid border for location $location';
      }
      if (target == border) return true;
      rotate90();
    }
    return false;
  }

  void rotate90() {
    var result = <String>[];
    for (var i = 0; i < tile.length; i++) {
      result.add(tile.reversed.map((line) => line[i]).join());
    }
    tile = result;
  }

  void flip() {
    tile = tile.reversed.toList();
  }

  List get withoutBorder {
    var result = List.from(tile)
      ..removeLast()
      ..removeAt(0);
    return result.map((e) => e.substring(1, e.length - 1)).toList();
  }

  //Return Edge object with location of border and border as it is
  //on the tile.
  Edge edge(String border) {
    bool equals(String a, String b) => (a == b) || (a == b.reversed);

    if (equals(border, top)) return Edge(Location.top, top);
    if (equals(border, bottom)) return Edge(Location.bottom, bottom);
    if (equals(border, left)) return Edge(Location.left, left);
    if (equals(border, right)) return Edge(Location.right, right);
    throw '$border is not on any side of the tile';
  }

  String get top => tile[0];
  String get bottom => tile.last;
  String get left => tile.map((line) => line[0]).join();
  String get right => tile.map((line) => line[line.length - 1]).join();

  @override
  String toString() =>
      '$id: ${edges}${adjacentTiles.values}\n${tile.join('\n')}';
}

class Image {
  Map<int, Tile> tiles;
  final String input;
  var tileIdGrid;
  List<String> mergedImage;
  int monstersFound;

  static RegExp testMonsterRegex = RegExp(
      '(?<=#.{5})#.{4}#{2}.{4}#{2}.{4}#{3}(?=.{5}#.{2}#.{2}#.{2}#.{2}#.{2}#)');

  static RegExp monsterRegex = RegExp(
      '(?<=#.{77})#.{4}#{2}.{4}#{2}.{4}#{3}(?=.{77}#.{2}#.{2}#.{2}#.{2}#.{2}#)');

  static const SEA_MONSTER = '                  # '
      '#    ##    ##    ###'
      ' #  #  #  #  #  #   ';

  Image(this.input) {
    tiles = {for (var e in parseInput()) e.id: e};

    var size = math.sqrt(tiles.entries.length).round();
    //2D square array
    tileIdGrid = List.generate(size, (i) => List(size), growable: false);
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
  }

  //We want the corner tile we process to be [0, 0] in grid
  //we create. Rotate until it's the top left hand corner of square.
  void makeTopLeft(Tile cornerTile) {
    bool isCorrectOrientation(Set s1, Set s2) =>
        (s1.intersection(s2)).length == 2;

    var border1 = cornerTile.adjacentTiles.values.toList()[0].sharedBorder;
    var border2 = cornerTile.adjacentTiles.values.toList()[1].sharedBorder;

    var targetOrientation = <Location>{Location.right, Location.bottom};

    for (var corners = 0; corners < Tile.NUM_SIDES; corners++) {
      if (isCorrectOrientation({
        cornerTile.edge(border1).location,
        cornerTile.edge(border2).location
      }, targetOrientation)) return;

      cornerTile.rotate90();
    }
    throw 'Could not make corner tile top left';
  }

  void alignTiles() {
    var startTile = cornerTiles()[0]..aligned = true;
    var startPoint = Point(0, 0);

    makeTopLeft(startTile);
    alignAdjacent(startTile);

    tileIdGrid[startPoint.row][startPoint.col] = startTile.id;
    createTileIdGrid(startTile, startPoint);
  }

  void createMergedImage() {
    var trimmedTileLength = tiles[tiles.keys.first].withoutBorder.length;

    //REMOVE - test with untrimmed tile
    // trimmedTileLength = tiles[tiles.keys.first].tile.length;

    mergedImage = List<String>.generate(
        tileIdGrid.length * trimmedTileLength, (int i) => '');

    // print(mergedImage.length);

    for (var row = 0; row < tileIdGrid.length; row++) {
      for (var col = 0; col < tileIdGrid.length; col++) {
        //
        var trimmedTile = tiles[tileIdGrid[row][col]].withoutBorder;
        //REMOVE - test with untrimmed; useful to print merged image
        // trimmedTile = tiles[tileIdGrid[row][col]].tile;
        for (var tileIndex = 0; tileIndex < trimmedTile.length; tileIndex++) {
          var mergedIndex = row * trimmedTileLength + tileIndex;
          //add + ' ' to separate tiles for testing
          mergedImage[mergedIndex] += trimmedTile[tileIndex]; // + ' ';
        }
      }
    }
  }

  static Map<Location, Point> directionVector = {}
    ..[Location.top] = Point(-1, 0)
    ..[Location.bottom] = Point(1, 0)
    ..[Location.left] = Point(0, -1)
    ..[Location.right] = Point(0, 1);

  //create grid with just IDs (not the tiles) eg:
  // 1234 3455 2342
  // 3456 7643 1322
  // 5456 4643 4322
  void createTileIdGrid(Tile start, Point pos) {
    start.edges.entries.forEach((t) {
      var newPos = pos + Image.directionVector[t.key];
      tileIdGrid[newPos.row][newPos.col] = t.value;
      createTileIdGrid(tiles[t.value], newPos);
    });
  }

  //tile1 must be aligned before this method is invoked
  void alignAdjacent(Tile tile1) {
    // print('Aligning tiles adjacent to: $tile1 ----------------------');

    for (var adjacent in tile1.adjacentTiles.values) {
      var tile2 = tiles[adjacent.id];
      // print('     Processing $tile2');
      if (!tile2.aligned) {
        var edge = tile1.edge(adjacent.sharedBorder);
        var targetLocation = Tile.alignsWith[edge.location];
        tile1.edges[edge.location] = tile2.id;

        if (!tile2.alignEdges(targetLocation, edge.border)) {
          tile2.flip();
          if (!tile2.alignEdges(targetLocation, edge.border)) {
            throw 'Cannot align ${tile2.id} with ${tile1.id}';
          }
        }
        tile2.aligned = true;
        alignAdjacent(tile2);
      }
    }
  }

  void findMonsters(regex) {
    monstersFound = 0;
    var merged = Tile()..tile = mergedImage;

    void doSearch() {
      for (var i = 0; i < Tile.NUM_SIDES; i++) {
        monstersFound = regex.allMatches(merged.tile.join('')).toList().length;
        if (monstersFound > 0) return;
        merged.rotate90();
      }
    }

    doSearch();
    if (monstersFound == 0) {
      merged.flip();
      doSearch();
    }
  }

  List<Tile> cornerTiles() =>
      tiles.values.where((t1) => t1.adjacentTiles.keys.length == 2).toList();

  //part 1 solution
  int cornerIdMultiplier() => cornerTiles().map((t2) => t2.id).multiply;

  //part 2 solution
  int waterRoughness() {
    int count(list) => list.fold(0, (sum, v) => sum + (v == '#' ? 1 : 0));

    var total = mergedImage.fold(0, (sum, v) => sum + (count(v.split(''))));
    var perMonster = count(SEA_MONSTER.split(''));
    // print(
    //     'total: $total, per monster: $perMonster, monsters found: $monstersFound');
    return total - (perMonster * monstersFound);
  }

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
}

void runPart2(String name, Image image, RegExp regex) {
  printHeader(name);
  image
    ..findAdjacentTiles()
    ..alignTiles()
    ..createMergedImage()
    ..findMonsters(regex);

  print('water roughness: ${image.waterRoughness()}');
}

void main(List<String> arguments) {
  TEST_INPUT = Image(readFile('../data/day20-test.txt'));
  MAIN_INPUT = Image(readFile('../data/day20.txt'));

  //Answer: 1951 * 3079 * 2971 * 1171 = 20899048083289
  runPart1('20 test part 1', TEST_INPUT);
  //Answer: 273 (303 - two monsters; each monster is 15 #'s)
  runPart2('20 test part 2', TEST_INPUT, Image.testMonsterRegex);

  //Answer: 22878471088273
  runPart1('20 part 1', MAIN_INPUT);
  //Answer: 1680 (2130 - 30 monsters)
  runPart2('20 part 2', MAIN_INPUT, Image.monsterRegex);
}
