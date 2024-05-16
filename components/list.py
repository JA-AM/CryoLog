import streamlit as st
import plotly.express as px
from components.food_search import get_nutritional_info, search_food

def clear():
    st.session_state.search_input = ""

def show_list(db, currUser, userFoods):
    for i, food in enumerate(userFoods):
        with st.popover(f"{food['description']}({food['brandName']})"):
            st.markdown(f"Food Category: {food['brandedFoodCategory']}")
            st.markdown(f"FDC ID: {food['fdcId']}")
            st.markdown(f"Ingredients: {food['ingredients']}")
            with st.expander("Label Nutrients", expanded=False):
                extract_keys = ['carbohydrates', 'fat', 'protein']
                macros = {key: food['labelNutrients'][key] for key in extract_keys if key in food['labelNutrients']}
                # other_values = sum(value for key, value in food['labelNutrients'].items() if key not in extract_keys)
                # macros['other'] = other_values
                data = {'Macros ': list(macros.keys()), 'Value ': list(macros.values())}
                fig = px.pie(data, names='Macros ', values='Value ', title='Macros')
                # data = {'Components ': list(food['labelNutrients'].keys()), 'Value ': list(food['labelNutrients'].values())}
                # fig = px.pie(data, names='Components ', values='Value ', title='Nutrients')
                st.plotly_chart(fig, use_container_width=True)
                st.write('All Nutritional Information')
                st.json(food['labelNutrients'], expanded=False)
            if st.button("Delete", key=i): 
                del userFoods[i] 
                db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
                st.switch_page('app.py')

def search(db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data['Foods'] if 'Foods' in user_data else []
    
    with st.expander('Search'):
        search_query = st.text_input("Food Search:", key="search_input")
        if search_query:
            query = search_query.strip()
            if query:
                foods = search_food(query)
                placeholder_search = st.empty()
                placeholder_btn = st.empty()
                selections = placeholder_search.multiselect(f"Found {len(foods)} results for '{query}':", \
                                            [f"{food['description'].title()}, {food.get('brandOwner', 'N/A')}, FDCID: {food['fdcId']}" for food in foods])
                if placeholder_btn.button("Add To List", key='foodsendbtn'):
                    for selection in selections:
                        id = selection.split(" ")[-1]
                        nutritional_info = get_nutritional_info(id)
                        userFoods.append(nutritional_info)
                    
                    db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
                    placeholder_search.empty()
                    placeholder_btn.empty()
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a search query.")
    
    with st.container(border=True):
        st.subheader('My List')
        st.write("✦ " * 4) 
        show_list(db, currUser, userFoods)

if __name__ == "__main__":
    search()
