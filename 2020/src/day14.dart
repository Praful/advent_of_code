import '../../shared/dart/src/utils.dart';
import 'dart:math' as math;

const bool DEBUG = false;

class Computer {
  final List<String> input;
  static const MASK = 'mask';
  static const MEM = 'mem';
  static final MEM_REGEX =
      RegExp(r'^mem\[(?<address>\d*)\]\s=\s(?<value>\d+)$');
  static const X = 'X';
  static final X_REGEX = RegExp(X);
  static const MASK_BITS = 36;

  Computer(this.input);

  BigInt maskAsAnd(String mask) =>
      BigInt.parse(mask.replaceAll(X, '1'), radix: 2);
  BigInt maskAsOr(String mask) =>
      BigInt.parse(mask.replaceAll(X, '0'), radix: 2);
  String getMask(String s) => s.split('=')[1].trim();
  BigInt memorySum(Map memory) =>
      memory.values.fold(BigInt.zero, (acc, value) => acc + value);
  String addLeadingZeroes(s, count) => s.padLeft(count, '0');

  void run() {
    BigInt updatedValue(String mask, int value) {
      var result = BigInt.from(value);
      if (mask.isNotEmpty) {
        result = maskAsAnd(mask) & result;
        result = maskAsOr(mask) | result;
      }
      return result;
    }

    var mask = '';
    var memory = {};

    input.forEach((instruction) {
      if (instruction.startsWith(MASK)) {
        mask = getMask(instruction);
      } else if (instruction.startsWith(MEM)) {
        var match = MEM_REGEX.firstMatch(instruction)!;
        var address = int.parse(match.namedGroup('address')!);
        var value = int.parse(match.namedGroup('value')!);
        memory[address] = updatedValue(mask, value);
      }
    });

    print(memorySum(memory));
  }

  // if mask is 110X010X0X and replaceXwith is 001, then the first
  // X becomes 0, the second 0 and the third 1. The replacement
  // occurs in maskedAddress eg if X index is 3 in mask, then character
  // at index 3 is changed in maskedAddress.
  String generateNewAddress(
      String mask, String maskedAddress, String replaceXwith) {
    var result = addLeadingZeroes(maskedAddress, MASK_BITS);
    var index = 0;
    replaceXwith.split('').forEach((c) {
      index = mask.indexOf(X, index);
      result = result.replaceCharAt(index, c);
      index += 1;
    });
    return result;
  }

  String generateMaskedAddress(mask, address) {
    return (maskAsOr(mask) | BigInt.from(address)).toRadixString(2);
  }

  //1. apply mask to address - m1
  //2. for the number of X's generate all perm of m1
  List<String> memoryAddressesToUpdate(String mask, int address) {
    var result = <String>[];
    var xCount = X.allMatches(mask).length;
    var newAddressCount = math.pow(2, xCount);
    var maskedAddress = generateMaskedAddress(mask, address);

    for (var i = 0; i < newAddressCount; i++) {
      var replaceXwith = i.toRadixString(2);
      result.add(generateNewAddress(
          mask, maskedAddress, addLeadingZeroes(replaceXwith, xCount)));
    }
    return result;
  }

  void run2() {
    var mask = '';
    var memory = {};

    input.forEach((instruction) {
      if (instruction.startsWith(MASK)) {
        mask = getMask(instruction);
      } else if (instruction.startsWith(MEM)) {
        var match = MEM_REGEX.firstMatch(instruction)!;
        var address = int.parse(match.namedGroup('address')!);
        var value = int.parse(match.namedGroup('value')!);

        memoryAddressesToUpdate(mask, address)
            .forEach((a) => memory[a] = BigInt.from(value));
      }
    });

    print(memorySum(memory));
  }
}

void runPart1(String name, List<String> input) {
  printHeader(name);
  Computer(input).run();
}

void runPart2(String name, List<String> input) {
  printHeader(name);
  Computer(input).run2();
}

void main(List<String> arguments) {
  var TEST_INPUT = FileUtils.asLines('../data/day14-test.txt');
  var TEST_INPUT2 = FileUtils.asLines('../data/day14b-test.txt');
  var MAIN_INPUT = FileUtils.asLines('../data/day14.txt');

  //Answer: 165
  runPart1('14 test part 1', TEST_INPUT);
  //Answer: 208
  runPart2('14 test part 2', TEST_INPUT2);

  //Answer: 5875750429995
  runPart1('14 part 1', MAIN_INPUT);
  //Answer: 5272149590143
  runPart2('14 part 2', MAIN_INPUT);
}
