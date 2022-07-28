from apiclient.discovery import build
import json, yaml
import datetime
from dateutil.relativedelta import relativedelta
import isodate


def video_length(video_id):
    '''
    video_idから動画の長さを秒に変換してリターンする
    '''
    content_details = youtube.videos().list(
        part='contentDetails',
        id=video_id
    ).execute()

    duration = isodate.parse_duration(content_details['items'][0]['contentDetails']['duration'])
    return duration.seconds


def youtube_search(page_token, st, ed):
    '''
    期間内のぽんぽこちゃんねるの動画情報を保管する
    '''
    search_response = youtube.search().list(
        channelId='UC1EB8moGYdkoZQfWHjh7Ivw',
        part='snippet',
        maxResults=50,
        publishedAfter=st,
        publishedBefore=ed,
        pageToken=page_token,
        type="video"
    ).execute()

    for search_result in search_response.get("items", []):

        title = search_result["snippet"]["title"]
        video_id = search_result["id"]["videoId"]
        duration = video_length(video_id)

        d = {
            'videoId': video_id,
            'title':title,
            'url':'https://youtu.be/%s' % video_id,
            'duration': int(duration)
            }

        database.append(d)

    try:
        next_page_token = search_response["nextPageToken"]
        print(next_page_token)
        youtube_search(next_page_token)
    except:
        return



if __name__ == '__main__':

    with open("./apikeys.yml") as f:
        conf = yaml.safe_load(f)

    youtube = build('youtube', 'v3', developerKey=conf["YOUTUBE_API_KEY"])

    database = []

    #開始日
    dt = datetime.datetime(2018, 1, 1, 0, 0)

    #開始日から何ヶ月後まで取得するか
    month_num = 56

    for i in range(1, month_num):
        #print(dt.isoformat())
        youtube_search('', dt.isoformat()+'Z', (dt+relativedelta(months=1)).isoformat()+'Z')
        dt = dt + relativedelta(months=1)

    with open("response.json", mode="w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)


