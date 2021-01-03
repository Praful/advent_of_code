import 'dart:io';
import 'dart:math' as math;
import 'dart:collection' show Queue;

void printHeader(String day) => print('=== Day $day ====================');

String readFile(input) {
  return File(input).readAsStringSync();
}

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

extension String2 on String {
  String replaceCharAt(int index, String newChar) =>
      substring(0, index) + newChar + substring(index + 1);

  String get reversed => split('').reversed.join('');

  int parseInt() {
    return int.parse(this);
  }
}

extension Iterable2 on Iterable<int> {
  int get max => reduce(math.max);
  int get min => reduce(math.min);
  int get sum => reduce((a, b) => a + b);
  int get multiply => reduce((a, b) => a * b);
}

extension Num2 on num {
  /// Range is inclusive, ie num >= from && num <= to
  bool isBetweenI(num from, num to) => from <= this && this <= to;

  /// Range is exclusive, ie num > from && num < to
  bool isBetween(num from, num to) => from < this && this < to;
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
