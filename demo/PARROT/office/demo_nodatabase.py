import wandb
import sys 
sys.path.append('../../..')
from trainer_ours_forall import Flowtrainer
from hyperparams.office import *
import os
import time
from datetime import date
# real_names = ["microwave_kettle_topknob_switch"] 
real_names = ["TA"]#["TS-sub"]
#  ["kitchen-demo-kettle-bottomknob-hinge-slide", "kitchen-demo-kettle-topknob-switch-slide", "kitchen-demo-kettle_bottomknob_switch_hinge", "kitchen-demo-microwave-bottomknob-switch-slide", "kitchen-demo-topknob_bottomknob_hinge_slide",\"kitchen-demo-microwave-kettle-topknob-hinge", "kitchen-demo-microwave_kettle_hinge_slide", "kitchen-demo-microwave_kettle_topknob_switch"]
real_names_abbr = ["formal"] # m = microwave, k = kettle, t = topknob, b = bottomknob, h = hinge, sl = slide, sw = switch

def setenv(env_name, statedim, actiondim, tasknum):
    # TODO: read from a certain file and use hps_env_setter to change hyperparams.
    # assert env_name in ["maze", "kitchen", "office", "metaworld", "lunarlander", "bipedalwalker", "halfcheetah"], "Not Implemented!"
    # print("setenv...", env_name, statedim, actiondim, tasknum)
    hps_env_setter("env_name", env_name)
    hps_env_setter("state", statedim)
    hps_env_setter("action", actiondim)
    hps_env_setter("task_num", tasknum)

if __name__ == "__main__":
    args = get_args()
    # For readers: substitute the following [two lines to your own.
    wandb.login(key=XXXXXXX)
    wandb.init(entity=XXXXXXX, project="integration_3", name="PARROT_exp3_formal_"+str(args.seed)+"_"+str(args.arch)+"_"+''.join(real_names_abbr)+"_arch4256_v4")
    # wandb.define_metric("test*", step_metric="valid_step")
    # code backup
    now = time.strftime("%a-%b-%d-%H:%M:%S-%Y", time.localtime())
    save_path = "code_backup/"+str(now)+project_name
    os.mkdir(save_path)
    os.system("cp *.py "+save_path)
    
    # torch.autograd.set_detect_anomaly(True)
    # ep = {"fetchhard_hidden_4.5": 20, "fetchhard_hidden_5.5": 20, "fetchhard_hidden_6.5": 50, "fetchhard_hidden_7.5": 50}
    
    args.train_size = 0
    args.transfer_size = 0
    hps_train_setter("early_stop_num_pretrain", 4000)
    hps_train_setter("early_stop_num_transfer", 4000) # note: this number should be > 5?
    hps_train_setter("current_method", "PARROT_decoupled_noEX")
    hps_train_setter("train_epoch", 1000)
    hps_train_setter("transfer_epoch", 1000)
    hps_train_setter("batch_size_train", 256)
    hps_train_setter("batch_size_transfer", 128)
    hps_train_setter("wdk", 0)
    hps_train_setter("seed", args.seed)
    
    hps_model_setter("type", "1layer_single")
    
    for name in real_names:
        print(name)
        args.env_name = name
        #if name != real_names[0]:
        args.train = 1
        #else: args.train = 1
        print("args.env_name:", args.env_name)
        # project_name_setter(args.env_name)
        hps_env_setter("env_name", args.env_name)
        # hps_train_setter("transfer_epoch", ep[name])
        print("project_name:", hps_env["env_name"])
        # exit(0)
        setenv(args.env_name, 97, 8, 1)
        Flowtrainer(args, hps_env, hps_train, hps_model)