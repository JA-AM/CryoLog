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
## LLM

# Obstacles faced 🚧
> * Streamlit's high-level programming prevented a lot of customizability when it came down to stylization
> * 


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

Some features that may push the boundaries of CryoLog include:

Integration with Wearables
Health Data Integration: Integrate with wearable devices to collect real-time health data, providing more accurate and timely dietary advice.
Social and Community Features
Community Forums: Introduce forums where users can share recipes, dietary tips, and success stories, fostering a supportive community.
Social Sharing: Enable users to share their grocery lists, recipes, and meal plans on social media platforms directly from the app.
Sustainability and Eco-Friendly Options
Eco-Friendly Products: Highlight eco-friendly and sustainable product options, helping users make environmentally conscious choices.
Carbon Footprint Tracking: Provide insights into the carbon footprint of users' dietary choices and suggest ways to reduce it.


# Closing Statements 👋
