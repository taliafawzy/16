from py_edamam import Edaman

test = Edaman(recipes_appid='f3fd7ba6',
           recipes_appkey='2171c8a5d3d1bc0087955191c4209734')

print(test.search_recipe("chicken"))