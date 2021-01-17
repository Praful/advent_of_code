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
    ..[HALT] = Opcode(Opcode.HALT, (a) => Halt(a), 1);
}

abstract class Instruction {
  static const MAX_LENGTH = 4;

  static final modeMap = {}
    ..[0] = Mode.position
    ..[1] = Mode.immediate;

  //instruction consists of code, param1, param2 [,param3]
  //code is of form ABCDE where
  //DE = opcode id, C = mode of param1, B = mode of param2, A = mode of param3
  List<int> instruction;
  Opcode opcode;
  Map<int, Parameter> parameters = {};

  @override
  String toString() => 'param: $instruction\nparams: $parameters';
  List<int> apply(List<int> memory) => memory;
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
  int withMode(memory) {
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
    memory[parameters[3].value] =
        parameters[1].withMode(memory) + parameters[2].withMode(memory);
    return memory;
  }
}

class Multiply extends Instruction {
  Multiply(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    memory[parameters[3].value] =
        parameters[1].withMode(memory) * parameters[2].withMode(memory);
    return memory;
  }
}

class Write extends Instruction {
  int input;
  Write(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    memory[parameters[1].value] = input;
    return memory;
  }
}

class Output extends Instruction {
  Output(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    // print(memory[parameters[1].value]);
    return [memory[parameters[1].value]];
    // return memory;
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
  List<int> apply(List<int> memory) {
    lastInstructionPointer = (parameters[1].withMode(memory) != 0)
        ? parameters[2].withMode(memory)
        : NO_CHANGE;
    return super.apply(memory);
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
  List<int> apply(List<int> memory) {
    lastInstructionPointer = (parameters[1].withMode(memory) == 0)
        ? parameters[2].withMode(memory)
        : NO_CHANGE;
    return super.apply(memory);
  }
}

class LessThan extends Instruction {
  LessThan(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    memory[parameters[3].value] =
        parameters[1].withMode(memory) < parameters[2].withMode(memory) ? 1 : 0;
    return memory;
  }
}

class Equals extends Instruction {
  Equals(instruction) : super(instruction);

  @override
  List<int> apply(List<int> memory) {
    memory[parameters[3].value] =
        parameters[1].withMode(memory) == parameters[2].withMode(memory)
            ? 1
            : 0;
    return memory;
  }
}

class Halt extends Instruction {
  Halt(instruction) : super(instruction);
}

class Computer {
  List<int> memory;
  Computer(data) {
    memory = List.from(data);
  }

  List<int> run(int returnAddress, List<int> input) {
    var instructionPointer = 0;
    var output;
    var opcodeId = 0;
    List<int> params;
    while (true) {
      try {
        opcodeId = Opcode.opcodeId(memory[instructionPointer]);
        if (opcodeId == Opcode.HALT) break;
        params = memory
            .getRange(instructionPointer,
                instructionPointer + Opcode.opcodeMap[opcodeId].length)
            .toList();
        var instruction = Instruction.create(opcodeId, params);
        if (opcodeId == Opcode.WRITE) {
          (instruction as Write).input = input.first;
          input.removeAt(0);
        }
        var result = instruction.apply(memory);
        if (opcodeId == Opcode.OUTPUT) output = result;

        instructionPointer = instruction.nextPointer(instructionPointer);
      } catch (e, stacktrace) {
        print(
            'Error running program:\n instruction pointer: $instructionPointer, opcode: $opcodeId, params: $params\n\n$stacktrace');
        return null;
      }
    }
    return output ?? [memory[returnAddress]];
  }
}
