import requests, logging


logger = logging.getLogger(__name__)
CUSTODY_ENDPOINT = "https://custody.arianee.com"

def create_wallet(client, network, provider, bearer_token):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/wallet/create"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {
        "provider": provider
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed to create wallet:", response.json())
        return None
    
def get_wallet_info(client, network, bearer_token):
    url = f"https://custody.arianee.com/{client}/{network}/wallet/infos"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {'error': 'Failed to get wallet info', 'details': response.text}

    return response.json()

def get_owned_nfts(client, network, bearer_token):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/nft/getOwned"
    headers = {
        "accept": "application/json; charset=utf-8",
        "authorization": f"Bearer {bearer_token}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return {"error": "Failed to get owned NFTs"}, response.status_code

def claim(client, network, bearer_token, link):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/nft/claim"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {
        "link": link
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed to claim NFT:", response.json())
        return None

def get_from_link(client, network, link, bearer_token):
    url = f"https://custody.arianee.com/{client}/{network}/nft/getFromLink"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {"link": link}
    response = requests.post(url, json=payload, headers=headers)
    
    
    return response

def transfer(client, network, bearer_token, certificate_id, to_address):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/nft/transfer"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {
        "to": to_address,
        "smartAssetId": certificate_id
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed to transfer NFT:", response.json())
        return None

def create_transfer_link(client, network, bearer_token, smart_asset_id):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/nft/createTransferLink"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {
        "smartAsset": {"id": smart_asset_id},
        "protocolName": network
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed to create transfer link:", response.json())
        return None

def create_proof_link(client, network, bearer_token, certificate_id, protocol_name):
    url = f"{CUSTODY_ENDPOINT}/{client}/{network}/nft/createProofLink"
    headers = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    payload = {
        "smartAsset": { "id": certificate_id },
        "protocolName": protocol_name
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.ok:
            return response.json()
        else:
            print("Failed to create proof link:", response.text)  
            return None
    except Exception as e:
        print(f"Error during request to create proof link: {str(e)}")
        return None


