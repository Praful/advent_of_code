import 'dart:math' as math;

void printHeader(String day) => print('=== Day $day ====================');

extension Iterable2 on Iterable<int> {
  int get max => reduce(math.max);
  int get min => reduce(math.min);
}
