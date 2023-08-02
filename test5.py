from plexapi.myplex import MyPlexAccount
account = MyPlexAccount('jgarza9788@gmail.com', 'GetMoviesBitch')
plex = account.resource('TheBlackPearl').connect()  # returns a PlexServer instance

movies = plex.library.section('Movies')
# for video in movies.search(unwatched=True):
#     print(video.title)
#     print(video)


s = plex.search('Spider')
for i in s:
    try:
        print(
            i.title,
            i.listType,
            i.art
            )
    except:
        pass