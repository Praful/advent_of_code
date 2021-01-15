import 'dart:io';
import 'dart:math' as math;
import 'dart:collection' show Queue;

void printHeader(String header) =>
    print('=== Day $header ====================');

void assertEqual(found, expected) {
  try {
    assert(found == expected);
  } catch (e, stacktrace) {
    print(
        'Failed assertion: found $found, expected $expected\n\n${stacktrace}');
  }
}

class FileUtils {
  static String asString(input) => File(input).readAsStringSync();

  static List<String> asLines(input, [sort = false]) {
    var result = File(input).readAsLinesSync();
    if (sort) result.sort();
    return result;
  }

  static List<int> asInt(input, [sort = false]) {
    var result = File(input).readAsLinesSync().map((l) => l.toInt()).toList();
    if (sort) result.sort();
    return result;
  }
}

extension String2 on String {
  String replaceCharAt(int index, String newChar) =>
      substring(0, index) + newChar + substring(index + 1);

  String get reversed => split('').reversed.join('');

  int toInt() {
    return int.parse(this);
  }
}

class NumUtils {
  static T sum<T extends num>(T a, T b) => a + b;
  static T multiply<T extends num>(T a, T b) => a * b;
}

extension IterableNum on Iterable<num> {
  num get max => fold(first, math.max);
  num get min => fold(first, math.min);
  num get sum => fold(0, (a, b) => a + b);
  num get multiply => fold(1, (a, b) => a * b);

  //these don't work for int; ok for double!
  // num get max => reduce(math.max);
  // num get min => reduce(math.min);
  // num get sum => reduce(NumUtils.sum);
  // num get multiply => reduce(NumUtils.multiply);
}

extension GeneralIterableExtension<T> on Iterable<T> {
  num fold2(num Function(T) convert) => fold(0, (a, b) => a + convert(b));
}

extension Num2 on num {
  /// Range is inclusive, ie num >= from && num <= to
  bool isBetween(num from, num to) => from <= this && this <= to;

  /// Range is exclusive, ie num > from && num < to
  bool isBetweenX(num from, num to) => from < this && this < to;
}

//Two ways for range. See
// https://stackoverflow.com/questions/37798397/dart-create-a-list-from-0-to-n
// See quiver package for useful libaries.
// eg 0.to(10).forEach(....
// range(1,10).map()....
// extension Int2 on int {
//   List<int> to(int maxExclusive, [int step = 1]) =>
//       [for (int i = this; i < maxExclusive; i += step) i];
// }

Iterable<int> range(int lowInclusive, int highExclusive) sync* {
  for (var i = lowInclusive; i < highExclusive; ++i) {
    yield i;
  }
}

class Stack<T> {
  final Queue<T> _underlyingQueue;

  Stack() : _underlyingQueue = Queue<T>();

  int get length => _underlyingQueue.length;
  bool get isEmpty => _underlyingQueue.isEmpty;
  bool get isNotEmpty => _underlyingQueue.isNotEmpty;

  void clear() => _underlyingQueue.clear();

  T peek() {
    if (isEmpty) {
      throw StateError('Cannot peek() on empty stack.');
    }
    return _underlyingQueue.last;
  }

  T pop() {
    if (isEmpty) {
      throw StateError('Cannot pop() on empty stack.');
    }
    return _underlyingQueue.removeLast();
  }

  @override
  String toString() {
    return _underlyingQueue.toString();
  }

  void push(final T element) => _underlyingQueue.addLast(element);
}
