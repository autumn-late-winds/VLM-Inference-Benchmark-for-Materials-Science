import subprocess
from fastapi import FastAPI

app = FastAPI(title="GPU Monitor")


@app.get("/gpu")
def gpu():
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.used,utilization.gpu,power.draw",
        "--format=csv,noheader,nounits",
    ]
    try:
        output = subprocess.check_output(cmd, text=True)
        rows = []
        for line in output.strip().splitlines():
            name, total, used, util, power = [x.strip() for x in line.split(",")]
            rows.append({"name": name, "memory_total_mb": total, "memory_used_mb": used, "utilization_percent": util, "power_w": power})
        return {"available": True, "gpus": rows}
    except Exception as exc:
        return {"available": False, "error": str(exc)}

