import streamlit as st
import requests

def search_food(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": st.secrets['FOODDATA_API_KEY'],
        "query": query,
        "limit": 10,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["foods"][:10]
    else:
        return None

def search():
    selections=[]
    st.title("FoodData Search App")
    search_query = st.text_input("Enter a food item to search:")
    
    if search_query:
        query = search_query.strip()
        if query:
            foods = search_food(query)
            selection = st.multiselect(f"Found {len(foods)} results for '{query}':", [food['description'] for food in foods])
            if st.button("Submit", key="foodsbtn"):
                selections.extend(selection)
                st.write(selections)
                search_query = None
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a search query.")

if __name__ == "__main__":
    search()
