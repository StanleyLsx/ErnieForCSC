# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : main.py
# @Software: PyCharm
from utils.logger import get_logger
from config import use_cuda, cuda_device, configure, mode
from data import DataManager
import torch
import os
import json


def fold_check(configures):
    if configures['checkpoints_dir'] == '':
        raise Exception('checkpoints_dir did not set...')

    if not os.path.exists(configures['checkpoints_dir']):
        print('checkpoints fold not found, creating...')
        os.makedirs(configures['checkpoints_dir'])

    if not os.path.exists(configures['checkpoints_dir'] + '/logs'):
        print('log fold not found, creating...')
        os.mkdir(configures['checkpoints_dir'] + '/logs')


if __name__ == '__main__':
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    fold_check(configure)
    logger = get_logger(configure['checkpoints_dir'] + '/logs')
    if use_cuda:
        if torch.cuda.is_available():
            if cuda_device == -1:
                device = torch.device('cuda')
            else:
                device = torch.device(f'cuda:{cuda_device}')
        else:
            raise ValueError(
                "'use_cuda' set to True when cuda is unavailable."
                " Make sure CUDA is available or set use_cuda=False."
            )
    else:
        device = 'cpu'
    logger.info(f'device: {device}')
    data_manager = DataManager(logger=logger)

    if mode == 'train':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        from train import Train
        logger.info('mode: train')
        Train(data_manager, device, logger).train()
    elif mode == 'interactive_predict':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        from predict import Predictor
        logger.info('mode: interactive_predict')
        predictor = Predictor(data_manager, device, logger)
        predictor.predict_one('warm up')
        while True:
            logger.info('please input a sentence (enter [exit] to exit.)')
            sentence = input()
            if sentence == 'exit':
                break
            result = predictor.predict_one(sentence)
            print(result)
    elif mode == 'test':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        from predict import Predictor
        logger.info('mode: test')
        predictor = Predictor(data_manager, device, logger)
        predictor.predict_one('warm up')
        predictor.predict_test()
    elif mode == 'convert2tf':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: convert2tf')
        from predict import Predictor
        predictor = Predictor(data_manager, device, logger)
        predictor.convert_torch_to_tf()

