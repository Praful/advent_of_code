import 'dart:io';
import 'dart:math' as math;

void printHeader(String day) => print('=== Day $day ====================');

List<String> fileAsString(input, [sort = false]) {
  var result = File(input).readAsLinesSync();
  if (sort) result.sort();
  return result;
}

List<int> fileAsInt(input, [sort = false]) {
  var result = File(input).readAsLinesSync().map((l) => int.parse(l)).toList();
  if (sort) result.sort();
  return result;
}

extension Iterable2 on Iterable<int> {
  int get max => reduce(math.max);
  int get min => reduce(math.min);
}

extension Range on num {
  /// Range is exclusive, ie num > from && num < to
  bool isBetween(num from, num to) {
    return from < this && this < to;
  }
}
