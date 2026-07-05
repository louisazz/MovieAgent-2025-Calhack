import json
from typing import List, Tuple
from PIL import ImageFont
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, 
    concatenate_videoclips
)
from text2voice import generate_voice

class VideoProcessor:
    """视频处理类，负责添加字幕和合成视频"""
    
    def __init__(self, font_settings: dict = None):
        """初始化字体设置"""
        self.default_font_settings = {
            'font': "也字工厂思美人宋体.TTF",
            'font_size': 30,
            'stroke_color': "black",
            'stroke_width': 1,
            'color': "white",
            'method': 'caption',
            'size': None  # 将在处理视频时动态设置
        }
        
        if font_settings:
            self.default_font_settings.update(font_settings)
        
        # 验证字体
        self._verify_font()

    def _verify_font(self):
        """验证字体文件是否存在"""
        try:
            ImageFont.truetype(self.default_font_settings['font'], 24)
            print("✅ 字体验证通过")
        except IOError:
            print(f"❌ 字体文件不存在: {self.default_font_settings['font']}")

    def add_subtitles(
        self, 
        video_path: str, 
        output_path: str, 
        subtitles: List[Tuple[float, float, str, str]],
        audio_output_dir: str = "audio"
    ) -> VideoFileClip:
        """
        为视频添加字幕和语音
        
        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
            subtitles: 字幕列表，格式为(start_time, end_time, text, actor)
            audio_output_dir: 音频文件输出目录
            
        Returns:
            处理后的视频剪辑对象
        """
        # 加载原始视频
        video = VideoFileClip(video_path)
        
        # 更新字体大小设置
        font_settings = self.default_font_settings.copy()
        font_settings['size'] = (int(video.w), int(video.h * 0.1))
        
        video_clips = []
        
        for start, end, text, actor in subtitles:
            print(f"处理字幕: {text}")
            
            # 创建字幕剪辑
            txt_clip = TextClip(
                text=text,
                **font_settings
            ).with_position(("center", "bottom")).with_duration(end - start)
            
            # 获取视频片段
            clip = video.subclip(start, end)
            
            # 生成语音
            audio_path = f"{audio_output_dir}/{actor}.mp3"
            if actor == "志明":
                generate_voice("male", text, audio_path)
            else:
                generate_voice("female", text, audio_path)
            
            # 加载音频并合成
            audio = AudioFileClip(audio_path)
            video_with_subtitle = CompositeVideoClip([clip, txt_clip])
            video_final = video_with_subtitle.with_audio(audio)
            
            video_clips.append(video_final)
        
        # 合并所有片段
        final_video = concatenate_videoclips(video_clips)
        
        # 写入输出文件
        final_video.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac"
        )
        
        return final_video

    @staticmethod
    def combine_videos(
        video_paths: List[str], 
        output_path: str = "final.mp4"
    ) -> VideoFileClip:
        """
        合并多个视频文件
        
        Args:
            video_paths: 视频路径列表
            output_path: 输出文件路径
            
        Returns:
            合并后的视频剪辑对象
        """
        clips = []
        
        for path in video_paths:
            clip = VideoFileClip(path)
            print(f"加载视频 {path}, 是否有音频: {clip.audio is not None}")
            clips.append(clip)
        
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac"
        )
        
        return final_clip

    @staticmethod
    def read_subtitles_from_json(file_path: str) -> List[Tuple]:
        """从JSON文件读取字幕数据"""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data


# 使用示例
if __name__ == "__main__":
    # 初始化视频处理器
    processor = VideoProcessor()
    
    # 示例字幕数据
    sample_subtitles = [
        (0, 3, '是啊，只要和你在一起，我就觉得很幸福。', "志明"),
    ]
    
    # 处理单个视频
    processor.add_subtitles(
        "raw_video/s2s4.mp4", 
        "result_video/s2s4_result.mp4", 
        sample_subtitles
    )
    
    # 生成另一个音频
    generate_voice("female", '你看那边！那些花好漂亮啊！', '春娇.mp3')
    
    # 合并多个视频
    video_paths = []
    for i in range(1, 3):
        for j in range(1, 5):
            video_paths.append(f"result_video/s{i}s{j}_result.mp4")
    
    processor.combine_videos(video_paths, "final.mp4")