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

def clear():
    st.session_state.search_input = ""

def search(auth, db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data['Foods'] if 'Foods' in user_data else []

    st.title("FoodData Search App")
    search_query = st.text_input("Enter a food item to search:", key="search_input")
    
    if search_query:
        query = search_query.strip()
        if query:
            foods = search_food(query)
            selection = st.multiselect(f"Found {len(foods)} results for '{query}':", [food['description'] for food in foods])
            if st.button("Submit", on_click=clear, key='foodsendbtn'):
                userFoods.extend(selection)
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a search query.")
    
    newFoodList = st.multiselect("USER FOODS", userFoods)
    if st.button("Submit", on_click=st.write("Done!"), key='foodlistbtn'):
        db.child("users").child(currUser["localId"]).child("Foods").set(newFoodList)

if __name__ == "__main__":
    search()
