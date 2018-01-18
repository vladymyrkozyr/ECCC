from InstagramAPI import InstagramAPI

API = InstagramAPI("bongthrower_dopesmoker", "Djdfy2000")
API.login()
API.getMediaComments()
print API.LastJson