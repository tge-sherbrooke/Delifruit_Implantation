# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['RH_Billeterie.pyw'],
    pathex=[],
    binaries=[],
    datas=[('option.json', '.'), ('lib/_init_.json', 'lib'), ('lib/cred.json', 'lib'), ('lib/csv_cv_motivation.csv', 'lib'), ('lib/envoi_vers_BD.ps1', 'lib'), ('lib/git_send.bat', 'lib'), ('lib/requirements.txt', 'lib'), ('lib/credentials.env', 'lib'), ('lib/Blocnotes/Dates.txt', 'lib/Blocnotes'), ('lib/Blocnotes/Infos.txt', 'lib/Blocnotes'), ('lib/Blocnotes/LiensUtiles.txt', 'lib/Blocnotes'), ('lib/Blocnotes/Plan.txt', 'lib/Blocnotes'), ('lib', 'lib'), ('assets', 'assets'), ('lib/sauvegarde.json', 'lib'), ('Sortie/formulaire.json', 'Sortie'), ('lib/Blocnotes', 'lib/Blocnotes'), ('lib/erreurs.txt', 'lib')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RH_Billeterie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
