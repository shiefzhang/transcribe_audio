import asyncio
import whisper
from whisper.utils import get_writer
from typing import Optional, Callable
import os
from tqdm import tqdm
import sys
import argparse
from pathlib import Path

# 模型缓存目录(当前目录下的.whisper_models)
MODEL_CACHE_DIR = os.path.join(os.path.dirname(__file__), ".whisper_models")

class AsyncWhisperTranscriber:
    def __init__(self, model_name: str = "base", device: str = "cpu"):
        """初始化Whisper转录器"""
        # 创建模型缓存目录
        os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
        
        # 检查本地是否有缓存模型
        model_path = os.path.join(MODEL_CACHE_DIR, f"{model_name}.pt")
        if os.path.exists(model_path):
            print(f"使用本地缓存模型: {model_path}")
            self.model = whisper.load_model(model_path, device=device)
        else:
            print(f"下载模型 {model_name} 到本地缓存...")
            self.model = whisper.load_model(model_name, download_root=MODEL_CACHE_DIR, device=device)
            print(f"模型已保存到: {model_path}")
        
        self.model_name = model_name
        
    async def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = "zh",
        initial_prompt: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        chunk_size: int = 30 * 16000  # 30秒音频片段(16kHz)
    ) -> str:
        """异步转录音频文件"""
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"音频文件不存在: {audio_path}")
                
            print(f"正在加载音频文件: {audio_path}")
            audio = whisper.load_audio(audio_path)
            total_samples = len(audio)
            chunks = [
                audio[i : i + chunk_size]
                for i in range(0, total_samples, chunk_size)
            ]
            
            results = []
            with tqdm(total=len(chunks), desc="处理进度", unit="chunk") as pbar:
                for i, chunk in enumerate(chunks):
                    result = await asyncio.to_thread(
                        self.model.transcribe,
                        chunk,
                        language=language,
                        initial_prompt=initial_prompt or "这是一段正式的中文语音转写，请使用规范的中文标点符号，包括逗号、句号、问号等。",
                    )
                    results.append(result["text"])
                    
                    if progress_callback:
                        progress = (i + 1) / len(chunks)
                        progress_callback(progress)
                    pbar.update(1)
            
            return "".join(results)
        except Exception as e:
            print(f"转录失败: {e}", file=sys.stderr)
            raise

async def main(audio_file: str):
    """主函数"""
    print("=== Whisper中文语音转录 ===")
    transcriber = AsyncWhisperTranscriber(model_name="medium")
    
    def progress_callback(progress: float):
        print(f"\r当前进度: {progress:.1%}", end="", flush=True)
    
    print("\n开始转录...")
    result = await transcriber.transcribe(
        audio_file,
        language="zh",
        progress_callback=progress_callback
    )
    
    #print("\n\n转录结果:")
    #print(result)
    
    output_file = os.path.splitext(audio_file)[0] + "_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\n结果已保存到: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whisper中文语音转录工具")
    parser.add_argument("audio_file", help="要转录的音频文件路径")
    args = parser.parse_args()
    
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main(args.audio_file))