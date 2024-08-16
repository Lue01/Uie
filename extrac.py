from http.server import BaseHTTPRequestHandler, HTTPServer  
from urllib.parse import parse_qs  
import json  
from paddlenlp import Taskflow  
  
# 假设你已经有了训练好的模型路径  
model_path = './checkpoint/model_best'  
schema = {"武器名称": ["产国", "类型", "研发单位"]}  
ie = Taskflow("information_extraction", schema=schema, task_path=model_path)  
  
class InfoExtractionHandler(BaseHTTPRequestHandler):  
    def do_GET(self):  
        # 这里可以提供一个简单的 HTML 表单页面，但为简化，我们直接处理 POST  
        self.send_response(405)  # Method Not Allowed  
        self.end_headers()  
  
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  
        post_data = self.rfile.read(content_length)  
        # 假设是 application/x-www-form-urlencoded 数据  
        data = parse_qs(post_data.decode('utf-8'))  
  
        # 假设表单中有一个字段叫 "sentence"  
        sentence = data.get('sentence', [''])[0]  
        if not sentence:  
            self.send_error(400, "No sentence provided")  
            return  
        # 调用信息抽取模型  
        result = ie(sentence)  
  
        # 将结果转换为 JSON 并发送  
        self.send_response(200)  
        self.send_header('Content-type', 'application/json')  
        self.end_headers()  
        self.wfile.write(json.dumps(result).encode('utf-8'))  
  
def run(server_class=HTTPServer, handler_class=InfoExtractionHandler):  
    server_address = ('localhost', 7070)  
    httpd = server_class(server_address, handler_class)  
    print('Starting httpd...')  
    httpd.serve_forever()  
  
if __name__ == '__main__':  
    run()