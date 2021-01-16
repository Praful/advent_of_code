import '../../shared/dart/src/utils.dart';
// import 'package:trotter/trotter.dart';

enum Mode { position, immediate }

class Opcode {
  static const ADD = 1;
  static const MULTIPY = 2;
  static const WRITE = 3;
  static const OUTPUT = 4;
  static const JMP_TRUE = 5;
  static const JMP_FALSE = 6;
  static const LESS_THAN = 7;
  static const EQUALS = 8;
  static const HALT = 99;
  static const MAX_LENGTH = 4;

  final int opcodeId;
  final Instruction Function(List<int>) create;
  final length; //no of params in instruction
  Opcode(this.opcodeId, this.create, this.length);

  static final Map<int, Opcode> entries = {}
    ..[Opcode.ADD] = Opcode(Opcode.ADD, (a) => Add(a), 4)
    ..[Opcode.MULTIPY] = Opcode(Opcode.MULTIPY, (a) => Multiply(a), 4)
    ..[Opcode.WRITE] = Opcode(Opcode.WRITE, (a) => Write(a), 2)
    ..[Opcode.OUTPUT] = Opcode(Opcode.OUTPUT, (a) => Output(a), 2)
    ..[Opcode.HALT] = Opcode(Opcode.HALT, (a) => Halt(a), 1);
}

abstract class Instruction {
  static const MAX_LENGTH = 4;

  static final modes = {}
    ..[0] = Mode.position
    ..[1] = Mode.immediate;

  List<int> instruction;
  Opcode opcode;
  Map<int, Parameter> parameters = {};

  @override
  String toString() => 'param: $instruction\nparams: $parameters';
  List<int> apply(List<int> memory) => memory;
  int get length => opcode.length;

  Instruction(this.instruction) {
    opcode = Opcode.entries[opcodeId(instruction[0])];
    var modes = parseModes(instruction[0]);
    parameters
      ..[1] = Parameter(instruction[1], modes[0])
      ..[2] = Parameter(instruction[2], modes[1])
      ..[3] = Parameter(instruction[3], modes[2]);
  }

  //param 1 of form ABCDE where
  //DE = op code, C = mode of param1, B = mode of param2, A = mode of param3
  List parseModes(int opdata) {
    var opdataStr = opdata.toString().padLeft(5, '0');
    return [
      Instruction.modes[opdataStr[2].toInt()],
      Instruction.modes[opdataStr[1].toInt()],
      Instruction.modes[opdataStr[0].toInt()]
    ];
  }

  //Return opcode value, extracted from param1 described in parseModes().
  static int opcodeId(int param1) {
    var s = param1.toString();
    return s.length < 3 ? s.toInt() : s.substring(s.length - 2).toInt();
  }

  //Return a specific Instruction object eg Add, Multiply, Halt, etc, Multiply, Halt, etc.
  factory Instruction.create(int code, List<int> instruction) =>
      opcodes[opcodeId(code)].create(instruction);
}

class Parameter {
  final int value;
  final Mode mode;
  Parameter(this.value, this.mode);
  int read(memory) {
    switch (mode) {
      case Mode.position:
        return memory[value];
        break;
      case Mode.immediate:
        return value;
        break;
      default:
        throw 'Invalid mode $mode';
    }
  }

  @override
  String toString() => 'Param: $value, mode: $mode';
}

class Add extends Instruction {
  Add(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    // print('Add: $operand1 and $operand2. Store at: $storeAddress');
    memory[parameters[3].value] =
        parameters[1].read(memory) + parameters[2].read(memory);
    return memory;
  }
}

class Multiply extends Instruction {
  Multiply(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    // print('Multiply: $operand1 and $operand2. Store at: $storeAddress');
    memory[parameters[3].value] =
        parameters[1].read(memory) * parameters[2].read(memory);
    return memory;
  }
}

class Write extends Instruction {
  Write(instruction) : super(instruction); //todo

  @override
  List<int> apply(List<int> memory) {
    // print('Write: $param2. Store at: $storeAddress');
    memory[parameters[1].value] = parameters[2].value;
    return memory;
  }
}

class Output extends Instruction {
  Output(param) : super(param);

  @override
  List<int> apply(List<int> memory) {
    // print('Output: $param2. Store at: $storeAddress');
    print(memory[parameters[1].value]);
    return memory;
  }
}

class Halt extends Instruction {
  Halt(param) : super(param);
  // @override
  // int get length => Instruction.increment[Instruction.OPCODE_HALT];

  // @override
  // List<int> apply(List<int> memory) {
  // do nothing
  // return memory;
  // }
}

class Computer {
  List<int> memory;
  Computer(data) {
    memory = List.from(data);
  }

  Object run(returnAddress, input) {
    var pc = 0; //program counter
    var opcode = 0;
    while (true) {
      opcode = memory[pc];
      if (opcode == Opcode.HALT) break;

      var params = memory.getRange(pc, pc + Instruction.MAX_LENGTH).toList();
      if (opcode == Opcode.WRITE) params[2] = input;
      var instruction = Instruction.create(opcode, params);
      // print('------------------------------');
      // print(instruction);
      instruction.apply(memory);
      pc += instruction.length;
      // print(memory);
      // print('counter: $pc');
    }
    // print(input);
    return memory[returnAddress];
  }
}
