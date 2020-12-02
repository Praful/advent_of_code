import 'dart:io';
import '../utils.dart';

var verbose = false;
var debug = false;

typedef bool IsValidPasswordFn(PasswordEntry pe);

//find passwords that have a char in one of two positions (but not both)
void day2b() {
  //True if letter at pos1 or pos2 but not both) is char (^ = XOR)
  bool isValidPassword(PasswordEntry pe) =>
      ((pe.password[pe.minAppearances - 1] == pe.requiredChar) ^
          (pe.password[pe.maxAppearances - 1] == pe.requiredChar));

  printHeader('2b');
  day2(isValidPassword);
}

//find passwords that have between min and max occurences of a char in password
void day2a() {
  //
  bool isValidPassword(PasswordEntry pe) {
    var occurencesCount = pe.requiredChar.allMatches(pe.password).length;
    return (occurencesCount >= pe.minAppearances &&
        occurencesCount <= pe.maxAppearances);
  }

  printHeader('2a');
  day2(isValidPassword);
}

class PasswordEntry {
  //regex to parse "<min>-<max> char: password" eg:
  //   9-12 q: qqqxhnhdmqqqqjz
  //in part 2, min and max represent the two character position in the password
  static RegExp regex = RegExp(
      r'^(?<min>\d{1,2})-(?<max>\d{1,2}) (?<char>.): (?<password>.*)$',
      caseSensitive: true,
      multiLine: false);

  int minAppearances;
  int maxAppearances;
  String requiredChar;
  String password;

  PasswordEntry(String s) {
    final match = PasswordEntry.regex.firstMatch(s);

    minAppearances = int.parse(match.namedGroup('min'));
    maxAppearances = int.parse(match.namedGroup('max'));
    requiredChar = match.namedGroup('char').toString();
    password = match.namedGroup('password');
  }

  @override
  String toString() =>
      '$minAppearances, $maxAppearances, $requiredChar, $password';
}

void day2(IsValidPasswordFn isValidPassword) {
  final lines = File('./2020/data/day02.txt').readAsLinesSync();

  var validPasswordsCount = 0;

  for (var s in lines) {
    final passwordDetails = PasswordEntry(s);
    if (verbose) print('$s = $passwordDetails');
    try {
      if (isValidPassword(passwordDetails)) {
        validPasswordsCount++;
        if (verbose) ('   valid password');
      } else {
        if (verbose) ('   INVALID password');
      }
    } catch (e) {
      print('**** ERROR: $passwordDetails error: $e');
    }
  }
  print('Total valid passwords: $validPasswordsCount');
}

void test1() {
  printHeader('2 test output');
  final test = '9-12 q: qqqxhnhdmqqqqjz';

  print(PasswordEntry.regex.hasMatch(test));
  print(PasswordEntry.regex.stringMatch(test));

  final passwordDetails = PasswordEntry(test);
  print('Password entry: $passwordDetails');
}
