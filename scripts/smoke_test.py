from pathlib import Path
from aletheia.data.load_data import load_movielens
from aletheia.data.interactions import to_implicit

df = load_movielens(Path("data/ml-100k"))
implicit = to_implicit(df)

print(implicit.head())
print(len(implicit))