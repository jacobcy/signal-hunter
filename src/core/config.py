import os
import yaml
from typing import Dict, Any, List
from loguru import logger

class Config:
    """Signal Hunter 配置管理器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config = {}
        self.load()
    
    def load(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"✅ Loaded config from {self.config_path}")
        except FileNotFoundError:
            logger.warning(f"⚠️ Config file {self.config_path} not found, using defaults")
            self._config = self._get_defaults()
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
            self._config = self._get_defaults()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """默认配置（当 config.yaml 不存在时）"""
        return {
            'telegram': {
                'bot_token': os.getenv("TELEGRAM_BOT_TOKEN"),
                'channel_id': os.getenv("TELEGRAM_CHANNEL_ID"),
                'admin_chat_id': os.getenv("TELEGRAM_CHAT_ID")
            },
            'scheduler': {
                'interval_minutes': 60,
                'first_run_delay_seconds': 10
            },
            'sources': {
                'list': [
                    {'name': 'Vista', 'url': 'https://x.com/vista8', 'platform': 'twitter', 'weight': 1.0},
                    {'name': 'QingQ', 'url': 'https://x.com/QingQ77', 'platform': 'twitter', 'weight': 1.0},
                    {'name': 'Orange', 'url': 'https://x.com/oran_ge', 'platform': 'twitter', 'weight': 1.0},
                    {'name': 'FuSheng', 'url': 'https://x.com/FuSheng_0306', 'platform': 'twitter', 'weight': 1.0}
                ]
            },
            'signal_processing': {
                'blacklist': ['API', 'GUI', 'CLI', 'GPT', 'LLM', 'SDK', 'HTTP', 'WWW'],
                'keywords': {
                    'bullish': ['买入', '看多', '加仓', '突破', '目标价', '起飞', 'buy', 'long', 'moon'],
                    'bearish': ['卖出', '看空', '减仓', '跌破', '止损', '崩盘', 'sell', 'short', 'dump']
                }
            },
            'ai_summary': {
                'enabled': True,
                'provider': 'deepseek',
                'model': 'deepseek-chat',
                'max_tokens': 1000,
                'temperature': 0.7,
                'system_prompt': '你是一个专业的金融情报分析师...'
            },
            'notifications': {
                'resonance_threshold': 2,
                'deduplication_hours': 24
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/bot.log',
                'max_size': '10 MB',
                'backup_count': 7
            },
            'advanced': {
                'http_timeout': 10,
                'database_path': 'memory/signals.db',
                'graceful_shutdown_timeout': 5
            }
        }
    
    # 快捷访问方法
    @property
    def telegram(self) -> Dict[str, Any]:
        return self._config.get('telegram', {})
    
    @property
    def scheduler(self) -> Dict[str, Any]:
        return self._config.get('scheduler', {})
    
    @property
    def sources(self) -> List[Dict[str, Any]]:
        return self._config.get('sources', {}).get('list', [])
    
    @property
    def signal_processing(self) -> Dict[str, Any]:
        return self._config.get('signal_processing', {})
    
    @property
    def ai_summary(self) -> Dict[str, Any]:
        return self._config.get('ai_summary', {})
    
    @property
    def notifications(self) -> Dict[str, Any]:
        return self._config.get('notifications', {})
    
    @property
    def logging(self) -> Dict[str, Any]:
        return self._config.get('logging', {})
    
    @property
    def advanced(self) -> Dict[str, Any]:
        return self._config.get('advanced', {})

# 全局配置实例（单例模式）
config = Config()
