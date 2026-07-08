import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from app.schemas.common import Deployment


class DeploymentRegistry:
    def __init__(self, path: Path, default: Deployment):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.save_all({default.deployment_id: default.model_dump()})

    def save_all(self, data: Dict[str, dict]) -> None:
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_all(self) -> Dict[str, dict]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def list(self) -> List[Deployment]:
        return [Deployment(**item) for item in self.load_all().values()]

    def get(self, deployment_id: Optional[str]) -> Deployment:
        data = self.load_all()
        if deployment_id and deployment_id in data:
            return Deployment(**data[deployment_id])
        return Deployment(**next(iter(data.values())))

    def register(self, deployment: Deployment) -> Deployment:
        data = self.load_all()
        if not deployment.deployment_id:
            deployment.deployment_id = str(uuid.uuid4())
        data[deployment.deployment_id] = deployment.model_dump()
        self.save_all(data)
        return deployment

