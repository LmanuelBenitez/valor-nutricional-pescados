import pandas as pd

features = []

df_foods = pd.read_excel('./2019-2020 FNDDS - Ingredient Nutrient Values.xlsx', sheet_name=0, header=1)

#print(df_foods.head())

def most_calcium_cheeses():

    df_calcium_cheeses = df_foods[['Ingredient code', 'Ingredient description', 'Nutrient code', 'Nutrient description',
                                                'Nutrient value', 'Nutrient value source']]

    food_composition = df_calcium_cheeses['Ingredient description'].str.split(', ', n=2, expand=True)
    
    df_calcium_cheeses.loc[ : , 'Food name'] = food_composition[0]
    df_calcium_cheeses.loc[ : , 'Food type'] = food_composition[1]
    df_calcium_cheeses.loc[ : , 'Food form'] = food_composition[2]

    cheeses = df_calcium_cheeses[(df_calcium_cheeses['Food name'] == 'Cheese') & (df_calcium_cheeses['Nutrient description'] == 'Calcium')].sort_values(by='Nutrient value', ascending=False)
    print(cheeses[['Ingredient code', 'Ingredient description', 'Nutrient description', 'Nutrient value', 'Food type']].head())

    #print(df_calcium_cheeses['Food name'].tail)
    #print(len(df_calcium_cheeses['Ingredient description']))

if __name__ == '__main__':
    most_calcium_cheeses()