import './utils.dart';
import 'dart:math' as math;

//Requires following line to be added as dependency in pubspec.yaml:
//   trotter: any
//Remember to get package. In VS Code, right click pubspec.yaml and
//click Get Packages.
import 'package:trotter/trotter.dart';

const bool DEBUG = false;

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
  final _input;
  int id;
  List<String> tile;
  Map<String, Edge> possibleEdges;
  final Map<int, AdjacentTile> adjacentTiles = {};
  bool aligned = false;
  final Map<Location, int> edges = {};
  static const SIDES_COUNT = 4; //sides of tile! Used for rotations.

  final Map<Location, Function> _locationToBorderMapping = {};

  static Tile from(List<String> t) => Tile()..tile = t;

  //Align top with bottom, left with right, etc
  static final Map<Location, Location> alignsWith = {}
    ..[Location.left] = Location.right
    ..[Location.right] = Location.left
    ..[Location.top] = Location.bottom
    ..[Location.bottom] = Location.top;

  Tile([this._input]) {
    if (_input != null) _parseInput();

    //map location to getter for location
    _locationToBorderMapping[Location.bottom] = () => bottom;
    _locationToBorderMapping[Location.top] = () => top;
    _locationToBorderMapping[Location.left] = () => left;
    _locationToBorderMapping[Location.right] = () => right;
  }

  void _parseInput() {
    tile = _input.split('\n');
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

  //Return true if we managed to find tile border at the location
  bool alignSharedBorder(Location location, String border) {
    for (var _ in range(0, Tile.SIDES_COUNT)) {
      if (border == _locationToBorderMapping[location]()) return true;
      rotate90();
    }
    return false;
  }

  void rotate90() {
    var result = <String>[];
    for (var i in range(0, tile.length)) {
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
  final String _input;
  var tileIdGrid;
  List<String> mergedImage;
  int monstersFound;

  static const SEA_MONSTER = '                  # '
      '#    ##    ##    ###'
      ' #  #  #  #  #  #   ';

  Image(this._input) {
    tiles = {for (var e in _parseInput()) e.id: e};

    var size = math.sqrt(tiles.entries.length).round();
    //2D square array
    tileIdGrid = List.generate(size, (i) => List(size), growable: false);
  }

  List<Tile> _parseInput() => _input
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
  void _makeTopLeft(Tile cornerTile) {
    bool isCorrectOrientation(Set s1, Set s2) =>
        (s1.intersection(s2)).length == 2;

    var border1 = cornerTile.adjacentTiles.values.toList()[0].sharedBorder;
    var border2 = cornerTile.adjacentTiles.values.toList()[1].sharedBorder;

    var targetOrientation = <Location>{Location.right, Location.bottom};

    for (var _ in range(0, Tile.SIDES_COUNT)) {
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

    _makeTopLeft(startTile);
    _alignAdjacent(startTile);

    tileIdGrid[startPoint.row][startPoint.col] = startTile.id;
    _createTileIdGrid(startTile, startPoint);
  }

  void createMergedImage() {
    var trimmedTileLength = tiles[tiles.keys.first].withoutBorder.length;

    mergedImage = List<String>.generate(
        tileIdGrid.length * trimmedTileLength, (int i) => '');

    for (var row in range(0, tileIdGrid.length)) {
      for (var col in range(0, tileIdGrid.length)) {
        var trimmedTile = tiles[tileIdGrid[row][col]].withoutBorder;
        for (var tileIndex in range(0, trimmedTile.length)) {
          var mergedIndex = row * trimmedTileLength + tileIndex;
          mergedImage[mergedIndex] += trimmedTile[tileIndex];
        }
      }
    }
  }

  static final Map<Location, Point> _directionVector = {}
    ..[Location.top] = Point(-1, 0)
    ..[Location.bottom] = Point(1, 0)
    ..[Location.left] = Point(0, -1)
    ..[Location.right] = Point(0, 1);

  //create grid with just IDs (not the tiles) eg:
  // 1234 3455 2349
  // 3759 7641 1321
  // 5456 4643 4322
  void _createTileIdGrid(Tile start, Point pos) {
    start.edges.entries.forEach((t) {
      var newPos = pos + Image._directionVector[t.key];
      tileIdGrid[newPos.row][newPos.col] = t.value;
      _createTileIdGrid(tiles[t.value], newPos);
    });
  }

  //tile1 must be aligned before this method is invoked
  void _alignAdjacent(Tile tile1) {
    for (var adjacent in tile1.adjacentTiles.values) {
      var tile2 = tiles[adjacent.id];
      if (!tile2.aligned) {
        var edge = tile1.edge(adjacent.sharedBorder);
        var targetLocation = Tile.alignsWith[edge.location];
        tile1.edges[edge.location] = tile2.id;

        if (!tile2.alignSharedBorder(targetLocation, edge.border)) {
          tile2.flip();
          if (!tile2.alignSharedBorder(targetLocation, edge.border)) {
            throw 'Cannot align ${tile2.id} with ${tile1.id}';
          }
        }
        tile2.aligned = true;
        _alignAdjacent(tile2);
      }
    }
  }

  void findMonsters() {
    monstersFound = 0;
    var merged = Tile.from(mergedImage);
    var gap = mergedImage.length - (SEA_MONSTER.length ~/ 3) + 1;

    var monsterRegex = RegExp(
        '(?<=#.{$gap})#.{4}#{2}.{4}#{2}.{4}#{3}(?=.{$gap}#.{2}#.{2}#.{2}#.{2}#.{2}#)');

    void doSearch() {
      for (var _ in range(0, Tile.SIDES_COUNT)) {
        monstersFound =
            monsterRegex.allMatches(merged.tile.join('')).toList().length;
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
  int get waterRoughness {
    int count(list) => list.fold(0, (sum, v) => sum + (v == '#' ? 1 : 0));

    var total = mergedImage.fold(0, (sum, v) => sum + (count(v.split(''))));
    var perMonster = count(SEA_MONSTER.split(''));
    return total - (perMonster * monstersFound);
  }

  void printMergedImageWithBorders() {
    var tileLength = tiles[tiles.keys.first].tile.length;
    var merged =
        List<String>.generate(tileIdGrid.length * tileLength, (int i) => '');

    for (var row in range(0, tileIdGrid.length)) {
      for (var col in range(0, tileIdGrid.length)) {
        var tile = tiles[tileIdGrid[row][col]].tile;
        for (var tileIndex in range(0, tile.length)) {
          var mergedIndex = row * tileLength + tileIndex;
          merged[mergedIndex] += tile[tileIndex] + ' ';
        }
      }
    }
    print(merged.join('\n'));
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

void runPart2(String name, Image image) {
  printHeader(name);
  image
    ..findAdjacentTiles()
    ..alignTiles()
    // ..printMergedImageWithBorders()
    ..createMergedImage()
    ..findMonsters();

  print('water roughness: ${image.waterRoughness}');
}

void main(List<String> arguments) {
  var TEST_INPUT = Image(readFile('../data/day20-test.txt'));
  var MAIN_INPUT = Image(readFile('../data/day20.txt'));

  //Answer: 1951 * 3079 * 2971 * 1171 = 20899048083289
  runPart1('20 test part 1', TEST_INPUT);
  //Answer: 273 (303 - two monsters; each monster is 15 #'s)
  runPart2('20 test part 2', TEST_INPUT);

  //Answer: 22878471088273
  runPart1('20 part 1', MAIN_INPUT);
  //Answer: 1680 (2130 - 30 monsters)
  runPart2('20 part 2', MAIN_INPUT);
}
