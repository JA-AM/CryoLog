import streamlit as st
from snowflake.snowpark.session import Session
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import markdown
import time
from components.food_search import search_food, get_nutritional_info
from components.list_items import display_items

session = Session.builder.configs(st.secrets['SNOWFLAKE_CONFIG']).create()

pd.set_option("max_colwidth", None)
num_chunks = 3

def create_prompt(myquestion, rag, option_index, db):
    url = ""
    # Use context
    if rag == 1:
        if option_index == 0:
            prompt, url = nutritional_prompt(myquestion, db)
        elif option_index == 1:
            prompt, url = ingredients_prompt(myquestion)
        else:
            prompt = list_prompt_1(myquestion, db)
    # No context
    else:
        if option_index == 2:
            prompt = list_prompt_1(myquestion, db)
        else:
            prompt = f"""
                'Question:  
                {myquestion} 
                Answer: '
            """
        
    return prompt, url

def nutritional_prompt(myquestion, db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()

    cmd = """
         with results as
         (SELECT RELATIVE_PATH,
           VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
                    snowflake.cortex.embed_text_768('e5-base-v2', ?)) as distance,
           chunk
         from docs_chunks_table
         order by distance desc
         limit ?)
         select chunk, relative_path from results 
         """
    
    df_context = session.sql(cmd, params=[myquestion, num_chunks]).to_pandas()  
    relative_path = df_context._get_value(0,'RELATIVE_PATH')    
    
    context_length = len(df_context) -1

    prompt_context = ""
    for i in range (0, context_length):
        prompt_context += df_context._get_value(i, 'CHUNK')
    
    prompt_context = prompt_context.replace("'", "")

    biometrics = user_data.get("Biometrics", "")
    preferences = user_data.get("Preferences", "")
    goals = user_data.get("Goals", "")
    

    prompt = f"""
          'You are an expert nutritional advisor that uses the context provided to generate a well-informed reponse. 
           Answer the question based on the context. Be concise and do not hallucinate. 
           If you don't have the information, tell me you do not have it, and advise me to uncheck the "Use Context" box.
            Context: {prompt_context}
            My Biometrics: {biometrics}
            My Preferences: {preferences}
            My Goals: {goals}
            Question: {myquestion} 
           Answer: '
           """
    
    cmd2 = f"select GET_PRESIGNED_URL(@docs, '{relative_path}', 360) as URL_LINK from directory(@docs)"
    df_url_link = session.sql(cmd2).to_pandas()
    url_link = df_url_link._get_value(0,'URL_LINK')
    return prompt, url_link

def ingredients_prompt(myquestion):
    cmd_webmd = f"""
        SELECT URL, OVERVIEW, SIDE_EFFECTS, PRECAUTIONS, DOSING FROM WEBMD_INGREDIENTS_TABLE
        WHERE SUBSTANCE like '%{myquestion}%'
        LIMIT 1
         """
    
    df = session.sql(cmd_webmd, params=[myquestion]).to_pandas()

    url_link = ""
    prompt_context = ""
    if len(df):
        for column_name in df.columns:
            text = df.at[0, column_name]
            
            if column_name == 'URL':
                url_link = text
            if text is not None:
                prompt_context += text
        
        prompt_context = prompt_context.replace("'", "")

    prompt = f"""
          'You are an expert in nutritional substances that uses the context provided to generate a well-informed reponse. 
           Answer the question based on the context. Separate you answer sections into "Overview", "Intended Use", and "Precautions". Be concise and do not hallucinate. 
           If you don't have the information, tell me you do not have it, and advise me to uncheck the "Use Context" box.
          Context: {prompt_context}
          Question: {myquestion} 
           Answer: '
           """

    return prompt, url_link

def list_prompt_1(myquestion, db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    user_food_list = [food['description'] for food in user_data.get('Foods', [])]
    biometrics = user_data.get("Biometrics", "")
    preferences = user_data.get("Preferences", "")
    goals = user_data.get("Goals", "")

    prompt = f"""
          'You are an expert nutritional assistant designed to give recommended lists of food products
          or ingredients based on the question. Do not include any descriptions of the products or any other non-related text.
          If you are not sure if you can create a list, just say so. Remember to keep
          in mind general nutrition principles, so do not overly rely on a user's preferences,
          but keep them in mind. 
          User Current Food List: {user_food_list}
          User Biometrics: {biometrics}
          User Preferences: {preferences}
          User Goals: {goals}
          Question: {myquestion} 
          (IMPORTANT) Format: Bulleted Markdown List, Max Length 5
           Answer: '
           """
    
    return prompt
    
def list_prompt_2(myquestion, data_list, db):
    currUser = st.session_state['user']
    user_data = db.child("users").child(currUser["localId"]).get().val()
    user_food_list = [food['description'] for food in user_data.get('Foods', [])]
    biometrics = user_data.get("Biometrics", "")
    preferences = user_data.get("Preferences", "")
    goals = user_data.get("Goals", "")

    prompt = f"""
          'You are an expert nutritional assistant designed to select certain products
          based on the question given. You will be supplied a list of dictionaries representing
          each nutritional product and its data. Choose the products based on the question given,
          and the user data. Consider the product macros and nutritional value.
          Your answer must be a list of list indices from the given list in a markdown list. 
          Do not include any descriptions of the products or any other non-related text.
          If you are not sure if you can create a list, just say so. Remember to keep
          in mind general nutrition principles, so do not overly rely on a user's preferences,
          but keep them in mind.
          User Current Food List: {user_food_list}
          User Biometrics: {biometrics}
          User Preferences: {preferences}
          User Goals: {goals}
          Product List: {data_list}
          Question: {myquestion} 
          Answer Format: Markdown bullet list of ONLY the index values for product list
          Answer: '
           """
    
    return prompt

def extract_lists_from_markdown(markdown_text):
    html = markdown.markdown(markdown_text)

    lists = []
    in_list = False
    current_list = []
    for line in html.splitlines():
        if line.strip().startswith('<ul>'):
            in_list = True
        elif line.strip().startswith('</ul>'):
            in_list = False
            if current_list:
                lists.extend(current_list)
                current_list = []
        elif in_list:
            item = line.strip().lstrip('<li>').rstrip('</li>').strip()
            if item:
                current_list.append(item)

    return lists

def complete(myquestion, rag, option_index, db):
    prompt, url = create_prompt(myquestion, rag, option_index, db)
    cmd = f"""
             select snowflake.cortex.complete(?,?) as response
           """
    
    df_response = session.sql(cmd, params=['snowflake-arctic', prompt]).collect()
    return df_response, url 

def display_response(question, rag, option_index, db):
    response, url = complete(question, rag, option_index, db)
    res_text = response[0].RESPONSE
    def stream():
        for word in res_text.split(" "):
            yield word + " "
            time.sleep(0.05)
    
    st.write_stream(stream)

    if rag == 1:
        display_url = f"[Link]({url}) that may be useful"
        st.markdown(display_url)

def display_shopper_response(question, db):
    response1, _ = complete(question, 0, 2, db)
    res_text1 = response1[0].RESPONSE
    st.markdown(res_text1)

    recommended_list = extract_lists_from_markdown(res_text1)

    food_data_list = []
    for item in recommended_list:
        for food in search_food(item)[:3]:
            product_info = get_nutritional_info(food['fdcId'])
            food_data_list.append(product_info)
    
    cmd = f"""
            select snowflake.cortex.complete(?,?) as response
        """
    prompt = list_prompt_2(question, food_data_list, db)
    response2 = session.sql(cmd, params=['snowflake-arctic', prompt]).collect()
    res_text2 = response2[0].RESPONSE

    print(res_text2)
    picked_list = extract_lists_from_markdown(res_text2)

    index_list = []
    for item in picked_list:
        if item.isdigit():
            index_list.append(int(item))
        else:
            try:
                index_list.append(int(item[1:-1]))
            except ValueError:
                pass
    
    final_output = []
    for index in index_list:
        try:
            final_output.append(food_data_list[index])
        except IndexError:
            pass
    
    return final_output

def chat(db):
    with stylable_container(
        key = "chatintrocontainer",
        css_styles= """
        {
            background-color: #111111;
            border: 0.1px solid #222e3b2;
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
        }
        """
        ):
        st.header("Chat With Snowflake Arctic Helpers")
        st.markdown("""<span style='color: #779ecb;'>✦ ✦ ✦ ✦""", unsafe_allow_html=True)
        st.markdown("**Ask any one of our helpers about general dietary information, understanding \
                    complicated nutritional terms, or finding foods based on your needs!**")
        rag = st.toggle('Use Context? (Recommended)', value=True)

        if rag:
            use_rag = 1
        else:
            use_rag = 0
    with stylable_container(
        key = "chatcontainer",
        css_styles= """
        {
            background-color: #111111;
            border: 0.1px solid #222e3b2;
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
        }
        """
        ):
        dietitian, nutritionist, shopper = st.tabs(['Dave the Dietitian', 'Neil the Nutritionist', 'Sarah the Shopper'])
        with dietitian:
            with st.container():
                with st.chat_message('assistant', avatar='🐻‍❄️'):
                    st.write('I provide general nutritional advice!')
                diet_question = st.chat_input(placeholder="What is an example of a healthy breakfast?")
                diet_option_index = 0
                if diet_question:
                    with st.container(border=True):
                        st.markdown("""<span style='color: #779ecb; font-size: 1.5em;'>✦ </span><b style='font-size: 1.5em;'>Dietitian""", unsafe_allow_html=True)
                        with st.chat_message('user'):
                            st.write(diet_question)
                        with st.status('Cooking something up...', expanded=True) as status:
                            display_response(diet_question, use_rag, diet_option_index, db)
                            status.update(label="Answer prepared!", state="complete", expanded=True)
        
        with nutritionist:
            with st.container(border=True):
                with st.chat_message('assistant', avatar='🐧'):
                    st.write('Ask me to learn more about specific ingredients!')
                nutr_question = st.chat_input(placeholder="arabinoxylan")
                nutr_option_index = 1
                if nutr_question:
                    with st.container(border=True):
                        st.markdown("""<span style='color: #779ecb; font-size: 1.5em;'>✦ </span><b style='font-size: 1.5em;'>Nutritionist""", unsafe_allow_html=True)
                        with st.chat_message('user'):
                            st.write(nutr_question)
                        with st.status('Taste testing...', expanded=True) as status:
                            display_response(nutr_question, use_rag, nutr_option_index, db)
                            status.update(label="Ready for review!", state="complete", expanded=True)
        with shopper:
            with st.container(border=True):
                with st.chat_message('assistant', avatar='☃️'):
                    st.write('I can help with your shopping list!')
                shop_question = st.chat_input(placeholder="Generate a list for me!")
                shop_option_index = 2
                if shop_question:
                    with st.container(border=True):
                        st.markdown("""<span style='color: #779ecb; font-size: 1.5em;'>✦ </span><b style='font-size: 1.5em;'>Shopper""", unsafe_allow_html=True)
                        with st.chat_message('user'):
                            st.write(shop_question)
                        with st.status('Browsing...', expanded=True) as status:
                            suggested_items = display_shopper_response(shop_question, db)
                            status.update(label="Found suggestions!", state="complete", expanded=True)
                        display_items(db, suggested_items)
    # if selected_option == 'General Nutritional Advice':
    #     question = st.text_input("Enter question", placeholder="What is an example of a healthy breakfast?", label_visibility="collapsed")
    #     option_index = 0
    # elif selected_option == 'Learn More About Specific Ingredients':
    #     question = st.text_input("Learn more about: ", placeholder="arabinoxylan", label_visibility="collapsed")
    #     option_index = 1
    # else:
    #     question = st.text_input("Enter question", placeholder="Generate a list for me!", label_visibility="collapsed")
    #     option_index = 2

if __name__ == '__main__':
    chat()