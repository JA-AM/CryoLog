import extra_streamlit_components as stx
import streamlit as st

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

def main():
    cookie_manager = get_manager()

    st.write("# Cookie Manager")
    st.subheader("All Cookies:")
    cookies = cookie_manager.get_all()
    st.write(cookies)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Get Cookie:")
        cookie = st.text_input("Cookie", key="0")
        clicked = st.button("Get")
        if clicked:
            value = cookie_manager.get(cookie=cookie)
            st.write(value)
    with c2:
        st.subheader("Set Cookie:")
        cookie = st.text_input("Cookie", key="1")
        val = st.text_input("Value")
        if st.button("Add"):
            cookie_manager.set(cookie, val)
    with c3:
        st.subheader("Delete Cookie:")
        cookie = st.text_input("Cookie", key="2")
        if st.button("Delete"):
            cookie_manager.delete(cookie)

if __name__ == "__main__":
    main()