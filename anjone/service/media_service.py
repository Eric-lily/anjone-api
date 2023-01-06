from anjone.common import Response
from anjone.common.Constant import MUSIC_IMAGE_URL, ENTER_FILE_URL, VIDEO_IMAGE_URL
from anjone.models.sqlite.Music import Music
from anjone.models.sqlite.Video import Video


def get_all_music():
    music_list = Music.query.all()
    res = []
    for music in music_list:
        music.preview_image = MUSIC_IMAGE_URL + music.preview_image
        music.resource = ENTER_FILE_URL + music.resource + '?type=audio&'
        res.append(music.to_json())
    return Response.create_success(res)


def get_all_video():
    video_list = Video.query.all()
    res = []
    for video in video_list:
        video.preview_image = VIDEO_IMAGE_URL + video.preview_image
        video.resource = ENTER_FILE_URL + video.resource + '?type=video&'
        res.append(video.to_json())
    return Response.create_success(res)
