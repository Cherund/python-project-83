from bs4 import BeautifulSoup


def get_url_info(url_response):

    soup = BeautifulSoup(url_response.text, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    description_tag = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': h1_tag.text[:255] if h1_tag else '',
        'title': title_tag.text[:255] if title_tag else '',
        'status_code': url_response.status_code,
        'description': (description_tag.get('content', '')[:255]
                        if description_tag else '')
    }
