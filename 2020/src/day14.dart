import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List MAIN_INPUT;

class Computer {
  final List<String> input;
  static const MASK = 'mask';
  static const MEM = 'mem';
  static final MEM_REGEX =
      RegExp(r'^mem\[(?<address>\d*)\]\s=\s(?<value>\d+)$');
  static const LEAVE = 'X';

  Computer(this.input);

  BigInt maskAsAnd(String mask) =>
      BigInt.parse(mask.replaceAll(LEAVE, '1'), radix: 2);
  BigInt maskAsOr(String mask) =>
      BigInt.parse(mask.replaceAll(LEAVE, '0'), radix: 2);

  BigInt updateAddress(String mask, int value) {
    var result = BigInt.from(value);
    if (mask.isNotEmpty) {
      result = maskAsAnd(mask) & result;
      result = maskAsOr(mask) | result;
    }
    return result;
  }

  BigInt memorySum(Map memory) {
    return memory.values.fold(BigInt.zero, (acc, value) => acc + value);
  }

  void run() {
    assert(input != null);
    String getMask(String s) => s.split('=')[1].trim();
    var mask = '';
    var memory = {};
    input.forEach((instruction) {
      if (instruction.startsWith(MASK)) {
        mask = getMask(instruction);
      } else if (instruction.startsWith(MEM)) {
        var match = MEM_REGEX.firstMatch(instruction);
        var address = int.parse(match.namedGroup('address'));
        var value = int.parse(match.namedGroup('value'));
        memory[address] = updateAddress(mask, value);
      }
    });

    // print(mask);
    // print(memory);
    print(memorySum(memory));
  }
}

void runPart1(String name, List input) {
  printHeader(name);
  Computer(input).run();
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day14-test.txt');
  MAIN_INPUT = fileAsString('../data/day14.txt');

  //Answer:
  runPart1('12 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('12 test part 2', TEST_INPUT);

  //Answer:
  runPart1('12 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('12 part 2', MAIN_INPUT);
}
