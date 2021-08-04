import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/23

const bool DEBUG = false;
const DELIM = ',';

class NetworkedComputers {
  final int EMPTY_INPUT = -1;

  final program;
  late final inputProviders = <int, List<int>>{};
  late final computers = <int, Computer>{};

  NetworkedComputers(this.program, computerCount) {
    // var natInput = <int>[];
    // nat = Computer(
    //     program,
    //     () => natInput.isNotEmpty ? nat.removeAt(0) : EMPTY_INPUT,
    //     (i) => i == EMPTY_INPUT);

    for (var i in range(0, computerCount)) {
      inputProviders[i] = <int>[];
      inputProviders[i]!.add(i);
      computers[i] = Computer(
          program,
          () => inputProviders[i]!.isNotEmpty
              ? inputProviders[i]!.removeAt(0)
              : EMPTY_INPUT,
          (i) => i == EMPTY_INPUT);
    }
  }
  //Return ids of computer with input available
  //not used
  // List<Computer> active() {
  //   return inputProviders.entries
  //       .where((e) => e.value.isNotEmpty)
  //       .map((ev) => computers[ev.key]!)
  //       .toList();
  // }

  bool allIdle() {
    return inputProviders.values.every((e) => e.isEmpty);
  }

  int run1(final int targetAddress) {
    while (true) {
      for (var c in computers.values) {
        c.run([], true);
        var output = c.output();
        if (output.length == 3) {
          // print(output);
          c.output(true); //clear output
          var dest = output[0];
          var x = output[1];
          var y = output[2];
          if (dest == targetAddress) {
            return y;
          }
          inputProviders[dest]!.add(x);
          inputProviders[dest]!.add(y);
        }
      }
    }
  }

  int run2(final int targetAddress) {
    var nat_packet = <int>[];
    var prev_nat_y;

    while (true) {
      var outputPending = false;

      for (var c in computers.values) {
        c.run([], true);
        var output = c.output();
        if (output.length.isBetween(1, 2)) {
          outputPending = true;
        }
        if (output.length == 3) {
          outputPending = false;
          c.output(true); //clear output
          var dest = output[0];
          var x = output[1];
          var y = output[2];
          if (dest == targetAddress) {
            nat_packet = [x, y];
            // print(nat_packet);
          } else {
            inputProviders[dest]!.add(x);
            inputProviders[dest]!.add(y);
          }
        }
      }
      if (nat_packet.isNotEmpty && !outputPending && allIdle()) {
        // print('sending $nat_packet');
        if (prev_nat_y == nat_packet[1]) return prev_nat_y;
        prev_nat_y = nat_packet[1];
        inputProviders[0]!.addAll(nat_packet);
      }
    }
  }
}

Object part1(String header, NetworkedComputers nc) {
  printHeader(header);
  return nc.run1(255);
}

Object part2(String header, NetworkedComputers nc) {
  printHeader(header);
  return nc.run2(255);
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asInt('../data/day23.txt', DELIM);

  printAndAssert(part1('23 part 1', NetworkedComputers(mainInput, 50)), 17849);
  printAndAssert(part2('23 part 2', NetworkedComputers(mainInput, 50)), 12235);
}
