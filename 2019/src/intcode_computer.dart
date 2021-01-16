import '../../shared/dart/src/utils.dart';
// import 'package:trotter/trotter.dart';

enum Mode { position, immediate }

abstract class Instruction {
  static const OPCODE_ADD = 1;
  static const OPCODE_MULTIPY = 2;
  static const OPCODE_WRITE = 3;
  static const OPCODE_OUTPUT = 4;
  static const OPCODE_HALT = 99;
  static const MAX_LENGTH = 4;

  static final increment = {}
    ..[OPCODE_ADD] = 4
    ..[OPCODE_MULTIPY] = 4
    ..[OPCODE_WRITE] = 2
    ..[OPCODE_OUTPUT] = 2
    ..[OPCODE_HALT] = 1;

  static final modes = {}
    ..[0] = Mode.position
    ..[1] = Mode.immediate;

  List<int> param;
  int param1, param2, param3;
  Mode param1Mode, param2Mode, param3Mode;

  @override
  String toString() {
    return 'param: $param\nparam1: $param1 ($param1Mode), param2: $param2 ($param2Mode),param3: $param3 ($param3Mode)';
  }

  List<int> apply(List<int> memory);

  int get length;

  Instruction(this.param) {
    parseOpData(param[0]);
    param1 = param[1];
    param2 = param[2];
    param3 = param[3];
  }

  //param of form ABCDE where
  //DE = op code, C = mode of param1, B = mode of param2, A = mode of param3
  void parseOpData(int opdata) {
    var opdataStr = opdata.toString().padLeft(5, '0');
    param1Mode = Instruction.modes[opdataStr[2].toInt()];
    param2Mode = Instruction.modes[opdataStr[1].toInt()];
    param3Mode = Instruction.modes[opdataStr[0].toInt()];
  }

  static int parseCode(int opcode) {
    var s = opcode.toString();
    return s.length < 3 ? s.toInt() : s.substring(s.length - 2).toInt();
  }

  factory Instruction.fromOpCode(int code, params) {
    var opcode = parseCode(code);
    switch (opcode) {
      case OPCODE_ADD:
        return Add(params);
        break;
      case OPCODE_MULTIPY:
        return Multiply(params);
        break;
      case OPCODE_WRITE:
        return Write(params);
        break;
      case OPCODE_OUTPUT:
        return Output(params);
        break;
      case OPCODE_HALT:
        return Halt(params);
        break;
      default:
        throw 'Unknown opcode: $opcode';
    }
  }
  int readValue(param, mode, memory) {
    switch (mode) {
      case Mode.position:
        return memory[param];
        break;
      case Mode.immediate:
        return param;
        break;
      default:
        throw 'Invalid mode $mode';
    }
  }
}

class Add extends Instruction {
  Add(param) : super(param);

  @override
  int get length => Instruction.increment[Instruction.OPCODE_ADD];

  @override
  List<int> apply(List<int> memory) {
    var operand1 = readValue(param1, param1Mode, memory);
    var operand2 = readValue(param2, param2Mode, memory);
    var storeAddress = param3; //readValue(param3, param3Mode, memory);
    // print('Add: $operand1 and $operand2. Store at: $storeAddress');
    memory[storeAddress] = operand1 + operand2;
    return memory;
  }
}

class Multiply extends Instruction {
  Multiply(param) : super(param);
  @override
  int get length => Instruction.increment[Instruction.OPCODE_MULTIPY];

  @override
  List<int> apply(List<int> memory) {
    var operand1 = readValue(param1, param1Mode, memory);
    var operand2 = readValue(param2, param2Mode, memory);
    var storeAddress = param3; //readValue(param3, param3Mode, memory);
    // print('Multiply: $operand1 and $operand2. Store at: $storeAddress');
    memory[storeAddress] = operand1 * operand2;
    return memory;
  }
}

class Write extends Instruction {
  Write(param) : super(param); //todo
  @override
  int get length => Instruction.increment[Instruction.OPCODE_WRITE];

  @override
  List<int> apply(List<int> memory) {
    var storeAddress = param1; //readValue(param1, param1Mode, memory);
    // print('Write: $param2. Store at: $storeAddress');
    memory[storeAddress] = param2;
    return memory;
  }
}

class Output extends Instruction {
  Output(param) : super(param);
  @override
  int get length => Instruction.increment[Instruction.OPCODE_OUTPUT];

  @override
  List<int> apply(List<int> memory) {
    var storeAddress = param1; //readValue(param1, param1Mode, memory);
    // print('Output: $param2. Store at: $storeAddress');
    print(memory[storeAddress]);
    return memory;
  }
}

class Halt extends Instruction {
  Halt(param) : super(param);
  @override
  int get length => Instruction.increment[Instruction.OPCODE_HALT];

  @override
  List<int> apply(List<int> memory) {
    //do nothing
    return memory;
  }
}

class Computer {
  List<int> memory;
  Computer(data) {
    memory = List.from(data);
  }

  int run(returnAddress) {
    var pc = 0; //program counter
    var opcode = 0;
    while (true) {
      opcode = memory[pc];
      if (opcode == Instruction.OPCODE_HALT) break;

      var params = memory.getRange(pc, pc + Instruction.MAX_LENGTH).toList();
      if (opcode == Instruction.OPCODE_WRITE) params[2] = 1;
      var instruction = Instruction.fromOpCode(opcode, params);
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
