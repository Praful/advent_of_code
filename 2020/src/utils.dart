import 'dart:math' as math;

void printHeader(String day) => print('=== Day $day ====================');

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
