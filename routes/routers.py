import json
from os import name
from pathlib import Path as dirPath
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from database.db_postgres import SessionLocal
import models.models as mod
import models.recipe as schema
import app.crud as crud

# mod.Base.metadata.create_all(bind=engine)
BASE_PATH = dirPath(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str("templates"))

router = APIRouter()


def get_db():
    base_datos = SessionLocal()
    try:
        yield base_datos
    finally:
        base_datos.close()


@router.get("/", status_code=200)
async def page_main(request: Request, db: Session = Depends(get_db)):
    return TEMPLATES.TemplateResponse(
        'index.html',
        {'request': request, 'recipes': crud.get_all_recipes(db)}
    )


@router.get('/', description='Hello world endpoint', tags=['Hello'])
async def hello():
    return {'message': 'Hello World!'}


@router.post('/form', )
async def create_recipe(request: Request, label: str = Form(),
                        source: str = Form(),
                        url: str = Form(),
                        db: Session = Depends(get_db)):
    db_recipe = schema.RecipeCreate(label=label, source=source, url=url)
    recipe = db_recipe.model_dump()
    return recipe


@router.get('/form/{label}')
def get_form(db: Session = Depends(get_db), label: str = Path(description='food lable')):
    db_recipe = crud.search_recipe(db, keyword=label, max_results=10)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.post('/recipes', response_model=schema.Recipe, description='Create a recipe', tags=['Recipe'])
async def create_recipe(recipe: schema.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)


@router.get('/recipe/{recipe_id}', response_model=schema.Recipe, description='Retrieve a recipe', tags=['Recipe'])
async def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipeid=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail=f'Recipe with id {recipe_id} not found')
    return db_recipe


@router.get('/search/', response_model=list[schema.Recipe], description='Search for a recipe', tags=['Recipe'])
async def search_recipe(keyword: Optional[str] = None, max_results: Optional[int] = 10, db: Session = Depends(get_db)):
    db_recipe = crud.search_recipe(db, keyword=keyword, max_results=max_results)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.get('api/recipe/{recipe_id}', description='Retrieve a recipe', tags=['Recipe noDB'])
async def get_recipe(recipe_id: int):
    result = [recipe for recipe in mod.RECIPES if recipe["recipeid"] == recipe_id]
    if not result:
        raise HTTPException(status_code=404, detail=f'Recipe with id {recipe_id} not found')


@router.get('api/search/', description='Search for recipes', tags=['Recipe noDB'])
async def search_recipes(keyword: Optional[str] = None, max_results: Optional[int] = 10):
    if not keyword:
        return mod.RECIPES[:max_results]
    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), mod.RECIPES)
    return list(results)[:max_results]
