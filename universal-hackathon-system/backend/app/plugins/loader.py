import importlib
import json
from pathlib import Path
from fastapi import APIRouter, FastAPI


class PluginMeta(dict):
    ...


def load_plugins(app: FastAPI) -> list[PluginMeta]:
    plugins_dir = Path(__file__).parent
    metas: list[PluginMeta] = []
    for path in plugins_dir.iterdir():
        if not path.is_dir() or path.name == "__pycache__":
            continue
        cfg_path = path / "plugin_config.json"
        if not cfg_path.exists():
            continue
        meta = json.loads(cfg_path.read_text())
        meta.setdefault("name", path.name)
        meta.setdefault("enabled", False)
        if not meta["enabled"]:
            continue
        # Import backend module
        module_path = f"app.plugins.{path.name}.backend"
        module = importlib.import_module(module_path)
        router = getattr(module, "router", None)
        if router:
            app.include_router(router, prefix=f"/plugins/{path.name}")
        init_plugin = getattr(module, "init_plugin", None)
        if init_plugin:
            init_plugin(app)
        metas.append(meta)
    return metas


def build_plugins_router(plugins_meta: list[PluginMeta]) -> APIRouter:
    router = APIRouter(prefix="/plugins", tags=["plugins"])

    @router.get("")
    def list_plugins():
        return plugins_meta

    return router