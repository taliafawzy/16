from edamam import *

test = Edaman(recipes_appid='f3fd7ba6',
           recipes_appkey='2171c8a5d3d1bc0087955191c4209734')

lijst = test.search_recipe("milk and chicken and cheese")


ingrediënten = []
for key in lijst:
    print(key)
    print(lijst[key]['ingredients'])
    rijen = lijst[key]['ingredients']
    for rij in rijen:
        if rij in ingrediënten:
            continue
        else:
            ingrediënten.append(rij)
print(ingrediënten)