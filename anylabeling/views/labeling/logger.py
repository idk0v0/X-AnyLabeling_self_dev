import traceback

from loguru import logger
from typing import List
from pathlib import Path
import yaml,os


log_config_path = Path("configs/logger_config.yaml").resolve()
level:str = ''
show_cmd:bool = True
default_log_path = Path("logs/label_x.log").resolve()

if os.path.exists(log_config_path):
    try:
        with open(log_config_path, mode='r+', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            level = data['level']
            show_cmd = data['show_in_cmd']
    except Exception as e:
        raise ValueError(f"some error happen: {e}")
else:
    raise FileNotFoundError(f"not found file: {log_config_path},please check your config file path")
# 内存缓存，用于保存日志记录
log_buffer: List[dict] = []

# 移除默认控制台输出
logger.remove()

# 内存 sink：捕获 LogRecord
def memory_sink(message):
    record = message.record
    log_buffer.append({
        "time": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "level": record["level"].name,
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "message": record["message"]
    })

# 添加内存 sink（最低 INFO 级别）
memory_handler_id = logger.add(memory_sink, level="INFO" if level == '' else level)

# 可选：保留控制台打印
if show_cmd:
    console_handler_id = logger.add(lambda msg: print(msg, end=""), colorize=True)

def dump_logs_to_file(filepath="logs/runtime.log",mode_str:str='a'):
    """
    将内存中的日志一次性写入文件，并保持原等级
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # 直接写入文件
    with open(filepath, mode=mode_str, encoding="utf-8") as f:
        for record in log_buffer:
            f.write(f"{record['time']} | {record['level']} | "
                    f"{record['module']}:{record['function']}:{record['line']} -- 【{record['message']}】\n")

    # 清空内存缓存
    log_buffer.clear()



def error_deal(e,log_path:str or Path=None):
    logger.error(f'error:{e}, detail:\n{traceback.format_exc()}')
    if log_path and Path(log_path).is_file():
        dump_logs_to_file(filepath=log_path, mode_str='a')
    return e


if __name__ == '__main__':
    logger.info('test')
    dump_logs_to_file(mode_str='w+')


