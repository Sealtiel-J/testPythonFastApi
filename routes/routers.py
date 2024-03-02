from typing import Optional
from fastapi import APIRouter
import json
from models.models import RECIPES


router = APIRouter()


@router.get('/', description='Hello world endpoint', tags=['Hello'])
async def hello():
    return {'message': 'Hello World!'}


@router.get('/recipe/{recipe_id}', description='Retrive a recipe', tags=['Recipe'])
async def get_recipe(recipe_id: int):
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]
    else:
        return json.loads('{"msg": "Recipe doesnt exist"}')


@router.get('/search/', description='Search for recipes', tags=['Recipe'])
async def search_recipes(keyword: Optional[str] = None, max_results: Optional[int] = 10):
    if not keyword:
        return RECIPES[:max_results]
    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), RECIPES)
    return list(results)[:max_results]
