from info.utils.captcha.captcha import captcha
from . import passport_bule
from flask import request, make_response, jsonify
from info import redis_store, constants
from info.utils.response_code import RET
from info.libs.yuntongxun.sms import CCP
import re
import random

"""
项目注册的图片验证码验证流程：
 1.获取前端发过来的图片验证码uuid
 2.导入第三方工具captcha,生成验证码
 3.将图片验证UUID及验证码存储到redis(key,value,设置过期时间）
 4.返回验证码图片给浏览器
"""


@passport_bule.route('/image_code')
def get_image_code():
    """获取图片验证码"""
    # 1.获取图片验证码的uuid
    code_id = request.args.get('code_id')
    print("uuid= " + code_id)
    # 2.生成验证码
    name, text, image = captcha.generate_captcha()
    print("验证码= " + text)
    # 3.验证码ｕuid当作key存储到redis(key,value,有效时间）
    redis_store.set('image_code_' + code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

    # 4.返回验证码图片给浏览器
    resp = make_response(image)
    # 设置响应的格式为image/jpg
    resp.headers['content_type'] = 'image/jpg'
    return resp


"""
发送短信验证码实现流程：
    接收前端发送过来的请求参数
    检查参数是否已经全部传过来
    判断手机号格式是否正确
    检查图片验证码是否正确，若不正确，则返回
    生成随机的短信验证码
    使用第三方SDK发送短信验证码
"""


@passport_bule.route('/sms_code',methods=["GET","POST"])
def send_code():
    """验证短信"""
    # １.获取前端发过来的json数据
    mobile = request.json.get('mobile')
    # 图片验证码内容
    image_code = request.json.get('image_code')
    # 图片验证码uuid
    image_code_id = request.json.get('image_code_id')
    print("%s %s %s" % (mobile,image_code,image_code_id))
    # 2.校验前端传过来的参数是否有值
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='请输入齐全的参数')
    # ３.校验手机号码
    if not re.match(r"^1[34578]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码不正确')
    # 4.获取redis数据库存储的验证码
    real_image_code = redis_store.get('image_code_' + image_code_id)
    # 5.判断验证码是否过期
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已过期")
    # 6.判断验证码是否正确,转换小写(可忽略大小写）
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="请输入正确的验证码")

    # 生成随机验证码
    result = random.randint(0, 9999)
    sms_code = "%06d" % result
    print("短信验证码：" + sms_code)

    statusCode = CCP().send_template_sms(mobile, ['1234', 5], 1)
    print(statusCode)
    if statusCode != 0:
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信失败")

    return jsonify(errno = RET.OK,errmsg="发送短信成功")
