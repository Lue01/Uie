from pprint import pprint
from paddlenlp import Taskflow

schema = {"武器名称": ["产国", "类型", "研发单位"]}
# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/model_best')
input_sentence = input("请输入一句话进行信息抽取：") 

extraction_result = my_ie(input_sentence) 

pprint(extraction_result)  