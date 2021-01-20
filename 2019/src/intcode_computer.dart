import '../../shared/dart/src/utils.dart';
// import 'package:trotter/trotter.dart';

enum Mode { position, immediate, relative }

class Opcode {
  static const ADD = 1;
  static const MULTIPY = 2;
  static const WRITE = 3;
  static const OUTPUT = 4;
  static const JMP_TRUE = 5;
  static const JMP_FALSE = 6;
  static const LESS_THAN = 7;
  static const EQUALS = 8;
  static const RELATIVE_BASE = 9;
  static const HALT = 99;

  final int id;
  final Instruction Function(List<int>) create;
  final length; //no of params in instruction
  Opcode(this.id, this.create, this.length);

  //code is of form ABCDE where DE = op code id.
  //Return opcode id, extracted from param1 described in parseModes().
  static int opcodeId(int code) {
    var s = code.toString().padLeft(5, '0');
    return s.substring(s.length - 2).toInt();
  }

  static final Map<int, Opcode> opcodeMap = {}
    ..[ADD] = Opcode(Opcode.ADD, (a) => Add(a), 4)
    ..[MULTIPY] = Opcode(Opcode.MULTIPY, (a) => Multiply(a), 4)
    ..[WRITE] = Opcode(Opcode.WRITE, (a) => Write(a), 2)
    ..[OUTPUT] = Opcode(Opcode.OUTPUT, (a) => Output(a), 2)
    ..[JMP_TRUE] = Opcode(Opcode.JMP_TRUE, (a) => JumpIfTrue(a), 3)
    ..[JMP_FALSE] = Opcode(Opcode.JMP_FALSE, (a) => JumpIfFalse(a), 3)
    ..[LESS_THAN] = Opcode(Opcode.LESS_THAN, (a) => LessThan(a), 4)
    ..[EQUALS] = Opcode(Opcode.EQUALS, (a) => Equals(a), 4)
    ..[RELATIVE_BASE] = Opcode(Opcode.RELATIVE_BASE, (a) => RelativeBase(a), 2)
    ..[HALT] = Opcode(Opcode.HALT, (a) => Halt(a), 1);
}

abstract class Instruction {
  static final modeMap = {}
    ..[0] = Mode.position
    ..[1] = Mode.immediate
    ..[2] = Mode.relative;

  //instruction consists of code, param1, param2 [,param3]
  //code is of form ABCDE where
  //DE = opcode id, C = mode of param1, B = mode of param2, A = mode of param3
  List<int> instruction;
  Opcode opcode;
  Map<int, Parameter> parameters = {};

  @override
  String toString() => 'param: $instruction\nparams: $parameters';
  Object apply(Map<int, int> memory, int relativeBase) => memory;
  int get length => opcode.length;

  int nextPointer(current) => current + opcode.length;

  Instruction(this.instruction) {
    opcode = Opcode.opcodeMap[Opcode.opcodeId(instruction[0])];
    var modes = parseModes(instruction[0]);
    for (var i in range(1, opcode.length)) {
      parameters[i] = Parameter(instruction[i], modes[i]);
    }
  }

  Map parseModes(int code) {
    var s = code.toString().padLeft(5, '0');
    return {
      1: Instruction.modeMap[s[2].toInt()],
      2: Instruction.modeMap[s[1].toInt()],
      3: Instruction.modeMap[s[0].toInt()]
    };
  }

  //Return a specific Instruction object eg Add, Multiply, Halt, etc,
  factory Instruction.create(int code, List<int> instruction) =>
      Opcode.opcodeMap[Opcode.opcodeId(code)].create(instruction);
}

class Parameter {
  final int value;
  final Mode mode;
  Parameter(this.value, this.mode);

  int withMode(memory, relativeBase, [isWrite = false]) {
    if (isWrite) return value + (mode == Mode.relative ? relativeBase : 0);

    switch (mode) {
      case Mode.position:
        return memory[value] ?? 0;
        break;
      case Mode.immediate:
        return value;
        break;
      case Mode.relative:
        return memory[relativeBase + value] ?? 0;
        break;
      default:
        throw 'Invalid mode $mode';
    }
  }

  @override
  String toString() => 'value: $value, mode: $mode';
}

class Add extends Instruction {
  Add(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    memory[parameters[3].withMode(memory, relativeBase, true)] =
        parameters[1].withMode(memory, relativeBase) +
            parameters[2].withMode(memory, relativeBase);
    return memory;
  }
}

class Multiply extends Instruction {
  Multiply(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    memory[parameters[3].withMode(memory, relativeBase, true)] =
        parameters[1].withMode(memory, relativeBase) *
            parameters[2].withMode(memory, relativeBase);
    return memory;
  }
}

class Write extends Instruction {
  int input;
  Write(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    memory[parameters[1].withMode(memory, relativeBase, true)] = input;
    return memory;
  }
}

class Output extends Instruction {
  Output(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    return parameters[1].withMode(memory, relativeBase);
  }
}

class JumpIfTrue extends Instruction {
  static const NO_CHANGE = -1;
  int lastInstructionPointer;

  JumpIfTrue(instruction) : super(instruction);

  @override
  int nextPointer(old) {
    return (lastInstructionPointer != NO_CHANGE)
        ? lastInstructionPointer
        : super.nextPointer(old);
  }

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    lastInstructionPointer = (parameters[1].withMode(memory, relativeBase) != 0)
        ? parameters[2].withMode(memory, relativeBase)
        : NO_CHANGE;
    return super.apply(memory, relativeBase);
  }
}

class JumpIfFalse extends Instruction {
  static const NO_CHANGE = -1;
  int lastInstructionPointer;
  JumpIfFalse(instruction) : super(instruction);

  @override
  int nextPointer(old) {
    return (lastInstructionPointer != NO_CHANGE)
        ? lastInstructionPointer
        : super.nextPointer(old);
  }

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    lastInstructionPointer = (parameters[1].withMode(memory, relativeBase) == 0)
        ? parameters[2].withMode(memory, relativeBase)
        : NO_CHANGE;
    return super.apply(memory, relativeBase);
  }
}

class LessThan extends Instruction {
  LessThan(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    memory[parameters[3].withMode(memory, relativeBase, true)] =
        parameters[1].withMode(memory, relativeBase) <
                parameters[2].withMode(memory, relativeBase)
            ? 1
            : 0;
    return memory;
  }
}

class Equals extends Instruction {
  Equals(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    memory[parameters[3].withMode(memory, relativeBase, true)] =
        parameters[1].withMode(memory, relativeBase) ==
                parameters[2].withMode(memory, relativeBase)
            ? 1
            : 0;
    return memory;
  }
}

class RelativeBase extends Instruction {
  RelativeBase(instruction) : super(instruction);

  @override
  Object apply(Map<int, int> memory, relativeBase) {
    return relativeBase + parameters[1].withMode(memory, relativeBase);
  }
}

class Halt extends Instruction {
  Halt(instruction) : super(instruction);
}

class Computer {
  Map<int, int> memory = {};
  bool halted = false;
  bool firstRun = true;
  var instructionPointer = 0;
  int output;
  int relativeBase = 0;

  Computer(List<int> data) {
    data.asMap().forEach((k, v) => memory[k] = v);
  }

  List getInstructionParams(opcodeId) => memory.values
      .toList()
      .getRange(instructionPointer,
          instructionPointer + Opcode.opcodeMap[opcodeId].length)
      .toList();

  void run([List<int> input, exitOnOuput = false]) {
    var opcodeId;
    List<int> params;
    while (true) {
      opcodeId = Opcode.opcodeId(memory[instructionPointer]);
      if (opcodeId == Opcode.HALT) {
        halted = true;
        break;
      }
      params = getInstructionParams(opcodeId);
      var instruction = Instruction.create(opcodeId, params);

      if (opcodeId == Opcode.WRITE) {
        (instruction as Write).input = firstRun ? input[0] : input[1];
        if (firstRun) firstRun = false;
      }

      var result = instruction.apply(memory, relativeBase);
      instructionPointer = instruction.nextPointer(instructionPointer);

      if (opcodeId == Opcode.RELATIVE_BASE) {
        relativeBase = result;
      }

      if (opcodeId == Opcode.OUTPUT) {
        output = result;
        print('output: $output');
        if (exitOnOuput) break;
      }
    }
  }
}
