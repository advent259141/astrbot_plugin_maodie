import os
import random
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

PLUGIN_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(PLUGIN_DIR, "maodie_img")

@register("astrbot_plugin_maodie", "Jason.Joestar", "发送随机耄耋图片", "1.0.0") #
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.image_files = [] # 初始化图片列表

    async def initialize(self):
        """插件初始化时加载图片列表"""
        try:
            if os.path.isdir(IMAGE_DIR):
                self.image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
                if not self.image_files:
                    logger.warning(f"插件 'maodie': 在 '{IMAGE_DIR}' 文件夹下未找到图片文件。")
                else:
                    logger.info(f"插件 'maodie': 成功加载 {len(self.image_files)} 张图片。")
            else:
                logger.error(f"插件 'maodie': 图片文件夹 '{IMAGE_DIR}' 不存在或不是一个目录。")
        except Exception as e:
            logger.error(f"插件 'maodie': 初始化时加载图片失败: {e}")

    @filter.command("哈个气")
    async def send_maodie_image(self, event: AstrMessageEvent):
        if not self.image_files:
            yield event.plain_result("错误：找不到图片文件。请检查插件文件夹。")
            return

        try:
            random_image_name = random.choice(self.image_files)
            image_path = os.path.join(IMAGE_DIR, random_image_name)

            chain = [
                Comp.Plain("耄耋来咯~"),
                Comp.Image.fromFileSystem(image_path)
            ]
            yield event.chain_result(chain)

        except FileNotFoundError:
            logger.error(f"插件 'maodie': 选择的图片文件 '{image_path}' 未找到。")
            yield event.plain_result("错误：无法找到选定的图片文件。")
        except Exception as e:
            logger.error(f"插件 'maodie': 发送图片时出错: {e}")
            yield event.plain_result("发送图片时发生内部错误。")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
