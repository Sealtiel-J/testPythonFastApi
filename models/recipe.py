from pydantic import BaseModel, HttpUrl


class RecipeBase(BaseModel):
    label: str
    source: str
    url: str


class Recipe(RecipeBase):
    recipeid: int

    class Config:
        from_attributes = True


class RecipeCreate(RecipeBase):
    pass
