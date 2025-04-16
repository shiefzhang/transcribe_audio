# Whisper 中文语音转文本工具

Windows环境下使用Python实现的异步语音转文本工具，基于OpenAI Whisper模型

## 功能特点

- **模型本地缓存**：自动下载并缓存模型到项目目录下的`.whisper_models`子目录
- **命令行操作**：直接通过参数指定音频文件
- **异步处理**：使用asyncio实现非阻塞转录
- **实时进度**：显示转录进度百分比
- **中文优化**：自动添加中文标点符号
- **大文件支持**：自动分块处理大音频文件

## 安装步骤

1. 安装Python 3.7+ (勾选"Add Python to PATH")
2. 安装FFmpeg:
   - 下载地址: https://ffmpeg.org/download.html
   - 解压后添加bin目录到系统PATH
3. 安装依赖:
   ```cmd
   pip install -r requirements.txt
   ```

## 使用方法

### 基本用法
```cmd
python transcribe_audio.py 音频文件路径
```

### 模型管理
- 首次使用会自动下载模型到当前目录下的`.whisper_models`目录
- 后续使用会自动复用已下载模型
- 模型文件会随项目一起保存

## 输出结果
转录结果将保存为同目录下的`[文件名]_transcript.txt`文件

## 常见问题

1. **模型下载慢**:
   - 可手动下载模型放入`.whisper_models`目录
   - 模型下载地址: https://huggingface.co/openai/whisper-{model}

2. **FFmpeg未安装**:
   - 错误信息: "FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'"
   - 解决方案: 按上述步骤安装FFmpeg并配置PATH

3. **中文标点不准确**:
   - 修改transcribe_audio.py中的initial_prompt参数
   - 示例: "这是一段正式的中文语音转写，请使用规范的中文标点符号，包括逗号、句号、问号等。"

