import 'dart:io';
import '../utils.dart';

//mapping lists and maps: https://bezkoder.com/dart-convert-list-map/

const bool DEBUG = true;

const int MAX_FIELDS = 8;
const int MIN_FIELDS = 7;

final List<String> TEST_INPUT =
    File('./2020/data/day04-test.txt').readAsLinesSync();
final List<String> TEST_INPUT_INVALID =
    File('./2020/data/day04-invalid-test.txt').readAsLinesSync();
final List<String> TEST_INPUT_VALID =
    File('./2020/data/day04-valid-test.txt').readAsLinesSync();

final List<String> MAIN_INPUT = File('./2020/data/day04.txt').readAsLinesSync();

typedef bool IsValidPassportFn(Map<String, String> p);

bool isValidPassportPart1(Map<String, String> passport) =>
    (passport.length == MAX_FIELDS) ||
    ((passport.length == MIN_FIELDS && !passport.containsKey('cid')));

bool isNumberInRange(String n, int min, int max) {
  var num = int.parse(n);
  return (num >= min && num <= max);
}

bool isValidHeight(String hgt, int cmMin, int cmMax, inMin, inMax) {
  if (hgt.contains('cm')) {
    return isNumberInRange(hgt.split('cm')[0], cmMin, cmMax);
  } else if (hgt.contains('in')) {
    return isNumberInRange(hgt.split('in')[0], inMin, inMax);
  } else {
    return false;
  }
}

final RegExp VALID_HAIR_COLOR_REGEX = RegExp(r'^#[0-9a-fA-F]{6}$');
final RegExp VALID_PASSPORT_PID_REGEX = RegExp(r'^\d{9}$');

const Set<String> VALID_EYE_COLORS = {
  'amb',
  'blu',
  'brn',
  'gry',
  'grn',
  'hzl',
  'oth'
};
bool isValidEyeColor(String ecl) => VALID_EYE_COLORS.contains(ecl);

bool hasMatch(String s, RegExp re) => re.hasMatch(s);

bool isValidPassportPart2(Map<String, String> passport) =>
    isValidPassportPart1(passport) &&
    isNumberInRange(passport['byr'], 1920, 2002) &&
    isNumberInRange(passport['iyr'], 2010, 2020) &&
    isNumberInRange(passport['eyr'], 2020, 2030) &&
    isValidHeight(passport['hgt'], 150, 193, 59, 76) &&
    hasMatch(passport['hcl'], VALID_HAIR_COLOR_REGEX) &&
    isValidEyeColor(passport['ecl']) &&
    hasMatch(passport['pid'], VALID_PASSPORT_PID_REGEX);

void test4a() {
  printHeader('4a test');
  var passportList = parseInput(TEST_INPUT);
  //Answer: 2
  print(
      'valid passports: ${passportValidCount(passportList, isValidPassportPart1)}');
}

void test4b() {
  printHeader('4b test');
  var passportListInvalid = parseInput(TEST_INPUT_INVALID);
  var passportListValid = parseInput(TEST_INPUT_VALID);

  //Answer: 0
  print(
      'valid passports invalid list: ${passportValidCount(passportListInvalid, isValidPassportPart2)}');

  //Answer: 4
  print(
      'valid passports in valid list: ${passportValidCount(passportListValid, isValidPassportPart2)}');
}

void day4a() {
  printHeader('4a');
  var passportList = parseInput(MAIN_INPUT);
  //Answer: 239
  print(
      'valid passports: ${passportValidCount(passportList, isValidPassportPart1)}');
}

void day4b() {
  printHeader('4b');
  var passportList = parseInput(MAIN_INPUT);
  //Answer: 188
  print(
      'valid passports: ${passportValidCount(passportList, isValidPassportPart2)}');
}

//functional version using fold (a generic version of reduce)
int passportValidCount(
    List<Map<String, String>> passports, IsValidPassportFn isValidPassport) {
  return passports.fold(
      0, (result, passport) => result + (isValidPassport(passport) ? 1 : 0));
}

//procedural
// int passportValidCount(
//     List<Map<String, String>> passports, IsValidPassportFn isValidPassport) {
//   var result = 0;
//   for (var passport in passports) {
//     if (DEBUG) print(passport);
//     if (isValidPassport(passport)) {
//       result++;
//       if (DEBUG) print('*** valid');
//     } else {
//       if (DEBUG) print('*** INVALID');
//     }
//   }
//   return result;
// }

List<Map<String, String>> parseInput(final List<String> input) {
  var result = <Map<String, String>>[];
  var passportDataMap = <String, String>{};
  result.add(passportDataMap);

  input.forEach((row) {
    var passportData = row.trim();
    if ('' != passportData) {
      passportData.split(' ').forEach((kvStr) {
        var kvList = kvStr.split(':');
        passportDataMap[kvList[0]] = kvList[1];
      });
    } else {
      passportDataMap = <String, String>{};
      result.add(passportDataMap);
    }
  });

  return result;
}
