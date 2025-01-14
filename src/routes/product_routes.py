import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import json
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

# 从环境变量中获取 AccessKey 和 SecretKey
k_access_key = os.getenv('VOLC_ACCESS_KEY', 'default_access_key')
k_secret_key = os.getenv('VOLC_SECRET_KEY', 'default_secret_key')

# 初始化翻译服务的配置信息
k_service_info = ServiceInfo(
    'translate.volcengineapi.com',
    {'Content-Type': 'application/json'},
    Credentials(k_access_key, k_secret_key, 'translate', 'cn-north-1'),
    5,
    5
)
k_query = {
    'Action': 'TranslateText',
    'Version': '2020-06-01'
}
k_api_info = {
    'translate': ApiInfo('POST', '/', k_query, {}, {})
}

service = Service(k_service_info, k_api_info)

# 创建蓝图
bp = Blueprint('translate', __name__)

@bp.route('/basic', methods=['POST'])
@cross_origin() 
def translate():
    try:
        # 获取请求中的 JSON 数据
        data = request.get_json()
        target_language = data.get('TargetLanguage', 'zh')  # 默认目标语言为中文
        text_list = data.get('TextList')

        if not text_list or not isinstance(text_list, list):
            return jsonify({"error": "Invalid or missing TextList. It should be a list of strings."}), 400

        # 构造请求体
        body = {
            'TargetLanguage': target_language,
            'TextList': text_list
        }

        # 调用翻译服务
        res = service.json('translate', {}, json.dumps(body))
        result = json.loads(res)

        # 返回翻译结果
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
