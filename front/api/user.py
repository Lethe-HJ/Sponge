from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account
from front.libs import auth


@app.route('/sponge/user/login', methods=["POST"])
def login():
    """
    用户登录接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    success, result["message"], result["status"] = verify_account(username, password)  # 验证账户
    if success:
        token = g.user.generate_auth_token()
        g.user.save_token(g.user.id, token)  # 保存token到缓存
        result["data"][0] = {
            "token": token,
            "user_id": g.user.id,
            "username": username
        }
    return result


@app.route('/sponge/user/logout', methods=["GET"])
@auth.auth_required
def logout():
    """
    用户登出接口
    """
    from front.libs.auth import clear_token
    clear_token(g.token)


# @app.route('/api/<string:language>/', methods=['GET'])
# def index(language):
#     """
#     This is the language awesomeness API
#     Call this api passing a language name and get back its features
#     ---
#     tags:
#       - Awesomeness Language API
#     parameters:
#       - name: language
#         in: path
#         type: string
#         required: true
#         description: The language name
#       - name: size
#         in: query
#         type: integer
#         description: size of awesomeness
#     responses:
#       500:
#         description: Error The language is not awesome!
#       200:
#         description: A language with its awesomeness
#         schema:
#           id: awesome
#           properties:
#             language:
#               type: string
#               description: The language name
#               default: Lua
#             features:
#               type: array
#               description: The awesomeness list
#               items:
#                 type: string
#               default: ["perfect", "simple", "lovely"]

#     """

#     language = language.lower().strip()
#     features = [
#         "awesome", "great", "dynamic", 
#         "simple", "powerful", "amazing", 
#         "perfect", "beauty", "lovely"
#     ]
#     size = int(request.args.get('size', 1))
#     if language in ['php', 'vb', 'visualbasic', 'actionscript']:
#         return "An error occurred, invalid language for awesomeness", 500
#     return jsonify(
#         language=language,
#         features=random.sample(features, size)
#     )