from sqlalchemy.orm import Session
import models.models as mod
import models.recipe as schema


def get_recipe(db: Session, recipeid: int):
    return db.query(mod.Recipe).filter(mod.Recipe.recipeid == recipeid).first()


def get_all_recipes(db: Session):
    return db.query(mod.Recipe).all()


def get_recipe_by_label(db: Session, keyword: str):
    return db.query(mod.Recipe).filter(mod.Recipe.label.like(f'%{keyword}%')).all()


def create_recipe(db: Session, recipe: schema.RecipeCreate):
    db_recipe = mod.Recipe(label=recipe.label, source=recipe.source, url=recipe.url )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def search_recipe(db: Session, max_results: int, keyword: str):
    if not keyword:
        return db.query(mod.Recipe).limit(max_results)
    else:
        return db.query(mod.Recipe).filter(mod.Recipe.label.like(f'%{keyword}%')).limit(max_results)
