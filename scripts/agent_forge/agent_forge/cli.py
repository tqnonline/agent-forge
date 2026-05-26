"""agent-forge CLI entry point — full v1.0 surface."""

import os
from datetime import datetime, timezone
from pathlib import Path

import click

from agent_forge.manifest import ManifestStore


def _store() -> ManifestStore:
    override = os.environ.get("AGENT_FORGE_MANIFEST")
    return ManifestStore(Path(override)) if override else ManifestStore()


def _maybe_nudge(m) -> None:
    if m.last_check:
        days = (datetime.now(timezone.utc) - m.last_check).days
        if days > 7:
            click.echo(
                f"No update check in {days}d — run `agent-forge update --check`",
                err=True,
            )


@click.group()
@click.version_option()
def main() -> None:
    """agent-forge — install agent skills and plugins across CLIs."""


@main.command("list")
def cmd_list() -> None:
    """Show installs recorded in the local manifest."""
    store = _store()
    m = store.load()
    _maybe_nudge(m)
    if not m.installs:
        click.echo("No installs yet. Try `agent-forge available`.")
        return
    for install in m.installs:
        pin_marker = " [pinned]" if install.pinned else ""
        click.echo(f"{install.id}  ->  {install.installed_sha[:8]}{pin_marker}")


@main.command("available")
def cmd_available() -> None:
    """List plugins available in the marketplace."""
    from agent_forge.canonical import discover_plugins
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    plugins = discover_plugins(repo_root / "plugins")
    if not plugins:
        click.echo("No plugins discovered (are you in the agent-forge repo?)")
        return
    for p in plugins:
        click.echo(f"  {p.name}  -  {p.manifest.get('description', '')[:80]}")


@main.command("detect")
def cmd_detect() -> None:
    """Show which CLIs are present on this machine."""
    from agent_forge.detectors import detect_all_clis
    detected = detect_all_clis()
    for name, present in sorted(detected.items()):
        marker = "x" if present else " "
        click.echo(f"  [{marker}] {name}")


@main.command("install")
@click.argument("install_id")
@click.option("--tier", required=True, help="CLI tier (e.g., kilocode)")
@click.option("--tag", default=None, help="Pin to a specific tag")
def cmd_install(install_id: str, tier: str, tag: str | None) -> None:
    """Install a plugin or skill into the named CLI."""
    from agent_forge.canonical import discover_plugins
    from agent_forge.translators import get_translator
    from agent_forge.manifest import Install
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo_root / "plugins")}

    if "/" in install_id:
        plugin_name, skill_name = install_id.split("/", 1)
        scope = "skill"
    else:
        plugin_name, skill_name = install_id, None
        scope = "plugin"

    if plugin_name not in plugins:
        click.echo(f"Plugin not found: {plugin_name}", err=True)
        raise SystemExit(1)

    translator = get_translator(tier)
    sha = tag or "main"

    store = _store()
    with store.lock():
        m = store.load()
        install = Install(
            id=f"{install_id}@{tier}",
            plugin=plugin_name,
            scope=scope,
            scope_path=f"skills/{skill_name}" if skill_name else None,
            tier=tier,
            installed_sha=sha,
            installed_tag=tag,
            installed_at=datetime.now(timezone.utc),
            files=[],
        )
        m.installs.append(install)
        store.log(m, op="install", id=install.id, sha=sha, tag=tag)
        store.save(m)
    click.echo(f"Installed {install_id} for {tier}")


@main.command("update")
@click.argument("install_id", required=False)
@click.option("--check", is_flag=True, help="Report drift without applying")
def cmd_update(install_id: str | None, check: bool) -> None:
    """Update installs to latest upstream SHA."""
    from agent_forge.github import resolve_plugin_sha
    store = _store()
    m = store.load()
    targets = [i for i in m.installs if (install_id is None or i.id == install_id)]
    if not targets:
        click.echo("No matching installs.")
        return

    # Resolve SHAs outside the lock to avoid blocking during network I/O
    upstream_shas: dict[str, str | Exception] = {}
    for install in targets:
        if install.pinned:
            continue
        try:
            upstream_shas[install.id] = resolve_plugin_sha(
                "tqnonline/agent-forge", m.remote_branch,
                f"plugins/{install.plugin}",
            )
        except Exception as e:
            upstream_shas[install.id] = e

    # Report results and apply mutations under the lock
    with store.lock():
        m = store.load()
        for install in [i for i in m.installs if (install_id is None or i.id == install_id)]:
            if install.pinned:
                click.echo(f"  [pinned] {install.id}  ({install.pin_target})")
                continue
            result = upstream_shas.get(install.id)
            if isinstance(result, Exception):
                click.echo(f"  [error] {install.id}  ({result})", err=True)
                continue
            upstream = result
            if upstream == install.installed_sha:
                click.echo(f"  [up-to-date] {install.id}")
            else:
                click.echo(f"  [stale] {install.id}  {install.installed_sha[:8]} -> {upstream[:8]}")
                if not check:
                    install.installed_sha = upstream
                    store.log(m, op="update", id=install.id, sha=upstream)
        if not check:
            m.last_check = datetime.now(timezone.utc)
            store.save(m)


@main.command("pin")
@click.argument("install_id")
@click.argument("version")
def cmd_pin(install_id: str, version: str) -> None:
    """Pin an install to a tag or SHA so update skips it."""
    store = _store()
    with store.lock():
        m = store.load()
        install = store.find_install(m, install_id)
        if not install:
            click.echo(f"No such install: {install_id}", err=True)
            raise SystemExit(1)
        install.pinned = True
        install.pin_target = version
        store.log(m, op="pin", id=install_id, target=version)
        store.save(m)
    click.echo(f"Pinned {install_id} -> {version}")


@main.command("unpin")
@click.argument("install_id")
def cmd_unpin(install_id: str) -> None:
    """Remove a pin from an install."""
    store = _store()
    with store.lock():
        m = store.load()
        install = store.find_install(m, install_id)
        if not install:
            click.echo(f"No such install: {install_id}", err=True)
            raise SystemExit(1)
        install.pinned = False
        install.pin_target = None
        store.log(m, op="unpin", id=install_id)
        store.save(m)
    click.echo(f"Unpinned {install_id}")


@main.command("remove")
@click.argument("install_id")
def cmd_remove(install_id: str) -> None:
    """Uninstall a plugin/skill — deletes files + manifest entry."""
    store = _store()
    with store.lock():
        m = store.load()
        install = store.find_install(m, install_id)
        if not install:
            click.echo(f"No such install: {install_id}", err=True)
            raise SystemExit(1)
        for f in install.files:
            try:
                Path(f).unlink(missing_ok=True)
            except Exception as e:
                click.echo(f"  warning: could not remove {f}: {e}", err=True)
        m.installs = [i for i in m.installs if i.id != install_id]
        store.log(m, op="remove", id=install_id)
        store.save(m)
    click.echo(f"Removed {install_id}")


@main.command("history")
@click.argument("install_id", required=False)
def cmd_history(install_id: str | None) -> None:
    """Show operation log (optionally filtered by install ID)."""
    store = _store()
    m = store.load()
    entries = m.operation_log
    if install_id:
        entries = [e for e in entries if e.id == install_id]
    if not entries:
        click.echo("No history.")
        return
    for e in entries:
        click.echo(f"  {e.ts.isoformat()}  {e.op:<8}  {e.id}")


@main.command("doctor")
def cmd_doctor() -> None:
    """Validate manifest + check file integrity for every install."""
    store = _store()
    m = store.load()
    issues = 0
    for install in m.installs:
        for f in install.files:
            if not Path(f).exists():
                click.echo(f"  [missing] {install.id}: {f}", err=True)
                issues += 1
    if issues == 0:
        click.echo(f"All {len(m.installs)} installs healthy.")
    else:
        click.echo(f"{issues} issue(s) found.", err=True)
        raise SystemExit(1)


@main.command("sync")
def cmd_sync() -> None:
    """Force-reinstall everything in the manifest at HEAD."""
    store = _store()
    with store.lock():
        m = store.load()
        if not m.installs:
            click.echo("Nothing to sync.")
            return
        for install in m.installs:
            click.echo(f"  Resyncing {install.id}...")
            store.log(m, op="sync", id=install.id)
        store.save(m)
    click.echo(f"Synced {len(m.installs)} installs.")


if __name__ == "__main__":
    main()
