import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/14

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

//round numToRound to nearest multiple that is >= multipleOf
//eg (8,3)-> 9, (2,3) -> 3
int roundUp(int numToRound, int multipleOf) {
  return ((numToRound + multipleOf - 1) ~/ multipleOf) * multipleOf;
}

class Recipe {
  final List<Ingredient> ingredients;
  final int minAmount;
  final String chemical;
  Recipe(this.chemical, this.minAmount, this.ingredients);

  @override
  String toString() => '$ingredients => $minAmount $chemical';
}

class Ingredient {
  final amount;
  final chemical;
  Ingredient(this.amount, this.chemical);
  @override
  String toString() => '$amount $chemical';
}

class NanoFactory {
  final _input;
  final _recipes = <String, Recipe>{};
  final _extra = <String, int>{};

  NanoFactory(this._input) {
    parse(_input);
  }

  //Example line:  12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
  Map parse(List<String> input) {
    input.forEach((l) {
      var equation = l.split('=>');
      var lhs = equation[0].trim().split(', ');
      var rhs = equation[1].trim().split(' ');
      _recipes[rhs[1]] = Recipe(
          rhs[1],
          rhs[0].toInt(),
          lhs.map((e) {
            var ingredient = e.split(' ');
            return Ingredient(ingredient[0].toInt(), ingredient[1]);
          }).toList());
    });
    return _recipes;
  }

  int produce(Ingredient toMake) {
    int newAmount(make, min, amount) => (make ~/ min) * amount;

    var recipe = _recipes[toMake.chemical];

    var min = _recipes[toMake.chemical].minAmount;
    var credit = _extra[toMake.chemical] ?? 0;
    var result = 0;

    var make = toMake.amount - credit;

    if (make < 0) {
      credit = -make;
    } else {
      var rounded = roundUp(make, min);
      credit = rounded - make;
      make = rounded;
    }

    _extra[toMake.chemical] = credit;

    if (make > 0) {
      if (recipe.ingredients[0].chemical == 'ORE') {
        result = newAmount(make, min, recipe.ingredients[0].amount);
      } else {
        result = recipe.ingredients.fold(
            0,
            (acc, i) =>
                acc +
                produce(
                    Ingredient(newAmount(make, min, i.amount), i.chemical)));
      }
    }
    return result;
  }
}

Object part1(String header, List input) {
  printHeader(header);
  return NanoFactory(input).produce(Ingredient(1, 'FUEL'));
}

const ONE_TRILLION = 1000000000000;

//Brute force - takes about 10 minutes.
Object part2a(String header, List input, int orePerFuel) {
  printHeader(header);
  var nf = NanoFactory(input);
  var old = 1;
  var next = 2;

  while (nf.produce(Ingredient(next, 'FUEL')) < ONE_TRILLION) {
    if (next % 1000000 == 0) print(next);
    old = next;
    next++;
  }
  return old;
}

//Binary search - takes 1 sec.
Object part2(String header, List input, int orePerFuel) {
  printHeader(header);
  var nf = NanoFactory(input);
  var min = 1;
  var max = ONE_TRILLION;
  while (max - min > 1) {
    var mid = (min + max) ~/ 2;
    if (nf.produce(Ingredient(mid, 'FUEL')) > ONE_TRILLION) {
      max = mid;
    } else {
      min = mid;
    }
  }
  return min;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/day14-test.txt');
  List testInputB = FileUtils.asLines('../data/day14b-test.txt');
  List testInputC = FileUtils.asLines('../data/day14c-test.txt');
  List testInputD = FileUtils.asLines('../data/day14d-test.txt');
  List testInputE = FileUtils.asLines('../data/day14e-test.txt');

  List mainInput = FileUtils.asLines('../data/day14.txt');

  assertEqual(part1('14 test part 1', testInput), 31);
  assertEqual(part1('14 test part 1b', testInputB), 165);
  assertEqual(part1('14 test part 1c', testInputC), 13312);
  assertEqual(part1('14 test part 1d', testInputD), 180697);
  assertEqual(part1('14 test part 1e', testInputE), 2210736);

  // assertEqual(part2('14 test part 2', testInput), 1);
  assertEqual(part2('14 test part 2c', testInputC, 13312), 82892753);
  assertEqual(part2('14 test part 2d', testInputD, 180697), 5586022);
  assertEqual(part2('14 test part 2e', testInputE, 2210736), 460664);

  printAndAssert(part1('14 part 1', mainInput), 261960);
  printAndAssert(part2('14 part 2', mainInput, 261960), 4366186);
}
