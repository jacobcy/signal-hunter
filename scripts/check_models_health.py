#!/usr/bin/env python3
"""
检查 OpenClaw 配置中所有模型的健康状态
"""
import json
import subprocess
import sys
import os
from typing import Dict, List, Tuple

def get_openclaw_config():
    """读取 OpenClaw 配置文件"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def test_model(model_id: str) -> Tuple[bool, str]:
    """测试单个模型是否可用"""
    try:
        # 使用 openclaw cli 测试模型
        result = subprocess.run([
            'openclaw', 'models', 'test', model_id
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return True, "OK"
        else:
            return False, result.stderr.strip() or result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def list_available_models():
    """列出所有可用的模型"""
    try:
        result = subprocess.run([
            'openclaw', 'models', 'list'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        else:
            print(f"Error listing models: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error running models list: {str(e)}")
        return []

def main():
    print("🔍 检查 OpenClaw 模型健康状态...")
    
    # 获取配置
    config = get_openclaw_config()
    
    # 获取所有可用模型列表
    available_models = list_available_models()
    print(f"\n📋 OpenClaw 中检测到 {len(available_models)} 个模型:")
    for model in available_models:
        print(f"  - {model}")
    
    # 从配置中提取主要使用的模型
    agents_defaults = config.get('agents', {}).get('defaults', {})
    primary_model = agents_defaults.get('model', {}).get('primary')
    fallback_models = agents_defaults.get('model', {}).get('fallbacks', [])
    
    print(f"\n🎯 主要模型: {primary_model}")
    print(f"🔄 回退模型: {fallback_models}")
    
    all_models_to_check = [primary_model] + fallback_models
    
    # 添加配置中定义的所有模型
    providers = config.get('models', {}).get('providers', {})
    for provider_name, provider_config in providers.items():
        if 'models' in provider_config:
            for model_info in provider_config['models']:
                model_id = f"{provider_name}/{model_info['id']}"
                if model_id not in all_models_to_check:
                    all_models_to_check.append(model_id)
    
    print(f"\n🧪 测试 {len(all_models_to_check)} 个模型的连接性:")
    
    results = {}
    for model_id in all_models_to_check:
        if not model_id:  # 跳过空值
            continue
        print(f"  测试 {model_id} ... ", end='', flush=True)
        success, message = test_model(model_id)
        results[model_id] = (success, message)
        if success:
            print("✅ OK")
        else:
            print(f"❌ {message}")
    
    # 总结
    print(f"\n📊 检查结果汇总:")
    working_models = [model for model, (success, _) in results.items() if success]
    failed_models = [model for model, (success, msg) in results.items() if not success]
    
    print(f"  ✅ 正常工作: {len(working_models)} 个")
    for model in working_models:
        print(f"     - {model}")
    
    print(f"  ❌ 连接失败: {len(failed_models)} 个")
    for model in failed_models:
        _, error = results[model]
        print(f"     - {model}: {error}")
    
    # 检查当前活动模型
    print(f"\n🔍 当前会话使用的模型: ", end='')
    try:
        result = subprocess.run(['openclaw', 'session', 'status'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # 查找模型信息
            for line in result.stdout.split('\n'):
                if 'Model:' in line:
                    print(line.strip())
                    break
        else:
            print("无法获取当前会话状态")
    except:
        print("无法获取当前会话状态")
    
    return len(failed_models) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)