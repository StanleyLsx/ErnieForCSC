# -*- coding: utf-8 -*-
# @Time : 2022/08/08 21:03 下午
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : config.py
# @Software: PyCharm

# [train, interactive_predict, test, convert2tf]
mode = 'train'

# 使用GPU设备
use_cuda = True
cuda_device = -1

configure = {
    'checkpoints_dir': 'checkpoints',
    'optimizer': 'AdamW',
    'max_sequence_length': 128,
    'learning_rate': 5e-5,
    'epochs': 5,
    'batch_size': 32,
    'model_name': 'ernie4csc.pkl',
    # 是否进行warmup
    'warmup': True,
    # warmup方法，可选：linear、cosine
    'scheduler_type': 'linear',
    # warmup步数，-1自动推断为总步数的0.1
    'num_warmup_steps': -1,
    'print_per_batch': 100,
    'is_early_stop': True,
    'patient': 3,
}