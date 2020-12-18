import 'dart:io';
import 'dart:math';
import 'dart:mirrors';

import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

class Calculator {
  Calculator();

  static RegExp regex =
      RegExp(r'^(?<min>\d+)-(?<max>\d+) (?<char>.): (?<password>.+)$');
  static RegExp REGEX_NUMBER = RegExp(r'^(?<number>\d+)');

  bool isNumber(c) => int.tryParse(c) != null;

  static String SPACE = ' ';
  static String BRACKET_OPENING = '(';
  static String BRACKET_CLOSING = ')';
  static String OPERATOR_ADD = '+';
  static String OPERATOR_MULTIPLY = '*';
  static Set OPERATOR = <String>{OPERATOR_ADD, OPERATOR_MULTIPLY};

  bool isOperator(c) => OPERATOR.contains(c);

  int getNumber(s) =>
      int.parse(REGEX_NUMBER.firstMatch(s).namedGroup('number'));

  String getSubexpression(String s) {
    var level = 0;
    var startIndex = -1;

    for (var i = 0; i < s.length; i++) {
      // print(s[i]);
      if (s[i] == BRACKET_OPENING) {
        if (startIndex < 0) startIndex = i;
        level++;
      } else if (s[i] == BRACKET_CLOSING) {
        level--;
      }
      if (level == 0) return s.substring(startIndex + 1, i);
    }
    throw 'Unbalanced subexpression';
  }

  int applyOperator(lhs, rhs, op) {
    // print('applyOperator: $lhs $op $rhs');
    if (op == OPERATOR_ADD) {
      return lhs + rhs;
    } else if (op == OPERATOR_MULTIPLY) {
      return lhs * rhs;
    } else {
      throw 'Invalid operator: $op';
    }
  }

  int evaluate(expression) {
    var lastOperator = null;
    var rhsNumber;
    var result = 0;
    var i = 0;

    void updateResult() {
      if (lastOperator == null) {
        result = rhsNumber;
      } else {
        result = applyOperator(result, rhsNumber, lastOperator);
        // print('result=$result');
        lastOperator = null;
      }
    }

    while (i < expression.length) {
      var ch = expression[i];
      if (ch == SPACE) {
        i++;
      } else if (isNumber(ch)) {
        rhsNumber = getNumber(expression.substring(i));
        updateResult();
        i += rhsNumber.toString().length;
      } else if (isOperator(ch)) {
        lastOperator = ch;
        i += ch.length;
      } else if (ch == BRACKET_OPENING) {
        var subexpression = getSubexpression(expression.substring(i));
        // print('subexp = $subexpression');
        rhsNumber = evaluate(subexpression);
        updateResult();
        i += subexpression.length + 2;
      }
    }
    return result;
  }
}

void runPart1(String name, List input) {
  printHeader(name);
  var calculator = Calculator();
  var total = 0;
  input.forEach((expression) {
    print('=====================');
    print('$expression');
    var result = calculator.evaluate(expression);
    print('Answer = $result');
    total += result;
  });
  print(total);
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day18-test.txt');
  MAIN_INPUT = fileAsString('../data/day18.txt');

  //Answers: total = 26406
  // 1 + 2 * 3 + 4 * 5 + 6 = 71
  // 2 * 3 + (4 * 5) = 26
  // 5 + (8 * 3 + 9 + 3 * 4 * 3) = 437
  // 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) = 12240
  // ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 = 13632
  runPart1('18 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('18 test part 2', TEST_INPUT);

  //Answer: 98621258158412
  runPart1('18 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('18 part 2', MAIN_INPUT);
}
