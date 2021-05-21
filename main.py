import argparse
from scraping import downloader, parse_video, emote_downloader
from client import client_setup

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--vod", help="Twitch VoD ID.", type=int)
    args = parser.parse_args()
    client = client_setup.create_client()
    vod = downloader.get_vod(args.vod, client)
    metadata = downloader.get_vod_metadata(vod)
    chat_df = parse_video.parse_chatlog(vod.comments)
    folder_path = parse_video.save_chatlog(metadata, chat_df)
    emote_downloader.downloader(folder_path)
