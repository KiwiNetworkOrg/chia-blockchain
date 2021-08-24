from setuptools import setup

dependencies = [
    "blspy==1.0.5",  # Signature library
    "chiavdf==1.0.2",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.4",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.8",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.7",  # Binary data management library
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the chia processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="kiwi-blockchain",
    author="Mariano Sorgente",
    author_email="mariano@chia.net",
    description="Kiwi blockchain full node, farmer, timelord, and wallet.",
    url="https://kiwinetwork.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="kiwi blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "kiwi",
        "kiwi.cmds",
        "kiwi.clvm",
        "kiwi.consensus",
        "kiwi.daemon",
        "kiwi.full_node",
        "kiwi.timelord",
        "kiwi.farmer",
        "kiwi.harvester",
        "kiwi.introducer",
        "kiwi.plotting",
        "kiwi.pools",
        "kiwi.protocols",
        "kiwi.rpc",
        "kiwi.server",
        "kiwi.simulator",
        "kiwi.types.blockchain_format",
        "kiwi.types",
        "kiwi.util",
        "kiwi.wallet",
        "kiwi.wallet.puzzles",
        "kiwi.wallet.rl_wallet",
        "kiwi.wallet.cc_wallet",
        "kiwi.wallet.did_wallet",
        "kiwi.wallet.settings",
        "kiwi.wallet.trading",
        "kiwi.wallet.util",
        "kiwi.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "kiwi = kiwi.cmds.kiwi:main",
            "kiwi_wallet = kiwi.server.start_wallet:main",
            "kiwi_full_node = kiwi.server.start_full_node:main",
            "kiwi_harvester = kiwi.server.start_harvester:main",
            "kiwi_farmer = kiwi.server.start_farmer:main",
            "kiwi_introducer = kiwi.server.start_introducer:main",
            "kiwi_timelord = kiwi.server.start_timelord:main",
            "kiwi_timelord_launcher = kiwi.timelord.timelord_launcher:main",
            "kiwi_full_node_simulator = kiwi.simulator.start_simulator:main",
        ]
    },
    package_data={
        "kiwi": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp"],
        "kiwi.util": ["initial-*.yaml", "english.txt"],
        "kiwi.ssl": ["kiwi_ca.crt", "kiwi_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
