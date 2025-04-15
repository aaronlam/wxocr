import wcocr
import os
import uuid
import base64
import logging
from flask import Flask, request, jsonify

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
wcocr.init("/app/wx/opt/wechat/wxocr", "/app/wx/opt/wechat")

@app.route('/ocr', methods=['POST'])
def ocr():
    logger.info("收到新的OCR请求")
    try:
        logger.info("收到新的OCR请求")
        # Get base64 image from request
        image_data = request.json.get('image')
        if not image_data:
            logger.warning("请求中未提供图片数据")
            return jsonify({'error': 'No image data provided'}), 400

        # Create temp directory if not exists
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            logger.info(f"创建临时目录: {temp_dir}")
            os.makedirs(temp_dir)

        # Generate unique filename and save image
        filename = os.path.join(temp_dir, f"{str(uuid.uuid4())}.png")
        logger.info(f"生成临时文件: {filename}")
        
        try:
            logger.info("开始解码base64图片数据")
            image_bytes = base64.b64decode(image_data)
            with open(filename, 'wb') as f:
                f.write(image_bytes)
            logger.info("图片保存成功")

            # Process image with OCR
            logger.info("开始OCR处理")
            result = wcocr.ocr(filename)
            logger.info("OCR处理完成")
            return jsonify({'result': result})

        finally:
            # Clean up temp file
            if os.path.exists(filename):
                logger.info(f"清理临时文件: {filename}")
                os.remove(filename)

    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("启动OCR服务，监听端口5000")
    app.run(host='0.0.0.0', port=5000, threaded=True)