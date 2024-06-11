document.getElementById('transformButton').addEventListener('click', async () => {
    const urlInput = document.getElementById('urlInput').value;
    const response = await fetch('/transform', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: urlInput })
    });

    const result = await response.json();
    const linksList = document.getElementById('linksList');
    linksList.innerHTML = '';

    if (response.status === 200) {
        result.links.forEach(link => {
            const li = document.createElement('li');
            li.textContent = link;
            li.addEventListener('click', () => {
                window.open(link, '_blank');
            });
            linksList.appendChild(li);
        });
    } else {
        alert(result.error);
    }
});

document.getElementById('copyButton').addEventListener('click', () => {
    const links = Array.from(document.getElementById('linksList').children)
                        .map(li => li.textContent)
                        .join('\n');
    navigator.clipboard.writeText(links).then(() => {
        alert('Copied to clipboard');
    });
});

document.getElementById('clearButton').addEventListener('click', () => {
    document.getElementById('linksList').innerHTML = '';
    document.getElementById('urlInput').value = '';
});
