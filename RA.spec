# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('config.json', '.'), ('install_java.py', '.'), ('force_java_config.py', '.'), ('download_neo4j.py', '.'), ('hooks\\neo4j.conf.template', 'Neo4jDB/conf/')],
    hiddenimports=['wx', 'wx.lib.scrolledpanel', 'wx.lib.newevent', 'json', 'threading', 'requests', 'shutil', 'traceback', 'dotenv', 'altgraph', 'neo4j', 'langchain', 'langchain_core', 'langchain_core.runnables', 'langchain_core.prompts', 'langchain_core.output_parsers', 'langchain.text_splitter', 'langchain.vectorstores', 'langchain.schema', 'langchain_openai', 'langchain_neo4j', 'langchain_community.vectorstores', 'langchain_community.vectorstores.neo4j_vector', 'langchain_community.document_loaders', 'langchain_community.document_loaders.pdf', 'langchain_community.document_loaders.text', 'langchain_community.document_loaders.docx', 'langchain_experimental', 'langchain_experimental.graph_transformers', 'openai', 'anthropic', 'google.generativeai', 'google.api_core', 'google.cloud', 'google.cloud.aiplatform', 'langchain_google_genai', 'langchain_anthropic', 'tiktoken', 'tiktoken_ext', 'tiktoken_ext.openai_public', 'docx', 'pypdf', 'wx.msw', 'tiktoken', 'tiktoken_ext', 'tiktoken_ext.openai_public'],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=['hooks/hook-app.py', 'hooks/hook-neo4j-bundling.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    manifest='app.manifest',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RA',
)
