import 'dart:io';
import '../utils.dart';

var verbose = false;
var debug = false;

typedef bool IsValidPasswordFn(PasswordEntry pe);

//find passwords that have a char in one of two positions (but not both)
void day2b() {
  //True if letter at pos1 or pos2 but not both) is char (^ = XOR)
  bool isValidPassord(PasswordEntry pe) =>
      ((pe.password[pe.minAppearances - 1] == pe.requiredChar) ^
          (pe.password[pe.maxAppearances - 1] == pe.requiredChar));

  printDay('2b');
  day2(isValidPassord);
}

//find passwords that have between min and max occurences of a char in password
void day2a() {
  //
  bool isValidPassord(PasswordEntry pe) {
    var occurencesCount = pe.requiredChar.allMatches(pe.password).length;
    return (occurencesCount >= pe.minAppearances &&
        occurencesCount <= pe.maxAppearances);
  }

  printDay('2a');
  day2(isValidPassord);
}

class PasswordEntry {
  int minAppearances;
  int maxAppearances;
  String requiredChar;
  String password;
  PasswordEntry(this.minAppearances, this.maxAppearances, this.requiredChar,
      this.password);

  @override
  String toString() =>
      '$minAppearances, $maxAppearances, $requiredChar, $password';
}

void day2(IsValidPasswordFn isValidPassword) {
  //regex to parse "<min>-<max> char: password" eg:
  //   9-12 q: qqqxhnhdmqqqqjz
  var test = '9-12 q: qqqxhnhdmqqqqjz';
  var re = RegExp(
      r'^(?<min>\d{1,2})-(?<max>\d{1,2}) (?<char>.): (?<password>.*)$',
      caseSensitive: true,
      multiLine: false);

  PasswordEntry getValues(RegExpMatch match) => PasswordEntry(
      int.parse(match.namedGroup('min')),
      int.parse(match.namedGroup('max')),
      match.namedGroup('char').toString(),
      match.namedGroup('password'));

  if (debug) {
    print('Test output');
    print(re.hasMatch(test));
    print(re.stringMatch(test));
    var match = re.firstMatch(test);

    var values = getValues(match);
    print('Password entry: $values');
  }

  var lines = File('./2020/data/day2a.txt').readAsLinesSync();

  var validPasswordsCount = 0;

  for (var s in lines) {
    var values = getValues(re.firstMatch(s));
    if (verbose) print('$s = $values');
    try {
      if (isValidPassword(values)) {
        // var occurencesCount = char.toString().allMatches(password).length;
        // if (occurencesCount >= min && occurencesCount <= max) {
        validPasswordsCount++;
        if (verbose) ('   valid password');
      } else {
        if (verbose) ('   INVALID password');
      }
    } catch (e) {
      print('**** ERROR: $values error: $e');
    }
  }
  print('Total valid passwords: $validPasswordsCount');
}
