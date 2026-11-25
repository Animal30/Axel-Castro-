"""ElevenLabs scribe_v1 con timestamps por palabra: python3 stt.py clip.mp4 out.json"""
import os, sys, subprocess, requests
src, out = sys.argv[1], sys.argv[2]
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vn', '-ac', '1', '-ar', '16000', '/tmp/_stt.mp3'], check=True)
r = requests.post('https://api.elevenlabs.io/v1/speech-to-text', headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY']},
                  files={'file': open('/tmp/_stt.mp3', 'rb')}, data={'model_id': 'scribe_v1', 'language_code': 'spa', 'timestamps_granularity': 'word'}, timeout=120)
r.raise_for_status(); open(out, 'w').write(r.text)
