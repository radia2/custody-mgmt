from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import api.custody as custody
import api.jwtGen
import datetime

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return redirect(url_for('manage_wallets'))

@app.route("/manage_wallets")
def manage_wallets():
    return render_template("NFTManagement.html")

@app.route('/api/wallets/create', methods=['POST'])
def create_wallet():
    data = request.get_json()
    client = data.get('client')
    network = data.get('network')
    provider = data.get('provider', 'arianee-custodial')
    bearer_token = data.get('bearerToken')
    wallet = custody.create_wallet(client, network, provider, bearer_token)
    if wallet:
        return jsonify(wallet), 201
    else:
        return jsonify({'error': 'Failed to create wallet'}), 400

@app.route('/generate_jwt', methods=['POST'])
def generate_jwt():
    data = request.get_json()
    payload = {
        "sub": data.get("sub"),
        "name": data.get("name"),
        "iat": datetime.datetime.now(datetime.timezone.utc).timestamp()
    }
    private_key = data.get("privateKey")
    if not private_key:
        return jsonify({"error": "Private key is missing"}), 400
    result = api.jwtGen.generate_jwt(payload, private_key)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400
    return jsonify({"token": result["token"]})

@app.route('/api/wallets/get_owned_nfts', methods=['POST'])
def fetch_owned_nfts():
    data = request.get_json()
    print("Received data:", data)
    client = data.get('client')
    network = data.get('network')
    bearer_token = data.get('bearerToken')
    
    if not client or not network or not bearer_token:
        print("Missing data")
        return jsonify({'message': 'Missing data'}), 400
    
    nfts, status_code = custody.get_owned_nfts(client, network, bearer_token)
    print("NFTs:", nfts)
    print("Status code:", status_code)
    return jsonify(nfts), status_code

@app.route('/nft/claim', methods=['POST'])
def claim_nft():
    data = request.get_json()
    client = data['client']
    network = data['network']
    bearer_token = data['bearerToken']
    link = data['link']
    nft = custody.claim(client, network, bearer_token, link)
    if nft:
        return jsonify({'success': True, 'data': nft})
    else:
        return jsonify({'success': False, 'error': 'Failed to claim NFT'}), 400

@app.route('/api/wallets/transfer', methods=['POST'])
def transfer_nft():
    data = request.get_json()
    client = data['client']
    network = data['network']
    bearer_token = data['bearerToken']
    certificate_id = data['certificateId']
    to_address = data['toAddress']
    nft_transfer = custody.transfer(client, network, bearer_token, certificate_id, to_address)
    if nft_transfer:
        return jsonify({'success': True, 'data': nft_transfer})
    else:
        return jsonify({'success': False, 'error': 'Failed to transfer NFT'}), 400

@app.route('/api/wallets/create_proof_link', methods=['POST'])
def create_proof_link():
    try:
        data = request.get_json()
        client = data['client']
        network = data['network']
        bearer_token = data['bearerToken']
        certificate_id = data['certificateId']
        protocol_name = data['protocolName']
        proof_link = custody.create_proof_link(client, network, bearer_token, certificate_id, protocol_name)
        if proof_link:
            return jsonify({'success': True, 'data': proof_link})
        else:
            return jsonify({'success': False, 'error': 'Failed to create proof link'}), 400
    except KeyError as e:
        return jsonify({'success': False, 'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/nft/get_from_link', methods=['POST'])
def api_get_from_link():
    data = request.get_json()
    client = data.get('client')
    network = data.get('network')
    link = data.get('link')
    bearer_token = data.get('bearerToken')
    missing_fields = [field for field in ['client', 'network', 'link', 'bearerToken'] if not data.get(field)]
    if missing_fields:
        return jsonify({'message': f'Missing data: {", ".join(missing_fields)}'}), 400
    response = custody.get_from_link(client, network, link, bearer_token)
    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to get data from link', 'details': response.text}), response.status_code

@app.route('/api/wallets/get_wallet_info', methods=['POST'])
def api_get_wallet_info():
    data = request.get_json()
    client = data.get('client')
    network = data.get('network')
    bearer_token = data.get('bearerToken')

    if not all([client, network, bearer_token]):
        return jsonify({'message': 'Client, network, and bearer token are required'}), 400

    wallet_info = custody.get_wallet_info(client, network, bearer_token)
    
    if 'error' in wallet_info:
        return jsonify({'message': wallet_info['error'], 'details': wallet_info.get('details')}), 400
    
    return jsonify(wallet_info), 200

@app.route('/api/wallets/create_transfer_link', methods=['POST'])
def create_transfer_link():
    data = request.get_json()
    client = data.get('client')
    network = data.get('network')
    bearer_token = data.get('bearerToken')
    smart_asset_id = data.get('smartAssetId')
    if not client or not network or not bearer_token or not smart_asset_id:
        return jsonify({'message': 'Missing data'}), 400
    transfer_link = custody.create_transfer_link(client, network, bearer_token, smart_asset_id)
    if transfer_link:
        return jsonify(transfer_link)
    else:
        return jsonify({'message': 'Failed to create transfer link'}), 404

@app.route("/submit_jwt", methods=['POST'])
def submit_jwt():
    data = request.get_json()
    token = data.get('jwt')
    public_key = data.get('publicKey')
    if not public_key.startswith('-----BEGIN PUBLIC KEY-----'):
        return jsonify({"success": False, "message": "Invalid public key format"}), 400
    result = custody.submit_jwt(token, public_key)
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

if __name__ == "__main__":
    app.run(debug=True)
