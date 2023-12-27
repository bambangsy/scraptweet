from scrap import TweetScrap

title = "climate change"
from_date = "2022-01-22"
to_date = "2022-01-28"
limit_time = 10


tweet = TweetScrap(title,from_date,to_date,limit_time)
tweet.main()

