import requests
import json


class Puppy(object):

    def search_recipe(self, query="chicken"):
        if isinstance(query,list):
            query = ','.join(query)
        url = 'http://www.recipepuppy.com/api/?i=' + query + '&p=6'

        r = requests.get(url)
        results = r.json()["results"]

        recipes = {}
        for recipe in results:
            name = recipe["title"]
            recipes[name] = {}
            recipes[name]["picture"] = recipe["thumbnail"]
            recipes[name]["ingredients"] = recipe["ingredients"]
            recipes[name]["url"] = recipe["href"]
        return recipes

