import '../../shared/dart/src/utils.dart';
// import 'package:trotter/trotter.dart';

enum ParameterMode { position, immediate, relative }

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
  final Instruction Function(List<int>, Map<int, int>, int relativeBase) create;
  final length; //no of params in instruction
  Opcode(this.id, this.create, this.length);

  //code is of form ABCDE where DE = op code id.
  //Return opcode id, extracted from param1 described in parseModes().
  static int opcodeId(int code) {
    var s = code.toString().padLeft(5, '0');
    return s.substring(s.length - 2).toInt();
  }

  static final Map<int, Opcode> opcodeMap = {}
    ..[ADD] = Opcode(Opcode.ADD, (a, b, c) => Add(a, b, c), 4)
    ..[MULTIPY] = Opcode(Opcode.MULTIPY, (a, b, c) => Multiply(a, b, c), 4)
    ..[WRITE] = Opcode(Opcode.WRITE, (a, b, c) => Write(a, b, c), 2)
    ..[OUTPUT] = Opcode(Opcode.OUTPUT, (a, b, c) => Output(a, b, c), 2)
    ..[JMP_TRUE] = Opcode(Opcode.JMP_TRUE, (a, b, c) => JumpIfTrue(a, b, c), 3)
    ..[JMP_FALSE] =
        Opcode(Opcode.JMP_FALSE, (a, b, c) => JumpIfFalse(a, b, c), 3)
    ..[LESS_THAN] = Opcode(Opcode.LESS_THAN, (a, b, c) => LessThan(a, b, c), 4)
    ..[EQUALS] = Opcode(Opcode.EQUALS, (a, b, c) => Equals(a, b, c), 4)
    ..[RELATIVE_BASE] =
        Opcode(Opcode.RELATIVE_BASE, (a, b, c) => RelativeBase(a, b, c), 2)
    ..[HALT] = Opcode(Opcode.HALT, (a, b, c) => Halt(a, b, c), 1);
}

abstract class Instruction {
  static final NO_RESULT = -1;

  static final modeMap = {}
    ..[0] = ParameterMode.position
    ..[1] = ParameterMode.immediate
    ..[2] = ParameterMode.relative;

  //instruction consists of code, param1, param2 [,param3]
  //code is of form ABCDE where
  //DE = opcode id, C = mode of param1, B = mode of param2, A = mode of param3
  List<int> _instruction;
  late Opcode opcode;
  final Map<int, Parameter> parameters = {};
  final Map<int, int?> _memory;
  final int _relativeBase;
  @override
  String toString() => 'param: $_instruction\nparams: $parameters';
  Object apply() => NO_RESULT;
  int get length => opcode.length;

  int nextPointer(current) => current + opcode.length;

  Instruction(this._instruction, this._memory, this._relativeBase) {
    opcode = Opcode.opcodeMap[Opcode.opcodeId(_instruction[0])]!;
    var modes = _parseModes(_instruction[0]);
    for (var i in range(1, opcode.length)) {
      parameters[i] =
          Parameter(_instruction[i], modes[i], _memory, _relativeBase);
    }
  }

  Map _parseModes(int code) {
    var s = code.toString().padLeft(5, '0');
    return {
      1: Instruction.modeMap[s[2].toInt()],
      2: Instruction.modeMap[s[1].toInt()],
      3: Instruction.modeMap[s[0].toInt()]
    };
  }

  //Return a specific Instruction object eg Add, Multiply, Halt, etc,
  factory Instruction.create(int code, List<int> instruction,
          Map<int, int> memory, int relativeBase) =>
      Opcode.opcodeMap[Opcode.opcodeId(code)]!
          .create(instruction, memory, relativeBase);
}

class Parameter {
  final int _value;
  final ParameterMode _mode;
  final _memory;
  final _relativeBase;
  Parameter(this._value, this._mode, this._memory, this._relativeBase);

  //The number returned depends on the mode and whether the caller
  //is going to use the returned value for writing to (=>asAddress) or
  //reading from (=>asValue) memory.
  int get asAddress =>
      _value + (_mode == ParameterMode.relative ? _relativeBase : 0) as int;

  int get asValue {
    switch (_mode) {
      case ParameterMode.position:
        return _memory[_value] ?? 0;
      case ParameterMode.immediate:
        return _value;
      case ParameterMode.relative:
        return _memory[_relativeBase + _value] ?? 0;
      default:
        throw 'Invalid mode $_mode';
    }
  }

  @override
  String toString() => 'value: $_value, mode: $_mode, relbase: $_relativeBase';
}

class Add extends Instruction {
  Add(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    _memory[parameters[3]!.asAddress] =
        parameters[1]!.asValue + parameters[2]!.asValue;
    return _memory;
  }
}

class Multiply extends Instruction {
  Multiply(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    _memory[parameters[3]!.asAddress] =
        parameters[1]!.asValue * parameters[2]!.asValue;
    return _memory;
  }
}

class Write extends Instruction {
  late int input;
  Write(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    _memory[parameters[1]!.asAddress] = input;
    return _memory;
  }
}

class Output extends Instruction {
  Output(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    return parameters[1]!.asValue;
  }
}

class JumpIfTrue extends Instruction {
  static const NO_CHANGE = -1;
  late int lastInstructionPointer;

  JumpIfTrue(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  int nextPointer(current) {
    return (lastInstructionPointer != NO_CHANGE)
        ? lastInstructionPointer
        : super.nextPointer(current);
  }

  @override
  Object apply() {
    lastInstructionPointer =
        (parameters[1]!.asValue != 0) ? parameters[2]!.asValue : NO_CHANGE;
    return super.apply();
  }
}

class JumpIfFalse extends Instruction {
  static const NO_CHANGE = -1;
  late int lastInstructionPointer;
  JumpIfFalse(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  int nextPointer(current) {
    return (lastInstructionPointer != NO_CHANGE)
        ? lastInstructionPointer
        : super.nextPointer(current);
  }

  @override
  Object apply() {
    lastInstructionPointer =
        (parameters[1]!.asValue == 0) ? parameters[2]!.asValue : NO_CHANGE;
    return super.apply();
  }
}

class LessThan extends Instruction {
  LessThan(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    _memory[parameters[3]!.asAddress] =
        parameters[1]!.asValue < parameters[2]!.asValue ? 1 : 0;
    return _memory;
  }
}

class Equals extends Instruction {
  Equals(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    _memory[parameters[3]!.asAddress] =
        parameters[1]!.asValue == parameters[2]!.asValue ? 1 : 0;
    return _memory;
  }
}

class RelativeBase extends Instruction {
  RelativeBase(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);

  @override
  Object apply() {
    return _relativeBase + parameters[1]!.asValue;
  }
}

class Halt extends Instruction {
  Halt(instruction, memory, relativeBase)
      : super(instruction, memory, relativeBase);
}

class ComputerState {
  final memory, instructionPointer, relativeBase;
  ComputerState(this.memory, this.instructionPointer, this.relativeBase);
}

class Computer {
  Map<int, int> memory = {};
  bool halted = false;
  bool _firstRun = true;
  var _instructionPointer = 0;
  final List<int> _output = [];
  int _relativeBase = 0;
  int Function()? _inputProvider;
  bool Function(int)? _forceExit;

  bool requiresInput = false;
  int? input;

  Computer(List<int> program,
      [int Function()? inputProvider, bool Function(int)? forceExit]) {
    program.asMap().forEach((k, v) => memory[k] = v);
    _inputProvider = inputProvider;
    _forceExit = forceExit;
  }

  ComputerState get state =>
      ComputerState(Map.from(memory), _instructionPointer, _relativeBase);

  set state(ComputerState state) {
    memory = Map.from(state.memory);
    _instructionPointer = state.instructionPointer;
    _relativeBase = state.relativeBase;
  }

  List<int> output([clearOnRead = false]) {
    var result = List<int>.from(_output);

    if (clearOnRead) _output.clear();
    return result;
  }

  List<int> getInstructionParams(opcodeId) => memory.values
      .toList()
      .getRange(_instructionPointer,
          _instructionPointer + Opcode.opcodeMap[opcodeId]!.length as int)
      .toList();

  List run([List<int>? program, exitOnOuput = false, exitCheck]) {
    int readInput() {
      if (input != null) {
        return input!;
      } else if (_inputProvider == null) {
        return _firstRun ? program![0] : program![1];
      } else {
        return _inputProvider!();
      }
    }

    var opcodeId;
    List<int> params;
    requiresInput = false;
    var lastInput = -1;
    while (true) {
      opcodeId = Opcode.opcodeId(memory[_instructionPointer]!);
      if (opcodeId == Opcode.HALT) {
        halted = true;
        break;
      }
      params = getInstructionParams(opcodeId);
      // print('$opcodeId, $params');
      var instruction =
          Instruction.create(opcodeId, params, memory, _relativeBase);

      if (opcodeId == Opcode.WRITE) {
        // var input = readInput();
        var input = readInput();
        lastInput = input;
        // print('input = $input');
        (instruction as Write).input = input;
        // (instruction as Write).input = readInput();
        // print((instruction as Write).input);
        // print('input ${(instruction as Write).input}');
        if (_firstRun) _firstRun = false;
      }

      var result = instruction.apply();
      _instructionPointer = instruction.nextPointer(_instructionPointer);

      if (opcodeId == Opcode.RELATIVE_BASE) {
        _relativeBase = result as int;
      }

      if (opcodeId == Opcode.OUTPUT) {
        _output.add(result as int);
        // print('output: $_output');
        if (exitOnOuput) break;
      }
      if (_forceExit != null && _forceExit!(lastInput)) break;
    }
    return output();
  }
}
