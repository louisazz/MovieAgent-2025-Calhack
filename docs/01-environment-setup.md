# 01-环境搭建与依赖安装

## 概述

本文档将指导您完成VideoAgent项目的环境搭建和依赖安装。我们将从基础环境开始，逐步安装所有必要的依赖包和工具。

## 前置要求

### 系统要求
- **操作系统**：Linux (推荐 Ubuntu 20.04+) 或 Windows 10+
- **Python版本**：3.10+ (必须)
- **GPU内存**：8GB+ (推荐，用于深度学习模型)
- **存储空间**：50GB+ (用于模型文件和依赖包)
- **网络环境**：稳定的网络连接

### 硬件要求
- **CPU**：4核心以上
- **内存**：16GB+ (推荐32GB)
- **显卡**：NVIDIA GPU (支持CUDA 11.8+)

## 步骤1：基础环境准备

### 1.1 安装Python 3.10

**Linux (Ubuntu/Debian):**
```bash
# 添加Python 3.10源
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# 安装Python 3.10
sudo apt install python3.10 python3.10-venv python3.10-dev

# 验证安装
python3.10 --version
```

**Windows:**
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.10.x版本
3. 安装时勾选"Add Python to PATH"

### 1.2 安装Conda (推荐)

**下载并安装Miniconda:**
```bash
# Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Windows
# 下载Miniconda3-latest-Windows-x86_64.exe并安装
```

**验证安装:**
```bash
conda --version
```

### 1.3 创建虚拟环境

```bash
# 创建VideoAgent专用环境
conda create --name videoagent python=3.10

# 激活环境
conda activate videoagent

# 验证环境
python --version
which python
```

## 步骤2：系统依赖安装

### 2.1 安装FFmpeg

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
1. 下载FFmpeg: https://ffmpeg.org/download.html
2. 解压到C:\ffmpeg
3. 添加C:\ffmpeg\bin到系统PATH

### 2.2 安装Git LFS

```bash
# Linux
sudo apt install git-lfs

# Windows
# 下载并安装: https://git-lfs.github.io/

# 初始化
git lfs install
```

### 2.3 安装CUDA (GPU用户)

**检查GPU:**
```bash
nvidia-smi
```

**安装CUDA 11.8:**
```bash
# 下载CUDA 11.8
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run

# 安装
sudo sh cuda_11.8.0_520.61.05_linux.run
```

## 步骤3：Python依赖安装

### 3.1 基础依赖

```bash
# 激活环境
conda activate videoagent

# 安装基础包
conda install -y -c conda-forge pynini==2.1.5 ffmpeg

# 安装PyTorch (GPU版本)
pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

### 3.2 项目依赖安装

```bash
# 克隆项目
git clone https://github.com/HKUDS/VideoAgent.git
cd VideoAgent

# 安装项目依赖
pip install -r requirements.txt

# 或者使用pyproject.toml
pip install -e .
```

### 3.3 验证安装

**创建测试脚本 `test_installation.py`:**
```python
import sys
import torch
import numpy as np
import librosa
import moviepy
import transformers

def test_installation():
    print("Python版本:", sys.version)
    print("PyTorch版本:", torch.__version__)
    print("CUDA可用:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU数量:", torch.cuda.device_count())
        print("GPU名称:", torch.cuda.get_device_name(0))
    
    print("NumPy版本:", np.__version__)
    print("Librosa版本:", librosa.__version__)
    print("MoviePy版本:", moviepy.__version__)
    print("Transformers版本:", transformers.__version__)
    
    print("✅ 所有依赖安装成功!")

if __name__ == "__main__":
    test_installation()
```

**运行测试:**
```bash
python test_installation.py
```

## 步骤4：模型文件下载

### 4.1 安装Hugging Face CLI

```bash
pip install huggingface-hub
```

### 4.2 下载核心模型

**CosyVoice模型:**
```bash
cd tools/CosyVoice
huggingface-cli download PillowTa1k/CosyVoice --local-dir pretrained_models
```

**Fish Speech模型:**
```bash
cd tools/fish-speech
huggingface-cli download fishaudio/fish-speech-1.5 --local-dir checkpoints/fish-speech-1.5
```

**Seed-VC模型:**
```bash
cd tools/seed-vc
huggingface-cli download PillowTa1k/seed-vc --local-dir checkpoints
```

**DiffSinger模型:**
```bash
cd tools/DiffSinger
huggingface-cli download PillowTa1k/DiffSinger --local-dir checkpoints
```

**Whisper模型:**
```bash
cd tools
huggingface-cli download openai/whisper-large-v3-turbo --local-dir whisper-large-v3-turbo
```

**ImageBind模型:**
```bash
cd tools
mkdir .checkpoints
cd .checkpoints
wget https://dl.fbaipublicfiles.com/imagebind/imagebind_huge.pth
```

## 步骤5：API配置

### 5.1 创建配置文件

编辑 `environment/config/config.yml`:

```yaml
llm:
  # Video Remixing/TTS/SVC/Stand-up/CrossTalk
  deepseek_api_key: "your_deepseek_api_key"
  deepseek_base_url: "https://api.deepseek.com"
  
  # Agentic Graph Router/TTS/SVC/Stand-up/CrossTalk
  claude_api_key: "your_claude_api_key"
  claude_base_url: "https://api.anthropic.com"
  
  # Video Editing/Overview/Summarization/QA/Commentary Video
  gpt_api_key: "your_openai_api_key"
  gpt_base_url: "https://api.openai.com"
  
  # MLLM for caption and fine-grained video understanding
  gemini_api_key: "your_gemini_api_key"
  gemini_base_url: "https://generativelanguage.googleapis.com"
```

### 5.2 获取API密钥

1. **OpenAI API**: https://platform.openai.com/api-keys
2. **Anthropic Claude API**: https://console.anthropic.com/
3. **DeepSeek API**: https://platform.deepseek.com/
4. **Google Gemini API**: https://makersuite.google.com/app/apikey

## 步骤6：环境验证

### 6.1 基础功能测试

**创建 `test_basic_functionality.py`:**
```python
import os
import sys
sys.path.append('.')

def test_imports():
    """测试核心模块导入"""
    try:
        from environment.agents.multi import MultiAgent
        from environment.agents.base import FunctionRegistry
        print("✅ 核心模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config_loading():
    """测试配置文件加载"""
    try:
        import yaml
        with open('environment/config/config.yml', 'r') as f:
            config = yaml.safe_load(f)
        print("✅ 配置文件加载成功")
        return True
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return False

def test_model_paths():
    """测试模型文件路径"""
    model_paths = [
        'tools/CosyVoice/pretrained_models',
        'tools/fish-speech/checkpoints',
        'tools/seed-vc/checkpoints',
        'tools/DiffSinger/checkpoints',
        'tools/whisper-large-v3-turbo',
        'tools/.checkpoints/imagebind_huge.pth'
    ]
    
    missing_paths = []
    for path in model_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ 缺少模型文件: {missing_paths}")
        return False
    else:
        print("✅ 所有模型文件存在")
        return True

if __name__ == "__main__":
    print("开始环境验证...")
    
    tests = [
        test_imports,
        test_config_loading,
        test_model_paths
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n测试结果: {passed}/{len(tests)} 通过")
    if passed == len(tests):
        print("🎉 环境搭建完成!")
    else:
        print("⚠️ 请检查失败的测试项")
```

### 6.2 运行基础测试

```bash
python test_basic_functionality.py
```

## 步骤7：启动项目

### 7.1 首次运行

```bash
# 激活环境
conda activate videoagent

# 进入项目目录
cd VideoAgent

# 运行主程序
python main.py
```

### 7.2 预期输出

如果环境搭建成功，您应该看到：
```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                     ║
║  ██╗   ██╗██╗██████╗ ███████╗ ██████╗  █████╗  ██████╗ ███████╗███╗   ██╗████████╗  ║
║  ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝  ║
║  ██║   ██║██║██║  ██║█████╗  ██║   ██║███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║     ║
║  ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║     ║
║   ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║     ║
║    ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝     ║
║                                                                                     ║
║                         🎬 Open Agentic Video Intelligence 🤖                       ║
║                                                                                     ║
╚═════════════════════════════════════════════════════════════════════════════════════╝

🎉 Welcome to VideoAgent - Open Agentic Video Intelligence!

User Requirement:
```

## 故障排除

### 常见问题及解决方案

**1. CUDA相关错误**
```bash
# 检查CUDA版本
nvcc --version

# 重新安装PyTorch
pip uninstall torch torchaudio
pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

**2. 模型下载失败**
```bash
# 使用代理下载
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download model_name
```

**3. 依赖冲突**
```bash
# 创建全新环境
conda create --name videoagent_new python=3.10
conda activate videoagent_new
pip install -r requirements.txt
```

**4. 权限问题**
```bash
# Linux权限修复
sudo chown -R $USER:$USER ~/.cache
sudo chown -R $USER:$USER ~/.local
```

## 下一步

环境搭建完成后，请继续阅读：
- [02-项目结构分析](./02-project-structure.md)
- [03-多智能体框架](./03-multi-agent-framework.md)

## 测试验证

完成环境搭建后，请运行以下测试确保一切正常：

1. **基础功能测试**: `python test_basic_functionality.py`
2. **GPU测试**: 检查CUDA是否可用
3. **模型加载测试**: 验证所有模型文件存在
4. **API连接测试**: 测试LLM API连接

如果所有测试通过，说明环境搭建成功！🎉
