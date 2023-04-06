import parsel
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

for page in range(1, 20):
    url = f'https://movie.douban.com/subject/35613853/comments?start={page*20}&limit=20&status=P&sort=new_score'
    data_html = requests.get(url=url, headers=headers).text
    selector = parsel.Selector(data_html)
    comment_list = selector.css('.comment-item')
    for comment in comment_list:
        short = comment.css('.short::text').get().strip()
        name = comment.css('.comment-info a::text').get().strip()
        time = comment.css('.comment-time::text').get().strip()
        vote_count = comment.css('.votes.vote-count::text').get().strip()
        print(short, name, time, vote_count)
