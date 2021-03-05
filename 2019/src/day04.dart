import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

//Each digit must be greater than or equal to the preceding digit.
bool isDecreasing(String s) {
  for (var i in range(1, s.length)) {
    if (s[i].toInt() < s[i - 1].toInt()) return true;
  }
  return false;
}

bool hasSameTwoAdjacentDigits1(String s) {
  for (var i in range(1, s.length)) {
    if (s[i] == s[i - 1]) return true;
  }
  return false;
}

bool hasThreeTheSame(String s, String char) => s.contains('$char$char$char');

bool hasSameTwoAdjacentDigits2(String s) {
  for (var i in range(1, s.length)) {
    if (s[i] == s[i - 1] && !hasThreeTheSame(s, s[i])) {
      return true;
    }
  }
  return false;
}

bool isPasswordValid1(String password, lower, upper) {
  if (password.length != 6) return false;
  if (!password.toInt().isBetween(lower, upper)) return false;
  if (isDecreasing(password)) return false;
  if (!hasSameTwoAdjacentDigits1(password)) return false;
  return true;
}

bool isPasswordValid2(String password, lower, upper) {
  if (password.length != 6) return false;
  if (!password.toInt().isBetween(lower, upper)) return false;
  if (isDecreasing(password)) return false;
  if (!hasSameTwoAdjacentDigits2(password)) return false;
  return true;
}

int validPasswordCount(bool Function(String, int, int) isValid, lower, upper) =>
    range(lower, upper + 1)
        .where((i) => isValid(i.toString(), lower, upper))
        .length;

Object part1(String header, lower, upper) {
  printHeader(header);
  return validPasswordCount(isPasswordValid1, lower, upper);
}

Object part2(String header, lower, upper) {
  printHeader(header);
  return validPasswordCount(isPasswordValid2, lower, upper);
}

void main(List<String> arguments) {
  assertEqual(hasSameTwoAdjacentDigits1('111111'), true);
  assertEqual(isDecreasing('111111'), false);

  assertEqual(isPasswordValid1('122345', 0, 999999), true);
  assertEqual(isPasswordValid1('111123', 0, 999999), true);
  assertEqual(isPasswordValid1('135679', 0, 999999), false);
  assertEqual(isPasswordValid1('111111', 0, 999999), true);
  assertEqual(isPasswordValid1('223450', 0, 999999), false);
  assertEqual(isPasswordValid1('123789', 0, 999999), false);

  assertEqual(isPasswordValid2('112233', 0, 999999), true);
  assertEqual(isPasswordValid2('123444', 0, 999999), false);
  assertEqual(isPasswordValid2('111122', 0, 999999), true);

  //Answer:
  printAndAssert(part1('04 part 1', 248345, 746315),1019);
  printAndAssert(part2('04 part 2', 248345, 746315),660);

  //Answer:
  // print(part2('04 part 2', mainInput));
}
