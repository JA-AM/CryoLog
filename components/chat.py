import streamlit as st
from snowflake.snowpark.session import Session

import pandas as pd

session = Session.builder.configs(st.secrets['SNOWFLAKE_CONFIG']).create()

pd.set_option("max_colwidth", None)
num_chunks = 3

def create_prompt(myquestion, rag, option_index):
    url = ""
    # Use context
    if rag == 1:
        if option_index == 0:
            prompt, url = nutritional_prompt(myquestion)
        elif option_index == 1:
            prompt, url = ingredients_prompt(myquestion)
        else:
            prompt = ""
    # No context
    else:
        prompt = f"""
         'Question:  
           {myquestion} 
           Answer: '
           """
        
    return prompt, url

def nutritional_prompt(myquestion):
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

    # TODO add conditions and preferences from firebase
    prompt = f"""
          'You are an expert nutritional advisor that uses the context provided to generate a well-informed reponse. 
           Answer the question based on the context. Be concise and do not hallucinate. 
           If you don't have the information, tell me you do not have it, and advise me to uncheck the "Use Context" box.
          Context: {prompt_context}
          My Medical Conditions:
          My Preferences:
          Question:  
           {myquestion} 
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
          Question:  
           {myquestion} 
           Answer: '
           """

    return prompt, url_link

def complete(myquestion, rag, option_index):
    prompt, url = create_prompt(myquestion, rag, option_index)
    cmd = f"""
             select snowflake.cortex.complete(?,?) as response
           """
    
    df_response = session.sql(cmd, params=['snowflake-arctic', prompt]).collect()
    return df_response, url 

def display_response(question, rag, option_index):
    response, url = complete(question, rag, option_index)
    res_text = response[0].RESPONSE
    st.markdown(res_text)

    if rag == 1:
        display_url = f"[Link]({url}) that may be useful"
        st.markdown(display_url)

#Main code
def chat():
    st.title("Snowflake Cortex: The Nutritionist")

    options = ['General Nutritional Advice', 'Learn More About Specific Ingredients', 'Help With My List']
    option_index = 0

    selected_option = st.selectbox('Select an option:', options, index=0)

    if selected_option == 'General Nutritional Advice':
        question = st.text_input("Enter question", placeholder="What is an example of a healthy breakfast?", label_visibility="collapsed")
        option_index = 0
    elif selected_option == 'Learn More About Specific Ingredients':
        question = st.text_input("Learn more about: ", placeholder="arabinoxylan", label_visibility="collapsed")
        option_index = 1
    else:
        question = st.text_input("Enter question", placeholder="Generate a list for me!", label_visibility="collapsed")
        option_index = 2

    rag = st.checkbox('Use Context? (Recommended)', value=True)

    if rag:
        use_rag = 1
    else:
        use_rag = 0

    if question:
        display_response(question, use_rag, option_index)

if __name__ == '__main__':
    chat()