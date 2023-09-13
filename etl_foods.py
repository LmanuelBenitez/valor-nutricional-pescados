import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Datos generales de el Data Frame, tipos de datos de sus columnas, el nombre de las columnas y las descripciones generales
def general_features(df):
    print(df.describe())
    print(df.dtypes)
    print(df.columns)

#Division de la descripcion de los alimentos por (nombre, tipo y forma de presentación)
def features_of_ingredients(df):

    ingredients_with_features = df.drop_duplicates(subset=['Ingredient description'])

    #Cambiar el formato de las columnas, para un manejo mas sencillo y estadar
    ingredients_with_features = df[['Ingredient code', 'Ingredient description', 'Nutrient code', 'Nutrient description', 'Nutrient value']]
    ingredients_with_features.columns = ingredients_with_features.columns.str.lower()
    ingredients_with_features.columns = ingredients_with_features.columns.str.replace(' ', '_')

    #Crear las nuevas columnas a partir de la separacion de la columna 'ingredient_description'
    features = df['Ingredient description'].str.split(', ', n=2, expand=True)
    ingredients_with_features[['food_name', 'fish_name', 'way_eat']] = features[[0, 1, 2]]

    #Remplazo de aquellos nutrientes con descripciones conflictivas, para mejorar la consulta de estos
    nutrient_replace = {'Sugars, total' : 'Sugars', 'Fiber, total dietery' : 'Fiber', 'Vitamin A, RAE' : 'Vitamin A', 'Cryptoxanthin, beta' : 'Cryptoxanthin', 
                        'Vitamin E (alpha-tocopherol)' : 'Vitamin E', 'Vitamin D (D2 + D3)' : 'Vitamin D', 'Folate, total' : 'Folate total', 
                        'Choline, total' : 'Choline', 'Vitamin K (phylloquinone)' : 'Vitamin K', 'Folate, food' : 'Folate food', 'Folate, DFE' : 'Folate DFE', 
                        'Vitamin E, added' : 'Vitamin E added', 'Vitamin B-12, added' : 'Vitamin B-12 added', 'Fatty acids, total satured' : 'fatty acids', 
                        'Fatty acids, total monounsaturated' : 'Acids monounsaturated', 'Fatty acids, total polyunsaturated' : 'Acids polyunsaturated'}        

    ingredients_with_features.loc[ : , 'nutrient_description'] = ingredients_with_features['nutrient_description'].replace(nutrient_replace)

    #Retorna el nuevo dataframe con la limpieza requerida a los datos
    return ingredients_with_features

#Funcion que filtra aquellos alimentos que solo son peces, ademas de crear nuevas columnas para describir mejor cada pez
def df_fishes(df):

    #Limitamos el numero de columnas que vamos a usar
    fishes = df[['ingredient_description', 'nutrient_description', 'nutrient_value', 'food_name', 'fish_name', 'way_eat']]
    
    fishes = fishes.drop_duplicates(subset=['ingredient_description']) #Eliminamos todo aquel registro duplicado
    fishes = fishes[fishes['food_name'] == 'Fish'] #Filtramos solo los alimentos que son pescados
    fishes = fishes.reset_index() #Resetamos los indices del dataframe
    unique_fishes = pd.unique(fishes['ingredient_description'])

    #Lista de las formas en las que se cocina el prescado (SOLO AQUELLAS QUE ESTAN DENTRO DEL DF)
    ways = ['raw', 'canned in oil', 'dry heat', 'canned', 'dried and salted', 'frozen', 'smoked', 'pickled', 'canned in water', 'granular']

    #Funcion que compara la columna de descripcion de alimentos con la lista de arriba, retorna la palabra con la que coincida en la lista
    def extract_word(text, words):
        for word in words:
            if word in text:
                return word

    fishes['way_eat'] = fishes['ingredient_description'].apply(extract_word, args=[ways]) #Aplicamos la funcion con el metodo 'apply'
    fishes_by_wayEat = fishes.groupby(by=['way_eat'])['nutrient_value'].mean() #Agrupamos el dataframe por la forma de consumo y obtenemos la media de la cantidad de proteína
    fishes['specie_wayEat'] = fishes['fish_name'] + ' ' + fishes['way_eat'] #Creamos una nueva columna a partir de el nombre del pez y la forma de consumo

    #Creamos un grafico de barras en base a todos los peces y la cantidad de proteinas
    plot_protein_fishes = plt.figure()

    sns.barplot(x=fishes['nutrient_value'], y=fishes['specie_wayEat'], orient='horizontal', color='blue')
    plt.xlabel('Proteina por cada 100 grs')
    plt.ylabel('Pescado y forma de consumo')
    plt.title('Valores de proteína', fontsize=15, color='darkblue')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    #Creamos otro grafico, pero ahora referente a las formas de consumo y la media de proteina de cada forma
    plot_protein_watEat = plt.figure()

    bar_fishes = fishes_by_wayEat.plot.barh(color='blue', xlabel='Forma de consumo', ylabel='Cantidad de proteína', 
                                            title='Proteínas por forma de consumo', fontsize=8)

    plt.show()


if __name__ == '__main__':

    df = pd.read_excel('./2019-2020 FNDDS - Ingredient Nutrient Values.xlsx', header=1)

    features = features_of_ingredients(df)
    df_fishes(features)

