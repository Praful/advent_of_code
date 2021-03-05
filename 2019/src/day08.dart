import '../../shared/dart/src/utils.dart';
import 'package:collection/collection.dart';

/// Puzzle description: https://adventofcode.com/2019/day/8

const bool DEBUG = false;
const BLACK = '0';
const WHITE = '1';
const TRANSPARENT = '2';

Map<int, String> toLayers(String input, int width, int height) {
  var totalPixels = width * height;
  var layerCount = range(0, input.length ~/ totalPixels).toList();
  return {
    for (var layerNum in layerCount)
      layerNum: input.substring(
          layerNum * totalPixels, layerNum * totalPixels + totalPixels)
  };
}

Object part1(String header, String input, int width, int height) {
  printHeader(header);
  var layers = toLayers(input, width, height);
  var zeroCounts =
      layers.values.map((l) => l.where((c) => c == BLACK).length).toList();
  var minZerosLayer = layers[zeroCounts.indexOf(zeroCounts.min)]!;
  return minZerosLayer.where((c) => c == WHITE).length *
      minZerosLayer.where((c) => c == TRANSPARENT).length;
}

void part2(String header, String input, int width, int height) {
  printHeader(header);
  var layers = toLayers(input, width, height);
  //merge layers, taking the first non-transparent pixel
  var pixels = IterableZip(layers.values.map((l) => l.split('')))
      .map((vslice) => (vslice.skipWhile((p) => p == TRANSPARENT)).first)
      .join();

  //will depend on user's console colours
  var blackBlock = '\u2588';
  var whiteBlock = '\u2591';

  var image =
      pixels.replaceAll(BLACK, blackBlock).replaceAll(WHITE, whiteBlock);
  for (var i = 0; i < image.length; i += width) {
    print(image.substring(i, i + width));
  }
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asString('../data/day08.txt');

  printAndAssert(part1('08 part 1', mainInput, 25, 6), 2286);
  part2('08 part 2', mainInput, 25, 6); //CJZLP
}
