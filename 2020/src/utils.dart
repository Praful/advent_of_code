import 'dart:io';
import 'dart:math' as math;
import 'dart:collection' show Queue;

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

extension String2 on String {
  String replaceCharAt(int index, String newChar) {
    return substring(0, index) + newChar + substring(index + 1);
  }
}

extension Iterable2 on Iterable<int> {
  int get max => reduce(math.max);
  int get min => reduce(math.min);
}

extension Range on num {
  /// Range is inclusive, ie num >= from && num <= to
  bool isBetweenI(num from, num to) => from <= this && this <= to;

  /// Range is exclusive, ie num > from && num < to
  bool isBetween(num from, num to) => from < this && this < to;
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
