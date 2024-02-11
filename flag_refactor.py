from collections import deque
from typing import Any, Generator, Optional
import cv2
import numpy as np
import itertools
from ultralytics import YOLO
from var_dump import var_dump


def phash(img):
    # 加载并调整图片为32x32灰度图片
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(np.float32)
    # 离散余弦变换
    img = cv2.dct(img)
    hash_str = ""
    img = img[0:8, 0:8]
    avg = sum(img[i, j] for i, j in itertools.product(range(8), range(8)))
    avg = avg / 64
    # 获得hsah
    for i, j in itertools.product(range(8), range(8)):
        hash_str = f"{hash_str}1" if img[i, j] > avg else f"{hash_str}0"
    return hash_str


def hamming_distance(str1, str2):
    """计算汉明距离"""
    if len(str1) != len(str2):
        return 0
    return sum(str1[i] != str2[i] for i in range(len(str1)))


def index_to_timecode(framerate: float, frameIndex: int) -> str:
    """帧序号转换为时间\n\n framerate: 视频帧率\n\n frames: 当前帧序号\n\n return:时间（00:00:01.01）"""
    frameIndex -= 1
    return "{0:02d}:{1:02d}:{2:02d}.{3:02d}".format(
        int(frameIndex / (3600 * framerate)),
        int(frameIndex / (60 * framerate) % 60),
        int(frameIndex / framerate % 60),
        int(frameIndex / framerate % 1 * 100),
    )


class SubtitleVideo:
    def __init__(self, local_video_path) -> None:
        self.videoPath = local_video_path
        self._init_video()
        self.tempHashDeque: deque[str] = deque(maxlen=2)
        self.tempHashDeque.append("")
        self.tempFrameIndex = 1
        self.subtitleList: list[tuple[int, int]] = []
        self.verifiedSubtitleList: list[tuple[int, int]] = []

    def _init_video(self) -> None:
        self.videoInstance = cv2.VideoCapture(self.videoPath)
        assert self.videoInstance.isOpened(), "Video file not opened!"
        self.frameRate = round(self.videoInstance.get(5), 2)

    def _init_model(self) -> None:
        self.model = YOLO('best.pt')
        self.classDict = self.model.names

    def read_frames(self) -> Generator[tuple[int, Any], None, None]:
        while self.videoInstance.isOpened():
            success, frame = self.videoInstance.read()
            if not success:
                break
            yield int(self.videoInstance.get(1)), frame

    def _update_index(self, index: int) -> None:
        self.tempFrameIndex = index

    def seek(self) -> None:
        for index, frame in video.read_frames():
            self.tempHashDeque.append(phash(frame[950:1045, 810:910]))
            hammingDistance = hamming_distance(self.tempHashDeque[0], self.tempHashDeque[1])
            if hammingDistance > 13:
                if (index - self.tempFrameIndex) > (self.frameRate / 2):
                    print(self.tempFrameIndex, index)
                    self.subtitleList.append((self.tempFrameIndex, index))
                    if len(self.subtitleList) > 13:
                        break
                self._update_index(index)

    def get_specific_frame(self, frame_index: int) -> Any:
        self.videoInstance.set(1, frame_index)
        _, frame = self.videoInstance.read()
        return frame

    def save(self) -> None:
        with open("Temp\\subtitle.srt", "w") as f:
            f.writelines(
                f"Dialogue: 1,{index_to_timecode(video.frameRate, start)},{index_to_timecode(video.frameRate, end)},路人男#1,mobuo,0,0,0,,示范性字幕{i}\n"
                for i, (start, end) in enumerate(self.subtitleList)
            )

    def valSubtiele(self, subtitles: tuple[tuple[int, int]]) -> tuple[bool, Optional[str]]: #type: ignore
        frames = [self.get_specific_frame(np.mean(each_subtitle, dtype=int))[900:1100, 0:1920] for each_subtitle in subtitles]
        result = self.model.predict(frames, stream=True)
        for r in result:
            var_dump(r)


video = SubtitleVideo("Temp\\test.webm")
video.seek()
# video.valSubtiele(video.subtitleList[:10]) #type: ignore

# from var_dump import var_dump
# var_dump(video.subtitleList)
# video.save()



# # classDict = model.names
# # Read an image using OpenCV
# source = video.get_specific_frame(8000)[900:1100, 0:1920]

# # Run inference on the source
# results = model.predict(source, stream=True)

# from var_dump import var_dump


# for r in results:
#     cv2.imshow("YOLOv8 Inference", r.plot())
#     cv2.waitKey(-1)
#     # print(r.boxes.cls)
#     var_dump(r.names[int(r.boxes.cls[0])])
#     # print(r.boxes)
#     # for box in r.boxes:
#     #     print(box.cls, box.xywhn, box.conf)
        
# # print(results)

