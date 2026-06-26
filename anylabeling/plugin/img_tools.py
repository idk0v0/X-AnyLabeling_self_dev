import cv2
import numpy as np
from pathlib import Path
from anylabeling.views.labeling.logger import logger, error_deal
from typing import Optional

def img_read_safe(imgpath:str or Path,read_mode:int=cv2.IMREAD_COLOR)->np.ndarray:
    '''
    根据单个文件路径安全导入图片
    Args:
        imgpath: 文件路径
    Returns: img:np.ndarray
    '''
    if Path(imgpath).is_file():
        try:
            img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), read_mode)
            return img
        except Exception as e:
            error_deal(e)
    else:
        e = FileNotFoundError(f"img not found:{imgpath} or input dir")
        logger.error(e)
        raise e

def img_write_safe(img:np.ndarray,save_img_path:str or Path,quantity:int=95,img_extension:str=".jpg")-> Optional[bool]:
    '''
    安全写图片，可处理中文字符
    Args:
        img: 输入的单个图片的np对象
        save_img_path: 图片保存的路径
        quantity: 输出图片质量，支持jpg,默认95
    Returns:
        是否成功
    '''
    try:

        save_img_path = Path(save_img_path) if isinstance(save_img_path,str) else save_img_path
        save_img_path.parent.mkdir(parents=True, exist_ok=True)
        if not save_img_path.suffix:
            save_img_path = Path(save_img_path.parent) / f'{save_img_path.stem}{img_extension}'
        cv2.imencode(img_extension, img, [int(cv2.IMWRITE_JPEG_QUALITY), quantity])[1].tofile(save_img_path)
        return True
    except Exception as e:
        error_deal(e)
        return False