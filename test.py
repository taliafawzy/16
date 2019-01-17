from puppy import *

test = Puppy()

lijst = test.search_recipe(["salmon"])

ingrediënten = []
for key in lijst:
    rijen = lijst[key]['ingredients']
    ingridients =[x.strip() for x in rijen.split(",")]
    for ingridient in ingridients:
        if ingridient in ingrediënten:
            continue
        else:
            ingrediënten.append(ingridient)
print(ingrediënten)