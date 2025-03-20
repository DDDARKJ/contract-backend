import webbrowser
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import difflib
import threading

app = Flask(__name__)

# 计算最长公共子序列（LCS），保证精准对比
def highlight_diff_lcs(text1, text2):
    seq_matcher = difflib.SequenceMatcher(None, text1, text2)
    result1, result2 = "", ""

    for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
        if tag == "equal":  # 相同部分标绿
            result1 += f'<span class="same">{text1[i1:i2]}</span>'
            result2 += f'<span class="same">{text2[j1:j2]}</span>'
        elif tag == "replace" or tag == "delete":  # 仅模板有，标灰
            result1 += f'<span class="diff">{text1[i1:i2]}</span>'
        elif tag == "insert":  # 仅新合同有，标灰
            result2 += f'<span class="diff">{text2[j1:j2]}</span>'

    return result1, result2


# 默认模板
fixed_template = "四、双方的权利和义务\n\n1、甲方的基本权利和义务\n\n甲方应根据该项目开发的实际需要为乙方提供所需的服务器..."


@app.route("/", methods=["GET", "POST"])
def index():
    global fixed_template
    fixed_result, new_result = "", ""

    if request.method == "POST":
        if "template_text" in request.form:
            fixed_template = request.form["template_text"]
        elif "contract_text" in request.form:
            new_contract = request.form["contract_text"]
            fixed_result, new_result = highlight_diff_lcs(fixed_template, new_contract)


    return render_template("index.html", fixed_template=fixed_template, fixed_result=fixed_result,
                           new_result=new_result)

def open_browser():
    """ 只在 Flask 第一次启动时打开浏览器 """
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()  # 1.5秒后自动打开浏览器
    app.run(debug=False)  # 取消 debug 模式，避免浏览器打开两次
