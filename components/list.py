import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from components.food_search import get_nutritional_info, search_food
from components.list_items import display_items

def clear():
    st.session_state.search_input = ""

def search(db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data['Foods'] if 'Foods' in user_data else []
    
    with stylable_container(
        key = "searchcontainer",
        css_styles= """
        {
            background-color: #111111;
            border: 0.1px solid #222e3b2;
            border-radius: 0.5rem;
        }
        """
        ):
        with st.expander('**Search**'):
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
                        st.snow()
                else:
                    st.write("No results found.")
            else:
                st.write("Please enter a search query.")

    with stylable_container(
        key = "listcontainer",
        css_styles= """
        {
            background-color: #111111;
            border: 0.1px solid #222e3b2;
            border-radius: 0.5rem;
            padding: 1em;
        }
        """
        ):
        c1, c2 = st.columns([7,1])
        with c1:
            st.subheader('My Shopping List')
        with c2:
            if st.button('Clear'):
                db.child("users").child(currUser["localId"]).child("Foods").remove()
                st.toast("List sucessfully cleared")
                st.switch_page("app.py")
        st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
        display_items(db, userFoods, is_remove=True)

if __name__ == "__main__":
    search()
