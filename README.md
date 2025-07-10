# Advent of Code

### Update 3 (Dec 2024)

At some point, I switched to Python for doing Advent of Code. I learnt the language for a machine learning course a few years ago.

To run the Python code, change to the `src` directory then run program. For example:

```
cd advent_of_code/2020/src
python day06.py
```

Generally, the programs will use the test input files and the real input files in the corresponding `data` directory. However, the `data` directories contain only the test input files. These are copied from each day's problem description. The real input files are personal to each user and the creator of Advent of Code has asked not to share the files. If you haven't already, you'll need to register for Advent of Code. Once registered, you can download your input files and place them in the right year's `data` directory. Remember to rename the file to match the day's number. The filename format for the real input files is `dayXX.txt` where XX is the day's number, starting at 01, 02, ..., 25.

Since the real input files are not in the `data` directory, you will get an error if you try to run the programs unamended. To run the scripts without the real input files, comment out the parts that use the real input files.

You may need to install some Python libraries by running:

```
python3 -m ensurepip --default-pip
pip install numpy
pip install matplotlib
```

For Advent of Code, I've switched from Dart to Julia to Python. At some point, I'll discover another interesting language and will try that out.

These are the other languages, in no particular order, I've used over the years (not for Advent of Code): Fortran, Algol 68, Pascal, C, C#, Java, JavaScript, Ruby, SQL, PHP, Perl, Octave/Matlab, Visual Basic, Delphi, and various shell scripting languages.


### Update 2 (Dec 2021)

I have 1.5 problems remaining for Aoc 2019. However, AoC 2021 has arrived. I'm doing this in Julia, which I know nothing about; I haven't even read a tutorial! My solutions for 2021, therefore, are the first bits of code I've ever written in Julia. Initially, they will probably look generically procedural but hopefully will become more idiomatic Julia as I learn the language.

### Update 1

Having completed AoC 2020, I'm slowly working my way through AoC 2019.
This repository has solutions to the 2020 programming challenges on [Advent of Code](https://adventofcode.com).

### Original

I'm learning [Flutter](https://api.flutter.dev/index.html) and, therefore, Dart too. [Dart](https://dart.dev/) is the programming language used to develop Flutter apps. Dart seems primarily to be a cross between Java, JavaScript and C#.

I recently came across the Advent of Code 2020. Attempting to solve the puzzles seemed a good way to learn a new programming language.

Sometimes the solutions seem verbose but I like to write code that you can read like prose and have some idea what's going on. Sometimes, I'm also trying to incorporate Dart features so that I can learn how to use them. For example, on Day 2, using named groups in the regular expressions was not necessary but it was good to learn their syntax. The regular expression itself follows JavaScript so there are plenty of examples on the web if you can't work out an expression.

Please feel free to suggest improvements, especially to make the code more Dart-like instead of the hybrid Java/JavaScript it tends to be whilst I learn Dart.

To run, go to directory `advent_of_code/2020/src` and run the day's program. For example, to run day 6's solution:

```
cd advent_of_code/2020/src
dart ./day06.dart
```

To enable assertions in dart:

```
dart --enable-asserts ./day06.dart
```

I wrote these on Windows 10 but Dart can run on Linux and macOS.

The story of my Advent of Code 2020 is on my [blog](https://prafulkapadia.com/2021/01/05/advent-of-code-2020/).
