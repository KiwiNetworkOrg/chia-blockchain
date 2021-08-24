from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "kiwi_harvester kiwi_timelord_launcher kiwi_timelord kiwi_farmer kiwi_full_node kiwi_wallet".split(),
    "node": "kiwi_full_node".split(),
    "harvester": "kiwi_harvester".split(),
    "farmer": "kiwi_harvester kiwi_farmer kiwi_full_node kiwi_wallet".split(),
    "farmer-no-wallet": "kiwi_harvester kiwi_farmer kiwi_full_node".split(),
    "farmer-only": "kiwi_farmer".split(),
    "timelord": "kiwi_timelord_launcher kiwi_timelord kiwi_full_node".split(),
    "timelord-only": "kiwi_timelord".split(),
    "timelord-launcher-only": "kiwi_timelord_launcher".split(),
    "wallet": "kiwi_wallet kiwi_full_node".split(),
    "wallet-only": "kiwi_wallet".split(),
    "introducer": "kiwi_introducer".split(),
    "simulator": "kiwi_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
