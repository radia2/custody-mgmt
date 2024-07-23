document.addEventListener('DOMContentLoaded', () => {
    addEventListeners();
    console.log("DOM fully loaded and parsed");
});

const handleError = (error, resultDiv) => {
    console.error("Error: ", error);
    resultDiv.textContent = `Error: ${error.message}`;
};

const addEventListeners = () => {
    document.getElementById('get-owned-nfts-form').addEventListener('submit', getOwnedNFTs);
    document.getElementById('create-wallet-form').addEventListener('submit', createWallet);
    document.getElementById('claim-nft-form').addEventListener('submit', claimNFT);
    document.getElementById('transfer-nft-form').addEventListener('submit', transferNFT);
    document.getElementById('create-transfer-link-form').addEventListener('submit', createTransferLink);
    document.getElementById('create-proof-link-form').addEventListener('submit', createProofLink);
    document.getElementById('get-link-info-form').addEventListener('submit', getNFTInfoFromLink);
    document.getElementById('get-wallet-info-form').addEventListener('submit', getWalletInfo);
    document.getElementById('submit-jwt-form').addEventListener('submit', submitJWT);
    console.log("Event listeners added");
};

const getFormData = (formId) => {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    return Object.fromEntries(formData.entries());
};

const getOwnedNFTs = (event) => {
    event.preventDefault();
    const data = getFormData('get-owned-nfts-form');
    fetch('/api/wallets/get_owned_nfts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => displayOwnedNFTs(data))
    .catch(error => handleError(error, document.getElementById('owned-nfts-list')));
};

const displayOwnedNFTs = (data) => {
    const nftsDisplay = document.getElementById('owned-nfts-list');
    nftsDisplay.innerHTML = '';
    if (Array.isArray(data) && data.length > 0) {
        data.forEach(nft => {
            const nftDiv = document.createElement('div');
            nftDiv.className = 'nft-item';
            nftDiv.innerHTML = `
                <h3>NFT ID: ${nft.data.certificateId}</h3>
                <p>Name: ${nft.data.content.name || 'N/A'}</p>
                <p>SKU: ${nft.data.content.sku || 'N/A'}</p>
                <p>Serial Number: ${nft.data.content.serialnumber?.[0]?.value || 'N/A'}</p>
                <p>Issuer: ${nft.data.issuer}</p>
            `;
            if (nft.data.content.medias && nft.data.content.medias.length > 0) {
                const img = document.createElement('img');
                img.src = nft.data.content.medias[0].url;
                img.alt = nft.data.content.name || 'NFT Image';
                nftDiv.appendChild(img);
            }
            nftsDisplay.appendChild(nftDiv);
        });
    } else {
        nftsDisplay.textContent = 'No NFTs found or error occurred.';
    }
};

const createWallet = (event) => {
    event.preventDefault();
    const data = getFormData('create-wallet-form');
    fetch('/api/wallets/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => displayWalletCreationResult(status, body))
    .catch(error => handleError(error, document.getElementById('wallet-create-result')));
};

const displayWalletCreationResult = (status, body) => {
    const resultDiv = document.getElementById('wallet-create-result');
    resultDiv.textContent = status === 201 ? 'Wallet created successfully: ' + JSON.stringify(body) : 'Error creating wallet: ' + JSON.stringify(body);
};

const claimNFT = (event) => {
    event.preventDefault();
    const data = getFormData('claim-nft-form');
    fetch('/nft/claim', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.success ? 'NFT claimed successfully!' : `Failed to claim NFT: ${data.error}`))
    .catch(error => {
        console.error(error);
        alert('An error occurred while claiming the NFT.');
    });
};

const transferNFT = (event) => {
    event.preventDefault();
    const data = getFormData('transfer-nft-form');
    fetch('/api/wallets/transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.success ? 'NFT transferred successfully.' : `Error transferring NFT: ${data.error}`))
    .catch(error => {
        console.error('Error transferring NFT:', error);
        alert('Error transferring NFT: ' + error);
    });
};

const createTransferLink = (event) => {
    event.preventDefault();
    const data = getFormData('create-transfer-link-form');
    fetch('/api/wallets/create_transfer_link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => displayTransferLinkResult(data))
    .catch(error => handleError(error, document.getElementById('transfer-link-result')));
};

const displayTransferLinkResult = (data) => {
    document.getElementById('transfer-link-result').textContent = data.link ? `Transfer link created: ${JSON.stringify(data)}` : 'Failed to create transfer link';
};

const createProofLink = (event) => {
    event.preventDefault();
    const data = getFormData('create-proof-link-form');
    fetch('/api/wallets/create_proof_link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.success ? 'Proof link created: ' + JSON.stringify(data.data) : 'Error creating proof link: ' + data.error))
    .catch(error => {
        alert('Error creating proof link: ' + error);
    });
};

const getNFTInfoFromLink = (event) => {
    event.preventDefault();
    const data = getFormData('get-link-info-form');
    fetch('/api/nft/get_from_link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.ok ? response.json() : Promise.reject('Failed to get data from link'))
    .then(data => displayNFTInfoFromLink(data))
    .catch(error => handleError(error, document.getElementById('link-info-result')));
};

const displayNFTInfoFromLink = (data) => {
    const resultDiv = document.getElementById('link-info-result');
    resultDiv.innerHTML = '';
    const nftData = data.data;
    const fields = [
        { label: 'Certificate ID', value: nftData.certificateId },
        { label: 'Name', value: nftData.content.name },
        { label: 'Model', value: nftData.content.model },
        { label: 'SKU', value: nftData.content.sku },
        { label: 'Serial Number', value: nftData.content.serialnumber?.[0]?.value || 'N/A' },
        { label: 'Parent ArianeeLink', value: nftData.content.parentCertificates?.[0]?.arianeeLink || 'N/A' },
        { label: 'Protocol Name', value: nftData.protocol.name },
        { label: 'Issuer Address', value: nftData.issuer },
        { label: 'Owner Address', value: nftData.owner },
        { label: 'Is Authentic', value: nftData.isAuthentic ? 'Yes' : 'No' }
    ];
    fields.forEach(field => {
        const fieldElement = document.createElement('p');
        fieldElement.textContent = `${field.label}: ${field.value}`;
        resultDiv.appendChild(fieldElement);
    });
    if (nftData.content.medias && nftData.content.medias.length > 0) {
        const img = document.createElement('img');
        img.src = nftData.content.medias[0].url;
        resultDiv.appendChild(img);
    }
};

document.getElementById('get-wallet-info-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const client = document.getElementById('client').value;
    const network = document.getElementById('network').value;
    const bearerToken = document.getElementById('walletBearerToken').value;

    fetch('/api/wallets/get_wallet_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client, network, bearerToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to get wallet info');
        }
        return response.json();
    })
    .then(data => {
        const resultDiv = document.getElementById('wallet-info-result');
        resultDiv.innerHTML = '';  

        const fields = [
            { label: 'Address', value: data.address },
            { label: 'Provider', value: data.provider },
            { label: 'Signing Client', value: data.signingClient }
        ];

        fields.forEach(field => {
            const fieldElement = document.createElement('p');
            fieldElement.textContent = `${field.label}: ${field.value}`;
            resultDiv.appendChild(fieldElement);
        });
    })
    .catch(error => {
        const resultDiv = document.getElementById('wallet-info-result');
        resultDiv.textContent = `Error: ${error.message}`;
    });
});


const submitJWT = (event) => {
    event.preventDefault();
    const data = getFormData('submit-jwt-form');
    fetch('/submit_jwt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => displayJWTSubmitResult(data))
    .catch(error => handleError(error, document.getElementById('jwt-submit-result')));
};

const displayJWTSubmitResult = (data) => {
    const resultDiv = document.getElementById('jwt-submit-result');
    if (data.success) {
        resultDiv.textContent = 'JWT submitted successfully';
    } else {
        resultDiv.textContent = 'Error submitting JWT: ' + data.message;
    }
};
