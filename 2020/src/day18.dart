import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

class Calculator {
  final Stack stack = Stack();

  Calculator();

  static RegExp REGEX_NUMBER = RegExp(r'^(?<number>\d+)');

  static const String SPACE = ' ';
  static const String BRACKET_OPENING = '(';
  static const String BRACKET_CLOSING = ')';
  static const String OPERATOR_ADD = '+';
  static const String OPERATOR_MULTIPLY = '*';
  static const Set OPERATOR = <String>{OPERATOR_ADD, OPERATOR_MULTIPLY};

  bool isOperator(c) => OPERATOR.contains(c);
  bool isNumber(c) => int.tryParse(c) != null;

  int getNumber(s) =>
      int.parse(REGEX_NUMBER.firstMatch(s)!.namedGroup('number')!);

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

  //return true if a has greater precedence that b
  bool greaterPrecedence(a, b) =>
      b == BRACKET_OPENING || a == OPERATOR_ADD && b == OPERATOR_MULTIPLY;

  int evaluate2(expression) {
    var digit;
    var i = 0;
    var postfix = [];
    var operatorStack = Stack();

    while (i < expression.length) {
      var ch = expression[i];
      if (ch == SPACE) {
        i++;
      } else if (isNumber(ch)) {
        digit = getNumber(expression.substring(i));
        postfix.add(digit);
        i += digit.toString().length;
      } else if (isOperator(ch)) {
        if (operatorStack.isEmpty ||
            greaterPrecedence(ch, operatorStack.peek())) {
          operatorStack.push(ch);
        } else {
          postfix.add(operatorStack.pop());
          operatorStack.push(ch);
        }
        i += ch.length as int;
      } else if (ch == BRACKET_OPENING) {
        operatorStack.push(ch);
        i += ch.length as int;
      } else if (ch == BRACKET_CLOSING) {
        while (true) {
          var opCh = operatorStack.pop();
          if (opCh == BRACKET_OPENING) break;
          postfix.add(opCh);
        }
        i += ch.length as int;
      }
    }
    while (operatorStack.isNotEmpty) {
      postfix.add(operatorStack.pop());
    }
    // print(postfix);
    return evaluatePostfix(postfix);
  }

  int evaluate(expression) {
    var lastOperator;
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
        i += ch.length as int;
      } else if (ch == BRACKET_OPENING) {
        var subexpression = getSubexpression(expression.substring(i));
        // print('subexp = $subexpression');
        rhsNumber = Calculator().evaluate(subexpression);
        updateResult();
        i += subexpression.length + 2;
      }
    }
    return result;
  }

  int evaluatePostfix(List postfix) {
    var stack = Stack<int>();

    for (var ch in postfix) {
      if (ch is int) {
        stack.push(ch);
      } else {
        var val1 = stack.pop();
        var val2 = stack.pop();

        if (ch == OPERATOR_ADD) {
          stack.push(val1 + val2);
        } else if (ch == OPERATOR_MULTIPLY) {
          stack.push(val1 * val2);
        } else {
          throw 'Invalid operator in postfix expression';
        }
      }
    }
    return stack.pop();
  }
}

void runPart1(String name, List input) {
  printHeader(name);
  var calculator = Calculator();
  var total = 0;
  input.forEach((expression) {
    // print('=====================');
    // print('$expression');
    var result = calculator.evaluate(expression);
    // print('Answer = $result');
    total += result;
  });
  print(total);
}

void runPart2(String name, List input) {
  printHeader(name);
  var calculator = Calculator();
  var total = 0;
  input.forEach((expression) {
    // print('=====================');
    // print('$expression');
    var result = calculator.evaluate2(expression);
    // print('Answer = $result');
    total += result;
  });
  print(total);
}

void main(List<String> arguments) {
  var TEST_INPUT = FileUtils.asLines('../data/day18-test.txt');
  var MAIN_INPUT = FileUtils.asLines('../data/day18.txt');

  //Answers: total = 26406
  // 1 + 2 * 3 + 4 * 5 + 6 = 71
  // 2 * 3 + (4 * 5) = 26
  // 5 + (8 * 3 + 9 + 3 * 4 * 3) = 437
  // 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) = 12240
  // ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 = 13632
  runPart1('18 test part 1', TEST_INPUT);

  // 1 + 2 * 3 + 4 * 5 + 6 = 231
  // 2 * 3 + (4 * 5) = 46
  // 5 + (8 * 3 + 9 + 3 * 4 * 3) = 1445
  // 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) = 669060
  // ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 = 23340
  runPart2('18 test part 2', TEST_INPUT);

  //Answer: 98621258158412
  runPart1('18 part 1', MAIN_INPUT);

  //Answer: 241216538527890
  runPart2('18 part 2', MAIN_INPUT);
}
