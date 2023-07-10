import requests
import os

# Get the latest version of UPX from GitHub
apiURL = "https://api.github.com/repos/upx/upx/releases/latest"

for _ in range(5):
    try:
        req = requests.get(apiURL)
        latestDownloadURL = [each['browser_download_url'] for each in req.json()['assets'] if 'win64' in each['name']][0]
        print(f'Latest UPX download URL: {latestDownloadURL}')
        break
    except KeyError:
        continue
else:
    print('Use old UPX download URL instead.')
    latestDownloadURL = 'https://github.com/upx/upx/releases/download/v4.0.2/upx-4.0.2-win64.zip'

os.system(f'certutil -urlcache -split -f {latestDownloadURL} upx.zip')