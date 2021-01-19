import 'dart:math' as math;
import '../../shared/dart/src/utils.dart';

// extension IterableNum<T extends num> on Iterable<T> {
//   T get max => reduce(math.max);
//   T get min => reduce(math.min);
//   T get sum => reduce((a, b) => a + b as T);
// }

void test1() {
  print([1.2, 1.3, 5, 2.2].sum); //works
  print([1.2, 1.3, 5, 2.2].max); //works
  print([1.2, 1.3, 5.3, 2.2].min); //works
  print([1.2, 1.3, 5.0, 2.2].sum); //does not work

  //these don't work
  print([1, 2, 3].max);
  print([1, 2, 3].min);
  print([1, 2, 3].sum);
}

void test2() {
  print('eeeeddabcde'.where((c) => c == 'c').length);
}

void main(List<String> args) {
  // test1();
  test2();
}
