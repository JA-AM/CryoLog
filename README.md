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
├───Input health conditions, personal food preferences, biometrics, and goal  
├───Access rest of app  
│   ├───Scan items for additional nutritional information and ingredient descriptions  
│   ├───Edit shopping list, browse through additional nutritional information  
│   └───Interact with chat bots, personalize lists and recieve recommendations  
```
### Library Usage  
> `streamlit_cookies_controller` - used to save user login states as well as current tabs, as streamlit session states erase those on page refresh  
> `streamlit_on-Hover-tabs` - provides a more fluid user experience with the tabs, as the user would be moving between them often
> `streamlit_webrtc` - integrate user camera with streamlit, as native streamlit is used for picture, not video  
> `streamlit-extras` - provides more CSS styling freedoms when it comes to containers  
> `plotly` - creates an interactable pie chart, which is not native to streamlit  

### Library Structure  
```
StreamLit
├───streamlit_cookies_controller
│   └───streamlit-on-Hover-tabs
├───streamlit_webrtc
├───streamlit-extras
├───streamlit_tags
├───plotly
```
## Backend
### Login and Authentication
>Authentication is implemented using Firebase, allowing users to manage their data with an email and password. Additionally, OAuth 2.0 is integrated to enable Google account sign-ins. This combination ensures a secure and user-friendly authentication process.

### Barcode Scanner
>A key feature of this project is the barcode scanner, which enables users to interact directly with their products. We used the `streamlit-webrtc` component to stream video in the Streamlit Community Cloud. Image frames are processed with OpenCV and Pyzbar to decode barcodes, with scanned items displayed after the streaming stops.

### FoodData API
>We use the FoodData Central API to generate list items, providing detailed nutritional information and more. The GET search endpoint retrieves initial product data, while the GET endpoint with the FDC ID fetches comprehensive details for each item.

## LLM Integration
>### Snowflake Cortex
>We chose Snowflake Cortex for accessing the Snowflake Arctic LLM due to its functionality and compatibility with RAG. Cortex offers multiple LLM functions and integrates well with the Snowflake Client, facilitating direct use of the Snowflake database.

### Retrieval-Augmented Generation (RAG)
>RAG is used to enhance LLM responses using our dataset, improving accuracy without tuning model weights. 

**Setup:**
> 1. Create database and schema in Snowflake.
> 2. Organize private documents.
> 3. Create preprocessing functions.
> 4. Build the vector database.

**Documents:**
> - Nutritional information from USAID
> - Dietary Guidelines 2010
> - Ingredients information from WebMD (scraped)

### Usage
>The LLM is used in three main ways:
>1. **Nutritional and dietary advice**: Generates advice based on user biometric data and contextual information.
>2. **Ingredient information overviews**: Provides simplified overviews using SQL search results.
>3. **Grocery lists and alternatives**: Generates lists or alternatives by integrating Snowflake Arctic with the FoodData API through multi-step processing.

**List Generation Process:**
>- **Prompt 1**: Generates a list of query searches based on user info and prompt question.
>- **FoodData API**: Executes queries and returns relevant product information.
>- **Prompt 2**: Selects the best options based on user info and extracted data.

# Obstacles faced 🚧
> * Streamlit's high-level programming prevented a lot of customizability when it came down to stylization
> * The lack of a native implementation of a camera streaming component led to a search of the custom component `streamlit-webrtc` which was not functional at first. It took many hours of debugging and reading forums to figure out that Streamlit version 1.33 with an external server made the component work for us.
> * On deployment we had many troubles with Google authentication, and we struggled to figure out why it worked locally but not on the cloud. We eventually switched to a different component for Google authentication which solved the issue.

# Impacts 💥
> CryoLog has the potential to go beyond a demo app created for a one-off hackathon. The real-world impacts may include:

> ## User Engagement and Retention
> **Enhanced User Experience**: With streamlined barcode scanning, personalized nutritional advice, and dynamic grocery list generation, users will likely find the app highly useful, leading to increased engagement and retention.
> **Health Benefits**: By providing personalized dietary advice and product information, the app can positively impact users' health and wellness, potentially leading to broader adoption.
> ## Market Opportunities
> **Healthcare and Wellness**: The app can be marketed to healthcare providers, dietitians, and fitness coaches who can use it to provide personalized dietary recommendations to their clients.
> **Retail Integration**: Grocery stores and online food retailers could integrate the app to offer personalized shopping experiences and improve customer satisfaction.
> ## Data Insights
> **Nutritional Trends**: Aggregated data from user interactions can provide valuable insights into dietary trends, preferences, and nutritional gaps, which can be used for research and development.
> **Consumer Behavior**: Understanding consumer behavior through detailed analytics can help improve product offerings and marketing strategies for food brands and retailers.


# What does the future look like? 🔮
> ## Scalability and Performance
> **Robust Infrastructure**: Implementing auto-scaling, load balancing, and efficient resource management to handle large numbers of concurrent users.
> **Optimized Backend**: Ensuring that backend services, especially those handling heavy computation like LLM and OpenCV processing, are optimized and capable of horizontal scaling.

> ## Security and Compliance
> **Data Security**: Implementing robust security measures to protect user data, including encryption, secure authentication, and regular security audits.
> **Compliance**: Ensuring compliance with relevant regulations such as GDPR, HIPAA (if dealing with health data), and other data protection laws.

> ## User Management
> **Authentication and Authorization**: Implementing a secure and scalable authentication system, potentially extending beyond Firebase to support enterprise-level requirements.
> **User Data Segmentation**: Ensuring that user data is properly segmented and isolated to prevent data breaches and enhance privacy.

> ## API and Third-Party Integration
> **Reliable API Integration**: Ensuring that integrations with external APIs like FoodData Central are reliable, with proper error handling and rate limiting.
> **Custom Components**: Maintaining and updating custom Streamlit components to ensure compatibility and performance.

> ## Operational Monitoring
> **Logging and Monitoring**: Implementing comprehensive logging and monitoring to track application performance, detect issues early, and enable quick troubleshooting.
> **Automated Testing**: Setting up automated testing pipelines to ensure code quality and reliability with each deployment.

> ## User Support and Feedback
> **Support Infrastructure**: Providing user support channels, such as chat support, FAQs, and documentation.
> **Feedback Loop**: Implementing mechanisms to gather user feedback and iteratively improve the application based on user needs and suggestions.

> ## Integration with Wearables
> **Health Data Integration**: Integrate with wearable devices to collect real-time health data, providing more accurate and timely dietary advice.

> ## Social and Community Features
> **Community Forums**: Introduce forums where users can share recipes, dietary tips, and success stories, fostering a supportive community.
> **Social Sharing**: Enable users to share their grocery lists, recipes, and meal plans on social media platforms directly from the app.

> ## Sustainability and Eco-Friendly Options
> **Eco-Friendly Products**: Highlight eco-friendly and sustainable product options, helping users make environmentally conscious choices.
> **Carbon Footprint Tracking**: Provide insights into the carbon footprint of users' dietary choices and suggest ways to reduce it.


# Closing Statements 👋
>We want to emphasize that CryoLog is more than just a grocery list application; it is a comprehensive tool designed to enhance your shopping experience and promote healthier eating habits.

>As we look to the future, we are committed to continuously improving CryoLog, addressing user feedback, and exploring new ways to make the app even more valuable. Whether you are a busy professional, a health-conscious individual, or someone looking to optimize your shopping routine, CryoLog is here to assist you every step of the way.

>Thank you for your interest in CryoLog. We are excited about the journey ahead and hope you will join us in making smart, healthy, and efficient grocery shopping a reality for everyone.

>Happy shopping and stay healthy! 🌟

by JA'AM
