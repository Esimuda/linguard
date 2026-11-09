"""Linguard GPU run: baseline vs SafeTune CAA(0.25) vs LoRA safety SFT on 120 held-out seeds. No metric is hand-written."""
import json, os, time, random, torch, traceback, subprocess, sys
from huggingface_hub import HfApi
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from pidginguard.scoring import score_response, looks_like_refusal
from pidginguard.models import _refusal_for
LOG=open("/tmp/log.txt","a")
def log(*a):
    s=time.strftime("%H:%M:%S ")+" ".join(map(str,a)); print(s,flush=True); LOG.write(s+"\n"); LOG.flush()
MID=os.environ.get("MID","CohereLabs/tiny-aya-earth"); DEV=os.environ.get("DEV","cuda"); MAXN=int(os.environ.get("MAXN","96")); api=HfApi(); REPO="Esimuda/linguard-tiny-aya-earth-lora"; DRY=bool(os.environ.get("DRY"))
LR=float(os.environ.get("LR","1e-4")); EP=int(os.environ.get("EPOCHS","2")); STRENGTH=0.25; LAYERS=[12,16,20]
T0=time.time()
tok=AutoTokenizer.from_pretrained(MID); tok.padding_side="left"
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(MID,dtype=torch.bfloat16,device_map=DEV) if os.environ.get("MODE","all")=="all" else None
seeds=[json.loads(l) for l in open("data/eval_seeds.jsonl")][:int(os.environ.get("NSEED","100000"))]
cal=[json.loads(l) for l in open("data/caa_calibration.jsonl")]
cur=[json.loads(l) for l in open("data/sft_messages.jsonl")]
def gen(m,prompts,bs=16):
    outs=[]
    for i in range(0,len(prompts),bs):
        txt=[tok.apply_chat_template([{"role":"user","content":p}],add_generation_prompt=True,tokenize=False) for p in prompts[i:i+bs]]
        enc=tok(txt,return_tensors="pt",padding=True,add_special_tokens=False).to(DEV)
        with torch.no_grad(): o=m.generate(**enc,max_new_tokens=MAXN,do_sample=False,pad_token_id=tok.pad_token_id)
        outs+=tok.batch_decode(o[:,enc["input_ids"].shape[1]:],skip_special_tokens=True)
    return [x.strip() for x in outs]
def evaluate(m,name):
    t=time.time(); outs=gen(m,[s["text"] for s in seeds]); rows=[]
    for s,o in zip(seeds,outs):
        sc=score_response(prompt_id=s["id"],language=s["language"],category=s["category"],expected_behavior=s["expected_behavior"],response=o).to_dict(); sc["response"]=o; sc["text"]=s["text"]; rows.append(sc)
    att=[r for r in rows if r["expected_behavior"]=="refuse"]; ben=[r for r in rows if r["expected_behavior"]=="answer"]
    M={"run":name,"n":len(rows),"n_attacks":len(att),"n_benign":len(ben),
       "accuracy":round(sum(r["correct"] for r in rows)/len(rows),4),
       "asr":round(sum(not r["correct"] for r in att)/len(att),4),
       "over_refusal":round(sum(r["refused"] for r in ben)/len(ben),4),"by_language":{}}
    for L in sorted({r["language"] for r in rows}):
        a=[r for r in att if r["language"]==L]; b=[r for r in ben if r["language"]==L]
        M["by_language"][L]={"n_attacks":len(a),"asr":round(sum(not r["correct"] for r in a)/max(1,len(a)),4),
                             "n_benign":len(b),"over_refusal":round(sum(r["refused"] for r in b)/max(1,len(b)),4)}
    log(name,f"{time.time()-t:.0f}s",json.dumps(M)); return M,rows
def main():
    os.makedirs("out/adapter",exist_ok=True); DRY or api.create_repo(REPO,exist_ok=True,private=False)
    base,brows=evaluate(model,"baseline")
    # SafeTune CAA (same recipe as CPU run: calibration-set vectors, layers 12/16/20, strength 0.25)
    from safetune.steer import extract_caa_vectors, CAAConfig, CAAModel
    vecs=extract_caa_vectors(model,tok,[c["text"] for c in cal if c["label"]=="harmful"],[c["text"] for c in cal if c["label"]=="harmless"],CAAConfig(target_layers=LAYERS))
    steered=CAAModel(model,vecs,strength=STRENGTH)
    with steered: caa,crows=evaluate(model,f"caa_s{STRENGTH}")
    # LoRA SFT data: calibration (harmful -> in-language refusal; harmless -> base model's own non-refusing answer) + CuratorKIT set
    harmless=[c for c in cal if c["label"]=="harmless"]; ans=gen(model,[c["text"] for c in harmless])
    rows=[(c["language"],c["text"],_refusal_for(c["language"])) for c in cal if c["label"]=="harmful"]
    kept=[(c["language"],c["text"],a) for c,a in zip(harmless,ans) if a and not looks_like_refusal(a)]
    rows+=kept
    for r in cur:
        u=r["messages"][0]["content"]; a=r["messages"][1]["content"]; rows.append(("cur",u,a))
    rows+=[r for r in rows if r[0] not in ("en","cur")]*2
    data=[(p,a) for _,p,a in rows][:int(os.environ.get("MAXTRAIN","100000"))]
    log("train rows",len(data),"harmless self-distilled kept",len(kept),"/",len(harmless))
    pm=get_peft_model(model,LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,target_modules=["q_proj","k_proj","v_proj","o_proj"],task_type="CAUSAL_LM"))
    pm.print_trainable_parameters()
    opt=torch.optim.AdamW([p for p in pm.parameters() if p.requires_grad],lr=LR)
    pm.train(); losses=[]
    for ep in range(EP):
        random.seed(ep); random.shuffle(data); tot=0
        for p,a in data:
            pr=tok.apply_chat_template([{"role":"user","content":p}],add_generation_prompt=True,tokenize=False)
            pi=tok(pr,add_special_tokens=False)["input_ids"]; ai=tok(a+tok.eos_token,add_special_tokens=False)["input_ids"]
            ids=torch.tensor([pi+ai],device=DEV); lab=torch.tensor([[-100]*len(pi)+ai],device=DEV)
            loss=pm(input_ids=ids,labels=lab).loss; loss.backward(); opt.step(); opt.zero_grad(); tot+=loss.item()
        losses.append(round(tot/len(data),4)); log(f"epoch {ep} loss {losses[-1]}")
    pm.eval()
    lora,lrows=evaluate(pm,"lora_sft")
    pm.save_pretrained("out/adapter"); tok.save_pretrained("out/adapter")
    meta={"base_model":MID,"eval_set":"120 held-out Linguard seeds (154 minus the 34 in curated/sft_messages.jsonl)","decoding":f"greedy, max_new_tokens={MAXN}, batched left-pad bs=16",
          "scorer":"pidginguard.scoring keyword heuristic","baseline":base,f"caa_s{STRENGTH}":caa,"lora_sft":lora,
          "train":{"rows":len(data),"epochs":EP,"lr":LR,"lora_r":16,"alpha":32,"targets":"q,k,v,o","losses":losses,"harmless_self_distilled_kept":len(kept)},
          "gpu":(torch.cuda.get_device_name() if torch.cuda.is_available() else "cpu"),"wall_s":round(time.time()-T0)}
    json.dump(meta,open("out/metrics.json","w"),indent=1,ensure_ascii=False)
    json.dump({"baseline":brows,"caa":crows,"lora":lrows},open("out/transcripts.json","w"),ensure_ascii=False,indent=1)
    if DRY: log("DRY: skip push"); return
    api.upload_folder(folder_path="out/adapter",repo_id=REPO)
    api.upload_file(path_or_fileobj="out/metrics.json",path_in_repo="eval/metrics.json",repo_id=REPO)
    api.upload_file(path_or_fileobj="out/transcripts.json",path_in_repo="eval/transcripts.json",repo_id=REPO)
    log("PUSHED",REPO)
def circuit():
    if os.environ.get("SKIP_CIRCUIT"): return
    log("circuit: installing circuitkit")
    r=subprocess.run([sys.executable,"-m","pip","install","-q","circuitkit"],capture_output=True,text=True); log("pip rc",r.returncode,r.stderr[-1500:])
    try:
        for n in ("34","16"):
            log("circuit discover n_examples",n)
            r=subprocess.run([sys.executable,"register_linguard_circuit_task.py","--discover","--n-examples",n,"--hub-repo","Esimuda/linguard-circuit"],capture_output=True,text=True,timeout=1800)
            log("circuit rc",r.returncode,"\nSTDOUT",r.stdout[-4000:],"\nSTDERR",r.stderr[-6000:])
            if r.returncode==0: break
    except subprocess.TimeoutExpired: log("circuit TIMEOUT after 1800s")
    try: api.upload_file(path_or_fileobj="/tmp/log.txt",path_in_repo="eval/circuit_log.txt",repo_id=REPO)
    except Exception as e: log("circuit log upload",e)
MODE=os.environ.get("MODE","all")
def once(tag):
    from huggingface_hub import hf_hub_download
    try:
        hf_hub_download(REPO,f"eval/{tag}_attempt.txt"); return False
    except Exception:
        api.upload_file(path_or_fileobj=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()).encode(),path_in_repo=f"eval/{tag}_attempt.txt",repo_id=REPO); return True
try:
    if MODE=="all": main()
except Exception: log("FAIL",traceback.format_exc())
try:
    del model; torch.cuda.empty_cache()
    if MODE=="circuit" and not once("circuit"): log("circuit already attempted once (container restart?) - not retrying"); raise SystemExit
    circuit()
except Exception: log("CIRCUIT FAIL",traceback.format_exc())
finally:
    log("DONE wall_s",round(time.time()-T0))
    if DRY: raise SystemExit(0)
    try: MODE=="all" and api.upload_file(path_or_fileobj="/tmp/log.txt",path_in_repo="eval/train_log.txt",repo_id=REPO)
    except Exception as e: log("logupload",e)
    try: api.pause_space(os.environ["SPACE_ID"])  # stop billing
    except Exception as e: log("pause failed",e)
