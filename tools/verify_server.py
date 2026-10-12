"""Start the release JAR in a disposable localhost-only Fabric server and stop cleanly."""
from pathlib import Path
import argparse, hashlib, json, os, queue, shutil, subprocess, tempfile, threading, time


def main():
    parser = argparse.ArgumentParser()
    for name in ['base', 'jdk', 'api', 'mod', 'out']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix='lss-263-server-'))
    for name in ['libraries', 'versions']:
        shutil.copytree(args.base / name, profile / name)
    for name in ['fabric-server-launch.jar', 'server.jar', 'fabric-server-launcher.properties']:
        shutil.copy2(args.base / name, profile / name)
    (profile / 'mods').mkdir()
    for file in [args.api, args.mod]: shutil.copy2(file, profile / 'mods' / file.name)
    (profile / 'eula.txt').write_text('eula=true\n', encoding='utf-8')
    (profile / 'server.properties').write_text('server-ip=127.0.0.1\nserver-port=0\nonline-mode=false\nview-distance=2\nsimulation-distance=2\nlevel-type=minecraft:normal\ngenerate-structures=false\n', encoding='utf-8')
    java = args.jdk / 'bin/java.exe'
    process = subprocess.Popen([str(java), '-Xms512M', '-Xmx2G', '-Dfile.encoding=UTF-8',
        '-jar', 'fabric-server-launch.jar', 'nogui'], cwd=profile, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    events = queue.Queue()
    def read():
        for line in process.stdout: events.put(line)
        events.put(None)
    threading.Thread(target=read, daemon=True).start()
    log = []; started = False; stopped = False; diagnosed = False
    deadline = time.monotonic() + 180
    try:
        while time.monotonic() < deadline:
            try: line = events.get(timeout=1)
            except queue.Empty: continue
            if line is None: break
            log.append(line)
            if 'Done (' in line and not started:
                started = True
                process.stdin.write('vsslod diag\n'); process.stdin.flush()
            if started and ('LOD diagnostics' in line or 'LOD Store:' in line or 'LOD store:' in line or 'Processing:' in line or 'disk_reads=' in line):
                diagnosed = True
            # Diagnostics produce several lines; queue a save and stop after its heading arrives.
            if started and not stopped and (diagnosed or '=== VSS' in line or '=== LSS' in line):
                diagnosed = True; stopped = True
                process.stdin.write('save-all\nstop\n'); process.stdin.flush()
        if not stopped and process.poll() is None:
            process.stdin.write('stop\n'); process.stdin.flush()
        code = process.wait(timeout=45)
        while not events.empty():
            line = events.get_nowait()
            if line: log.append(line)
    finally:
        if process.poll() is None: process.kill(); process.wait()
        (args.out / 'production-server.log').write_text(''.join(log), encoding='utf-8')
    result = {'minecraft':'26.3', 'jar':args.mod.name, 'started':started,
              'diagnostic_command':diagnosed, 'exit_code':code,
              'sha256':hashlib.sha256(args.mod.read_bytes()).hexdigest(),
              'config_created':(profile / 'config/vss-server-config.yaml').exists()}
    (args.out / 'production-server.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    if not started or not diagnosed or code: raise SystemExit(1)

if __name__ == '__main__': main()
