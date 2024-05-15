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

def search(db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data['Foods'] if 'Foods' in user_data else []

    st.subheader("FoodData Search App")
    col1, col2 = st.columns([1,2])
    with col1:
        search_query = st.text_input("Food Search:", key="search_input")
        
        if search_query:
            query = search_query.strip()
            if query:
                foods = search_food(query)
                placeholder = st.empty()
                selection = placeholder.multiselect(f"Found {len(foods)} results for '{query}':", \
                                           [f"{food['description']}  \nBrand: {food.get('brandOwner', 'N/A')}  \nFDCID: {food['fdcId']}" for food in foods])
                if st.button("Add To List", key='foodsendbtn'):
                    userFoods.extend(selection)
                    db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
                    placeholder.empty()
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a search query.")
    
    with col2:
        for i, food in enumerate(userFoods):
            with st.popover(food):
                st.markdown(food)
                if st.button("Delete", key=i): 
                    print(userFoods)
                    del userFoods[i] 
                    print(userFoods)
                    db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
                    st.switch_page('app.py')

if __name__ == "__main__":
    search()
