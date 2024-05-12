import streamlit as st
import requests

def search_food(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": st.secrets['FOODDATA_API_KEY'],
        "query": query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["foods"][:10]
    else:
        return None

def main():
    st.title("FoodData Search App")

    with st.form(key='search_form'):
        search_query = st.text_input("Enter a food item to search:")
        submitted = st.form_submit_button("Search")
        
        if submitted:
            query = search_query.strip()
            if query:
                foods = search_food(query)
                
                if foods:
                    st.write(f"Found {len(foods)} results for '{query}':")
                    for food in foods:
                        st.write(f"- {food['description']}")
                else:
                    st.write("No results found.")
            else:
                st.write("Please enter a search query.")

if __name__ == "__main__":
    main()
