document.addEventListener('DOMContentLoaded', function() {
    console.log('heya');
    let h2eTokenList = document.querySelector('#h2e-tokenList');
    ethereumTokens.forEach((token)=>{
        h2eTokenList.innerHTML += `
        <option value="${token.name}">
        ${token.name}
        </option>
        `
    })
});
