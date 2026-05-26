"""Local manifest at ~/.agent-forge/manifest.json — single source of state for installs."""

import contextlib
import fcntl
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Literal

from platformdirs import user_data_dir
from pydantic import BaseModel, Field

_PATH_LOCKS: dict[Path, threading.Lock] = {}
_PATH_LOCKS_GUARD = threading.Lock()


def _get_path_lock(path: Path) -> threading.Lock:
    resolved = path.resolve()
    with _PATH_LOCKS_GUARD:
        if resolved not in _PATH_LOCKS:
            _PATH_LOCKS[resolved] = threading.Lock()
        return _PATH_LOCKS[resolved]


def default_manifest_path() -> Path:
    return Path(user_data_dir("agent-forge")) / "manifest.json"


class Install(BaseModel):
    id: str
    plugin: str
    scope: Literal["plugin", "skill"]
    scope_path: str | None = None
    tier: str
    installed_sha: str
    installed_tag: str | None = None
    pinned: bool = False
    pin_target: str | None = None
    installed_at: datetime
    files: list[str] = Field(default_factory=list)


class OperationLogEntry(BaseModel):
    ts: datetime
    op: Literal["install", "update", "pin", "unpin", "remove", "sync"]
    id: str
    sha: str | None = None
    tag: str | None = None
    target: str | None = None


class Manifest(BaseModel):
    schema_version: int = 1
    agent_forge_version: str = "1.0.0"
    last_check: datetime | None = None
    remote: str = "https://github.com/tqnonline/agent-forge"
    remote_branch: str = "main"
    installs: list[Install] = Field(default_factory=list)
    operation_log: list[OperationLogEntry] = Field(default_factory=list)


class ManifestStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_manifest_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_path = self.path.with_suffix(".lock")
        self._thread_lock = _get_path_lock(self.path)

    def load(self) -> Manifest:
        if not self.path.exists():
            return Manifest()
        return Manifest.model_validate_json(self.path.read_text())

    def save(self, manifest: Manifest) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(manifest.model_dump_json(indent=2))
        tmp.replace(self.path)

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        with self._thread_lock:
            with self._lock_path.open("a+") as fh:
                try:
                    fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
                    yield
                finally:
                    fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

    def find_install(self, manifest: Manifest, install_id: str) -> Install | None:
        return next((i for i in manifest.installs if i.id == install_id), None)

    def log(self, manifest: Manifest, **kwargs) -> None:
        manifest.operation_log.append(
            OperationLogEntry(ts=datetime.now(timezone.utc), **kwargs)
        )
