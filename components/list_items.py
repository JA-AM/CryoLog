import streamlit as st
from components.food_search import get_nutritional_info_barcode, get_nutritional_info
import plotly.express as px

@st.experimental_fragment()
def display_items(db, items_list, is_barcode=False, is_remove=False):
    from components.chat import complete

    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    userFoods = user_data.get("Foods", [])

    if is_barcode and not items_list:
        st.write('No scannable items found yet :(')

    for i, item in enumerate(items_list):
        if is_barcode:
            product_info = get_nutritional_info_barcode(item)
        else:
            product_info = get_nutritional_info(item['fdcId'])
        
        if product_info is None and is_barcode:
            st.toast(f"No Information For Barcode: {item}")
            continue
        
        with st.popover(f"{product_info['description']}({product_info['brandName']})"):
            st.markdown(f"**Food Category:** {product_info['brandedFoodCategory']}")
            st.markdown(f"**FDC ID:** {product_info['fdcId']}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Ingredients:** {product_info['ingredients']}")
            
            with col2:
                with st.expander("Learn more", expanded=False):
                    if st.button("Generate Overview", key=str(i)+"ai"):
                        prompt = f"""You are an expert in nutritional ingredients. Give accurate
                        and consistent answers. If you are not sure about something, just say so.
                        You are given a list of ingredients. 
                        Give a brief overview of each ingredient, using 2-3 sentences. Output your answer
                        in markdown format in a bulleted list, with the ingredient bolded, and just the text overview in normal text. Do not create a title.
                        Ingredients list: {product_info['ingredients']}"""
                        response, _ = complete(prompt, 0, 0, db)
                        res_text = response[0].RESPONSE
                        st.markdown(res_text)
            
            nutrient_key = 'labelNutrients' if 'labelNutrients' in item else 'foodNutrients'
            with st.expander("Nutrient Information", expanded=False):
                extract_keys = ['carbohydrates', 'fat', 'protein', 'total lipid (fat)', 'carbohydrate, by difference']
                macros = {key: item[nutrient_key][key] for key in extract_keys if key in item[nutrient_key]}
                # other_values = sum(value for key, value in food['labelNutrients'].items() if key not in extract_keys)
                # macros['other'] = other_values
                data = {'Macros ': list(macros.keys()), 'Value ': list(macros.values())}
                fig = px.pie(data, names='Macros ', values='Value ', title='Macros')
                # data = {'Components ': list(food['labelNutrients'].keys()), 'Value ': list(food['labelNutrients'].values())}
                # fig = px.pie(data, names='Components ', values='Value ', title='Nutrients')
                st.plotly_chart(fig, use_container_width=True)
                st.write('All Nutritional Information')
                st.json(item[nutrient_key], expanded=False)
            
            if not is_remove:
                num_items = st.number_input("Number of Items to Add", 1, 10, key=str(i)+"num")

            if not is_remove and st.button("Add to List", key=i):
                st.toast(f"Added {num_items} {product_info['description']} to My List", icon="✅") 
                userFoods.extend([product_info] * num_items)
                db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
            
            if is_remove and st.button("Delete", key=i): 
                del userFoods[i] 
                db.child("users").child(currUser["localId"]).child("Foods").set(userFoods)
                st.switch_page('app.py')