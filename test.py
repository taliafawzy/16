from puppy import *

test = Puppy()

lijst = test.search_recipe(["cheese"])

ingrediënten = []
for key in lijst:
    rijen = lijst[key]['ingredients']
    ingredients =[x.strip() for x in rijen.split(",")]
    for ingredient in ingredients:
        if ingredient in ingrediënten:
            continue
        else:
            ingrediënten.append(ingredient)
print(ingrediënten)