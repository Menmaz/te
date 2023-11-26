import requests
from bs4 import BeautifulSoup
import streamlit as st

def get_manga_info(proxy, url):
    results = []
    session = requests.Session()
    session.proxies = proxy
    res = session.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.find('h1').text
    image = soup.find('img', class_='mx-auto lazy')['src']
    list_chapter = soup.find_all(class_="d-flex justify-content-between mb-2 pb-2 border-bottom align-items-center pl-3")
    arr = []
    for chap in reversed(list_chapter):
        link = chap.find('a')['href']
        name = chap.find('a').span.text
        arr.append({'link': link, 'name': name})

    results.append({'title': title, 'cover': image, 'list_chap': arr})
    return results

# Streamlit UI
st.title("Manga Info Getter")

# Input link
manga_link = st.text_input("Nhập đường link manga:")

# Proxy input (optional)
proxy = st.text_input("Nhập đường link proxy (nếu cần):")

# Button to trigger the function
if st.button("Start"):
    if manga_link:
        try:
            # Call the function to get manga info
            manga_info = get_manga_info({'http': proxy} if proxy else None, manga_link)

            # Display the results
            for info in manga_info:
                st.image(info['cover'], caption=info['title'], use_column_width=True)
                st.write(f"**Tiêu đề:** {info['title']}")
                st.write("**Danh sách chương:**")
                for chap in info['list_chap']:
                    st.write(f"- {chap['name']}: {chap['link']}")
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")
    else:
        st.warning("Vui lòng nhập đường link manga.")
