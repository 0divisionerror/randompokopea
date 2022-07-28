
import yaml, json
import random
from requests_oauthlib import OAuth1Session
from settings import DATABASE_PATH, MAX_LENGTH
from imageGenerator import ImageGenerator

def main():
    #データベースからもってくる
    with open(DATABASE_PATH, 'r') as f:
        json_load = json.load(f)

    #指定の長さ未満の動画をランダムに選ぶ
    while True:
        val = random.choice(json_load)
        if MAX_LENGTH > val['duration']:
            break

    #それぞれのデータをひっぱる
    title = val['title']
    url = val['url']
    duration = val['duration']

    #とってくる場所をランダムに選ぶ
    moment = random.randint(1, duration - 1)

    #とってきた場所にURLから飛べるようにする
    url = url + "?t=" + str(moment)

    
    #ランダムに選ばれた動画から1フレームだけ画像にして保存する
    img = ImageGenerator(url, moment)
    img.save_frame()


    #TwitterのKEYを準備する
    with open("./apikeys.yml") as f:
        conf = yaml.safe_load(f)

    #リクエストのURL準備
    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
    update_url = "https://api.twitter.com/1.1/statuses/update.json"

    twitter = OAuth1Session(conf["CK"], conf["CS"],conf["AT"],conf["AS"])

    #画像をアップロード
    files = {"media" : open('./tmp/image.jpg', 'rb')}
    req_media = twitter.post(upload_url, files = files)
    
    #失敗したらエラー吐く
    if req_media.status_code != 200:
        print("Media upload error.")
        print(req_media)
        return
    
    #アップしたメディアのIDを保管
    media_id = json.loads(req_media.text)['media_id']
    #print ("Media ID: %d" % media_id)

    #ツイートする文章を準備
    text = title + " " + url

    params = {'status':text, 'media_ids': [media_id]}
    req_tweet = twitter.post(update_url, params = params)
    #失敗したらエラー吐く
    if req_tweet.status_code != 200:
        print("Tweet error.")
        print(req_tweet)
        return



main()
