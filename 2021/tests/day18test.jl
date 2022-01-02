using AdventOfCodeUtils
using DelimitedFiles
using Test

include("../src/day18.jl")


function test_magnitude()
  @testset "Magnitude" begin
    @test magnitude("[[1,2],[[3,4],5]]") == 143


    @test magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    @test magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    @test magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    @test magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    @test magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488
  end
end

function test_explode()
  @testset "Explode" begin
    @test explode_wrapper("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    @test explode_wrapper("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    # big nuumbers to check increment of numbers left and right of
    # nested pair 
    @test explode_wrapper("[[6,[5,[114,[103,200]]]],11]") == "[[6,[5,[217,0]]],211]"
    @test explode_wrapper("[[[[0,7],4],[15,[0,13]]],[1,1]]") === nothing
    @test explode_wrapper("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    @test explode_wrapper("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    @test explode_wrapper("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    @test explode_wrapper("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
  end
end

function test_split()
  @testset "Split" begin
    @test split("[[[[0,7],4],[15,[0,13]]],[1,1]]") == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    @test split("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]") == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
  end
end

function test_add()
  @testset "Add" begin
    @test add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
  end
end

function test_all()
  @testset "Full example" begin
    s = add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]")
    @test s == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    s = explode_wrapper(s)
    @test s == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
    s = explode_wrapper(s)
    @test s == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    s = split(s)
    @test s == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    s = split(s)
    @test s == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    @test explode_wrapper(s) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
  end
end

function test_lists()
  @testset "Reduce list" begin
    @test reduce_list(["[1,1]", "[2,2]", "[3,3]", "[4,4]"]) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"

    @test reduce_list(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"

    @test reduce_list(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"]) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
    a1 = add("[1,1]", "[2,2]")
    a2 = add(a1, "[3,3]")
    a3 = add(a2, "[4,4]")
    @test a3 == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    @test reduce(a3) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
  end
end

function run()
  @testset "All tests" begin
    test_explode()
    test_split()
    test_add()
    test_all()
    test_lists()
    test_magnitude()
  end
end

run()
