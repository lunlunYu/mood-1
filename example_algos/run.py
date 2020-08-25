import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import argparse

from example_algos.util.factory import AlgoFactory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', type=str, default='train')
    parser.add_argument('--model_type', type=str, default='unet')
    parser.add_argument('--recipe', type=str, default='res')
    parser.add_argument('--other', type=str, nargs='+')
    args = parser.parse_args()

    run_mode = args.run_mode
    model_type = args.model_type
    recipe = args.recipe                            # list
    other = args.other
    assert run_mode in ['train', 'predict', 'validate', 'statistics']
    assert model_type in ['unet', 'zcae', None]
    assert recipe in ['rec',  'rot', 'mask', 'res', None]
    if other != None:
        if type(other) == str:
            assert other in ['change_loss']
        elif type(recipe) == list:
            for x in other:
                assert x in ['change_loss']        
    else: other = []

    # 一个af对应一个algo，若使用多个algo则用多个af创造。
    af = AlgoFactory()
    algo = af.getAlgo(run_mode=run_mode, model_type=model_type, recipe=recipe, other=other)
    algo.run(algo)


def auto_predict():
    from example_algos.util.configure import TEST_DATASET_DIR, TRAIN_DATASET_DIR
    import os
    af = AlgoFactory()

    log_dir = os.path.join(TRAIN_DATASET_DIR, 'log')
    basic_kws = {
        'logger': 'tensorboard',
        'test_dir': TEST_DATASET_DIR,
        'load': True,
    }

    for dir_name in os.listdir(log_dir):
        if len(dir_name) >= 20: continue
        print(f'dir_name: {dir_name}')

        basic_kws['name'] = dir_name
        basic_kws['log_dir'] = log_dir
        basic_kws['load_path'] = os.path.join(log_dir, dir_name, 'checkpoint')
        algo = af.getAlgo(run_mode='predict', basic_kws=basic_kws)
        algo.run(algo, num=20, return_rec=False)


def auto_validate():
    from example_algos.util.configure import TEST_DATASET_DIR
    import os
    test_dir = os.path.join(TEST_DATASET_DIR, 'eval')
    af = AlgoFactory()
    for dir_name in os.listdir(test_dir):
        print(f'dir_name: {dir_name}')
        algo = af.getAlgo(run_mode='validate')
        algo.name = dir_name
        algo.run(algo)


def auto_statistics():
    from example_algos.util.configure import TEST_DATASET_DIR
    import os
    test_dir = os.path.join(TEST_DATASET_DIR, 'eval')
    af = AlgoFactory()
    for dir_name in os.listdir(test_dir):
        print(f'dir_name: {dir_name}')
        algo = af.getAlgo(run_mode='statistics')
        algo.name = dir_name
        algo.run(algo)


if __name__ == '__main__':
    main()
    # auto_predict()
    # auto_statistics()