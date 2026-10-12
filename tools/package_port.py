"""Prepare distributable files without launcher data, worlds or renderer binaries."""
from pathlib import Path
import argparse, hashlib, io, json, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.17.0-port.26.3.1'

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build-root', type=Path, required=True)
    args = parser.parse_args()
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    checks = {}
    jars = []
    for brand in ['lod-server-support', 'voxy-server-side']:
        name = f'{brand}-fabric-{VERSION}.jar'
        target = dist / name
        shutil.copy2(args.build_root / 'fabric/build/libs' / name, target)
        with zipfile.ZipFile(target) as archive:
            meta = json.loads(archive.read('fabric.mod.json'))
            assert meta['id'] == 'lss' and meta['version'] == VERSION
            assert meta['depends']['minecraft'] == '~26.3'
            assert meta['depends']['fabricloader'] == '>=0.19.5'
            assert meta['depends']['fabric-api'] == '>=0.160.5'
            assert 'Community Port' in meta['name']
            assert 'THIRD-PARTY-NOTICES' in archive.namelist()
            assert any(n.startswith('LICENSE_') for n in archive.namelist())
            assert not any(n.startswith('dev/vox/lss/benchmark/') for n in archive.namelist())
            common_path = next(n['file'] for n in meta['jars'] if '/common-' in n['file'])
            with zipfile.ZipFile(io.BytesIO(archive.read(common_path))) as common:
                capsule = 'dev/vox/lss/internal/jdbc/sqlite-jdbc.jar.bin'
                assert capsule in common.namelist()
                with zipfile.ZipFile(io.BytesIO(common.read(capsule))) as sqlite:
                    assert 'META-INF/maven/org.xerial/sqlite-jdbc/LICENSE' in sqlite.namelist()
                assert 'META-INF/licenses/xz-java-0BSD.txt' in common.namelist()
            checks[name] = {'sha256':digest(target), 'bytes':target.stat().st_size,
                            'mod_id':'lss','minecraft':'~26.3','licenses_checked':True}
        jars.append(target)
    with zipfile.ZipFile(jars[0]) as lss, zipfile.ZipFile(jars[1]) as vss:
        for name in lss.namelist():
            if name.endswith('.class') or name.startswith('META-INF/jars/'):
                assert lss.read(name) == vss.read(name), f'Brand variants differ: {name}'
    excluded = {'.git','.gradle','build','dist','verification','__pycache__',
                '.tools','lod-server-support-main','.vscode'}
    sources = dist / f'lod-server-support-fabric-{VERSION}-project.zip'
    with zipfile.ZipFile(sources,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob('*')):
            relative = path.relative_to(ROOT)
            if not path.is_file() or any(p in excluded for p in relative.parts): continue
            if path.name in {'CLAUDE.md','CLAUDE.local.md','README.PORT.md'}: continue
            if path.suffix in {'.log','.jfr','.jar'} and path.name != 'gradle-wrapper.jar': continue
            archive.write(path, relative.as_posix())
        report = ROOT / 'verification/TEST-REPORT.md'
        if report.exists(): archive.write(report,'verification/TEST-REPORT.md')
    source_jar = dist / f'lod-server-support-fabric-{VERSION}-sources.jar'
    with zipfile.ZipFile(source_jar,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for folder in ['common/src/main/java','common/src/sqliteBridge/java',
                       'fabric/src/main/java','xplat/src/main/java']:
            for path in sorted((ROOT/folder).rglob('*.java')):
                archive.write(path,path.relative_to(ROOT/folder).as_posix())
        for name in ['LICENSE','THIRD-PARTY-NOTICES','UPSTREAM.md','CHANGELOG.md']:
            archive.write(ROOT/name,name)
    for name in ['LICENSE','THIRD-PARTY-NOTICES','UPSTREAM.md','CHANGELOG.md']:
        shutil.copy2(ROOT/name,dist/name)
    report = ROOT/'verification/TEST-REPORT.md'
    if report.exists(): shutil.copy2(report,dist/'TEST-REPORT.md')
    (ROOT/'verification/artifact-check.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    hashes = [f'{digest(p)}  {p.name}' for p in sorted(dist.iterdir())
              if p.is_file() and p.name != 'SHA256SUMS.txt']
    (dist/'SHA256SUMS.txt').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
    print(json.dumps(checks,indent=2))
    print('Prepared source JAR, source project ZIP and SHA256SUMS.txt.')

if __name__ == '__main__': main()
