import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

class Food {
  List input;
  Map<String, List<Set<String>>> allergensToIngredientsMap =
      <String, List<Set<String>>>{};
  // Map ingredientsToAllergensMap = {};

  Map<String, Set<String>> allergenCandidates = {};

  var allIngredients = [];

  static RegExp REGEX_INPUT =
      RegExp(r'^(?<ingredients>.*) \(contains (?<allergens>.*)\)$');

  Food(this.input) {
    parseInput();
  }
  void parseInput() {
    input.forEach((line) {
      Food.REGEX_INPUT.allMatches(line).forEach((m) {
        var ingredients = m.namedGroup('ingredients').split(' ').toSet();
        var allergens = m.namedGroup('allergens').split(', ');

        allIngredients.addAll(ingredients);
        allergens.forEach((a) {
          var ingredientsList = allergensToIngredientsMap[a] ?? <Set<String>>[];
          ingredientsList.add(ingredients);
          allergensToIngredientsMap[a] = ingredientsList;
        });
      });
    });

    //create of form map[allergen]={unique ingredients that could be allergen}
    allergenCandidates = allergensToIngredientsMap
        .map((a, i) => MapEntry(a, i.expand((x) => x).toSet()));
  }

  int findNonAllergens() {
    allergensToIngredientsMap.entries.forEach((kv) {
      kv.value.forEach((ingSet) {
        allergenCandidates[kv.key] =
            allergenCandidates[kv.key].intersection(ingSet);
      });
    });

    //remove allergens from all ingredients list
    allIngredients.removeWhere((i) =>
        allergenCandidates.values.expand((ing) => ing).toSet().contains(i));
    // print(allergenCandidates);
    return allIngredients.length;
  }

  //We need to narrow each set down to one element per allergen then
  //return the ingredients in allergen order
  String ingredientsInAllergenOrder() {
    while (true) {
      var singleElementSets =
          allergenCandidates.values.where((v) => v.length == 1);
      var multipleElementSets =
          allergenCandidates.values.where((s) => s.length > 1);
      if (multipleElementSets.isEmpty) break;
      singleElementSets.forEach((singles) => multipleElementSets
          .forEach((multiples) => multiples.remove(singles.first)));
    }
    var result = '';

    allergenCandidates.keys.toList()
      ..sort()
      ..forEach((k) => result += '${allergenCandidates[k].first},');

    return result;
  }
}

void runPart1and2(String name, List input) {
  printHeader(name);
  var food = Food(input);
  print(food.findNonAllergens());
  print(food.ingredientsInAllergenOrder());
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day21-test.txt');
  MAIN_INPUT = fileAsString('../data/day21.txt');

  //Answer: 5
  //Answer: mxmxvkd,sqjhc,fvjkl,
  runPart1and2('21 test part 1 and 2', TEST_INPUT);

  //Answer: 2315
  //Answer: cfzdnz,htxsjf,ttbrlvd,bbbl,lmds,cbmjz,cmbcm,dvnbh,
  runPart1and2('21 part 1 and 2', MAIN_INPUT);
}
