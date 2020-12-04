import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

const int MAX_FIELDS = 8;
const int MIN_FIELDS = 7;

final List<String> TEST_INPUT =
    File('./2020/data/day04-test.txt').readAsLinesSync();
final List<String> MAIN_INPUT = File('./2020/data/day04.txt').readAsLinesSync();

typedef bool IsValidPassportFn(Map<String, String> p);

bool isValidPassportPart1(Map<String, String> passport) =>
    (passport.length == MAX_FIELDS) ||
    ((passport.length == MIN_FIELDS && !passport.containsKey('cid')));

bool isValidPassportPart2(Map<String, String> passport) {
  if (!isValidPassportPart1(passport)) return false;
}

void test4a() {
  printHeader('4a test');
  var passportList = parseInput(TEST_INPUT);
  print(passportList);
  //Answer: 2
  print(
      'valid passports: ${passportValidCount(passportList, isValidPassportPart1)}');
}

void test4b() {
  printHeader('4b test');
}

void day4a() {
  printHeader('4a');
  var passportList = parseInput(MAIN_INPUT);
  // print(passportList);
  //Answer: 239
  print(
      'valid passports: ${passportValidCount(passportList, isValidPassportPart1)}');
}

void day4b() {
  printHeader('4b');
}

int passportValidCount(
    List<Map<String, String>> passports, IsValidPassportFn isValidPassport) {
  var result = 0;
  for (var passport in passports) {
    if (DEBUG) print(passport);
    if (isValidPassport(passport)) {
      result++;
      if (DEBUG) print('*** valid');
    } else {
      if (DEBUG) print('*** INVALID');
    }
  }
  return result;
}

List<Map<String, String>> parseInput(final List<String> input) {
  var result = <Map<String, String>>[];
  var passportDataMap = <String, String>{};
  result.add(passportDataMap);

  for (var row in input) {
    var passportData = row.trim();
    if ('' != passportData) {
      var keyValueList = passportData.split(' ');
      for (var kv in keyValueList) {
        var kvSplit = kv.split(':');
        passportDataMap[kvSplit[0]] = kvSplit[1];
      }
    } else {
      passportDataMap = <String, String>{};
      result.add(passportDataMap);
    }
  }

  return result;
}
