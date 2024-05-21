```
 ██████╗██████╗ ██╗   ██╗ ██████╗ ██╗      ██████╗  ██████╗  
██╔════╝██╔══██╗╚██╗ ██╔╝██╔═══██╗██║     ██╔═══██╗██╔════╝  
██║     ██████╔╝ ╚████╔╝ ██║   ██║██║     ██║   ██║██║  ███╗  
██║     ██╔══██╗  ╚██╔╝  ██║   ██║██║     ██║   ██║██║   ██║  
╚██████╗██║  ██║   ██║   ╚██████╔╝███████╗╚██████╔╝╚██████╔╝  
 ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝
```                                                           
                                                                                         
# What is CRYOLOG? ❄️
> CryoLog is a smart, intuitive, and integrated grocery list application powered by the Snowflake Arctic LLM.   
> CryoLog will help users:
> * Streamline Grocery List Creation: Generate and update grocery lists based on user preferences, past purchases, and current inventory, reducing the time and effort needed to manually compile lists.
> * Personalize Recommendations: Offer personalized product recommendations and substitutions that align with users' dietary restrictions, health goals, and taste preferences, ensuring a more tailored shopping experience.
> * Increase Nutritional Awareness: Provide detailed ingredient lists and nutritional information for all recommended products, enabling users to make healthier choices and better understand what they are consuming.  

# Why did we build CRYOLOG? 🛒
> In today's fast-paced world, managing grocery shopping efficiently can be a significant challenge for individuals and families. Traditional grocery lists are often cumbersome, easily forgotten, or incomplete. This leads to multiple trips to the store, wasted time, and increased stress. Additionally, with the plethora of dietary needs, preferences, and ever-changing product availability, maintaining an accurate and personalized grocery list becomes even more complex.  

> Moreover, many consumers are often unaware of the ingredients in the products they buy or neglect the nutritional value of their purchases, leading to poor dietary choices and potential health issues. The lack of easily accessible nutritional information exacerbates the difficulty of making informed decisions that align with personal health goals and dietary restrictions.  

# How did we build CRYOLOG? 🛠️
> ## Frontend
> The frontend was mainly reliant on Streamlit, and written pretty much exclusively in Python. Many of the libraries used were to work around the restrictions streamlit has around customizability.  
> The general user experience/story would go as follows:  
### User Experience  
```
Arrive at Landing page (Mission Statement Blurb)
Create Account/Login  
├─── Input health conditions, personal food preferences, biometrics, and goal  
├─── Access rest of app  
│   ├─── Scan items for additional nutritional information and ingredient descriptions  
│   ├─── Edit shopping list, browse through additional nutritional information  
│   └─── Interact with chat bots, personalize lists and recieve recommendations  
```
### Library Usage  
> `streamlit_cookies_controller` - used to save user login states as well as current tabs, as streamlit session states erase those on page refresh  
> `streamlit_on-Hover-tabs` - provides a more fluid user experience with the tabs, as the user would be moving between them often  
> `streamlit-extras` - provides more CSS styling freedoms when it comes to containers  
> `plotly` - creates an interactable pie chart, which is not native to streamlit  

### Library Structure  
```
StreamLit
├───streamlit_cookies_controller
│   └───streamlit-on-Hover-tabs
├───streamlit-extras
├───streamlit_tags
├───plotly
```
## Backend
## LLM

# Obstacles faced 🚧



# What does the future look like? 🔮



# CLosing Statements 👋
